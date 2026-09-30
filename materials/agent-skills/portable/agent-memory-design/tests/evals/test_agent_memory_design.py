"""技能接上可调用入口之后，才用黄金用例做模型评测。

入口通过环境变量 AGENT_MEMORY_DESIGN_ENTRY 指定，格式是「模块名:函数名」。
函数接收用户原话，返回设计文本。没有入口时本文件跳过，不假装已经评过。
"""

import importlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase

DATASET = os.path.join(os.path.dirname(__file__), ".dataset.json")


def _advise(user_input: str) -> str:
    spec = os.environ.get("AGENT_MEMORY_DESIGN_ENTRY", "").strip()
    if not spec or ":" not in spec:
        pytest.skip("未设置 AGENT_MEMORY_DESIGN_ENTRY=模块:函数，设计技能还没有可调用入口")
    module_name, function_name = spec.split(":", 1)
    module = importlib.import_module(module_name)
    advise = getattr(module, function_name)
    return advise(user_input)


dataset = EvaluationDataset()
dataset.add_goldens_from_json_file(file_path=DATASET)


@pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name or "")
def test_agent_memory_design(golden):
    actual_output = _advise(golden.input)
    from metrics import design_metrics

    assert_test(
        test_case=LLMTestCase(
            input=golden.input,
            actual_output=actual_output,
            expected_output=golden.expected_output,
            context=golden.context,
        ),
        metrics=design_metrics(),
    )
