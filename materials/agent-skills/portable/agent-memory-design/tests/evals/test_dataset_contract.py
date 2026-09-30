"""不调用模型，只检查黄金用例装得进 DeepEval，并且路线标签自洽。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from deepeval.dataset import EvaluationDataset

from goldens_data import ANCHORS, GOLDENS, PRETEST_INPUTS, validate, write_dataset

DATASET = Path(__file__).with_name(".dataset.json")


def test_goldens_are_internally_consistent():
    validate()
    assert len(GOLDENS) >= 32


def test_dataset_file_matches_source_and_loads():
    write_dataset(DATASET)
    payload_names = [item["name"] for item in GOLDENS]
    dataset = EvaluationDataset()
    dataset.add_goldens_from_json_file(file_path=str(DATASET))
    loaded_names = [golden.name for golden in dataset.goldens]
    assert loaded_names == payload_names
    assert all(golden.expected_output for golden in dataset.goldens)
    assert all(golden.context for golden in dataset.goldens)


def test_routes_and_pretest_prompts_are_distinct():
    routes = {item["additional_metadata"]["route"] for item in GOLDENS}
    assert routes == {"simple", "partial", "full", "out_of_scope"}
    inputs = [item["input"] for item in GOLDENS]
    for prompt in PRETEST_INPUTS:
        assert inputs.count(prompt) == 1
    by_name = {item["name"]: item for item in GOLDENS}
    selected_sets = []
    for name, (route, selected) in ANCHORS.items():
        meta = by_name[name]["additional_metadata"]
        assert meta["route"] == route
        assert tuple(meta["selected"]) == tuple(selected)
        selected_sets.append(tuple(meta["selected"]))
    assert len(set(selected_sets)) == len(selected_sets)


def test_module_rules_hold_for_every_golden():
    for item in GOLDENS:
        meta = item["additional_metadata"]
        selected = set(meta["selected"])
        deferred = set(meta["deferred"])
        assert selected.isdisjoint(deferred)
        if meta["route"] == "simple":
            assert selected == set()
        if meta["route"] == "partial":
            assert selected
        if meta["route"] == "full":
            assert {"P", "S", "O"} <= selected
            assert "行为画像" in item["expected_output"]
        if "G" in selected:
            assert meta["graph_failure"]
        else:
            assert meta["graph_failure"] == ""
        for question in meta["questions_that_change_plan"]:
            assert question in item["expected_output"]
            assert "不问完整因素表" in item["expected_output"]


def test_reference_answers_keep_the_non_negotiable_examples():
    by_name = {item["name"]: item["expected_output"] for item in GOLDENS}
    xiaolin = by_name["writeback-xiaolin"]
    assert "小林适合创业公司" in xiaolin
    assert "用户尚未表达是否接受" in xiaolin
    assert "独立支持" in xiaolin
    hyper = by_name["constraint-paper-hyperparams"]
    for token in ("60", "MiniLM", "flan-t5", "β"):
        assert token in hyper
    assert "不适用" in by_name["definition-observation-vs-opinion"]
    assert "订单系统" in by_name["cs-refund-timeout"]
    assert "不是 BM25" in by_name["retrieval-proper-name"] or "不自动" in by_name["retrieval-proper-name"]
