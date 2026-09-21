#!/usr/bin/env python3
"""检查 memory/kit/MEMORY.md 的体量是否在 kit 约定的预算内。

规则（与 templates/MEMORY.md §5「体量」节一致）：
- 全文 ≤ ~400 行
- §0「交接清单」**实义行** ≤ ~15 行 且 ≤ ~900 字符；空行 / 标题 / ">" 说明块**不计**
  （多模块根索引 / 模块 mini 若无此节，§0 计 0，只查全文）
- 单行 ≤ ~300 字符

为什么 §0 只数实义行：空行、标题、说明块不产生阅读负担，却会吃掉行预算——实测 4 个空行
占掉 15 行预算的 27%，导致「字符还剩 159，一条指针都加不了」。两个预算一个卡死一个富余。

为什么除了行还要查字符：行数上限管不住「单行变长」。§0 本来就鼓励把同一主题的指针并到
一行，**行数可以不涨、字符却一路涨**，只数行的门闸一次都不会响。所以两个维度都要查。

另外**顺带报告**同目录 HANDOVER.md 的行数，超过 200 行时打印一条提醒：**只提醒，不影响退出码**。
HANDOVER 是「必知事实」的终点——没有 tests/ 那样的外移退路，「超了就裁」的 SOP 在那里不成立
（过期事实该删、现状事实必须留）。过提醒线时该做的是逐条问「这条还成立吗」，不成立就删。

同样**顺带报告**同目录 REFERENCES.md 的**行数与条目数**（条目 = 行首 "## "），超过 80 行时提醒：
**只提醒，不影响退出码**。地址簿的真实故障不是「太长」，而是「某一条慢慢变成研究正文」
（实测踩过：把研究正文写进地址簿，最后不得不整段移出去）。约束写在 templates/REFERENCES.md
正文里，这里只给一个可见的数字，不替人做判断。

用法：
    python scaffold/scripts/check-memory-size.py [path/to/MEMORY.md]
默认路径：memory/kit/MEMORY.md
退出码：0 = 达标；1 = 超预算（需裁剪）。**仅由 MEMORY 决定，HANDOVER 不参与。**
"""
import os
import sys

# Windows 默认 GBK 控制台会因 ✗/✓ 等符号抛 UnicodeEncodeError；强制 UTF-8 输出。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOTAL_BUDGET = 400
SECTION0_BUDGET = 15
SECTION0_CHAR_BUDGET = 900
LINE_CHAR_BUDGET = 300
HANDOVER_WARN_LINES = 200
REFERENCES_WARN_LINES = 80


def report_handover(memory_path: str) -> None:
    """顺带报告同目录 HANDOVER.md 的行数。只报告，无预算，不参与退出码。"""
    handover = os.path.join(os.path.dirname(memory_path) or ".", "HANDOVER.md")
    # Windows 下 os.path.join 产出反斜杠，与上面 MEMORY 那行的正斜杠不一致；显示统一用正斜杠
    shown = handover.replace("\\", "/")
    try:
        with open(handover, encoding="utf-8") as f:
            n = len(f.readlines())
    except FileNotFoundError:
        return
    except OSError as e:
        print(f"[check-memory-size] {shown}: 读取失败（{e}），跳过")
        return
    print(f"[check-memory-size] {shown}: 全文 {n} 行（仅供参考，不影响退出码）")
    if n > HANDOVER_WARN_LINES:
        print(
            f"  ⚠ HANDOVER 全文 {n} 行 > 提醒线 {HANDOVER_WARN_LINES}：逐条问「这条还成立吗」，"
            "不成立就删。它是必知事实的终点、没有外移退路，唯一瘦身方式是删。"
        )


def report_references(memory_path: str) -> None:
    """顺带报告同目录 REFERENCES.md 的行数与条目数。只报告，无预算，不参与退出码。

    条目 = 行首 "## " 的行（templates/REFERENCES.md 约定：每条参考用 ##，说明性段落不用）。
    """
    refs = os.path.join(os.path.dirname(memory_path) or ".", "REFERENCES.md")
    shown = refs.replace("\\", "/")  # 与上面 MEMORY 那行的正斜杠保持一致
    try:
        with open(refs, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return
    except OSError as e:
        print(f"[check-memory-size] {shown}: 读取失败（{e}），跳过")
        return
    n = len(lines)
    entries = sum(1 for ln in lines if ln.startswith("## "))
    print(f"[check-memory-size] {shown}: 全文 {n} 行 / 条目 {entries} 个（仅供参考，不影响退出码）")
    if n > REFERENCES_WARN_LINES:
        print(
            f"  ⚠ REFERENCES 全文 {n} 行 > 提醒线 {REFERENCES_WARN_LINES}：逐条问「这个还在用吗」，"
            "不用的直接删（地址簿的瘦身方式是删死链，不是外移）。"
        )


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "memory/kit/MEMORY.md"
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[check-memory-size] 未找到 {path}，跳过（可能还没 init）")
        return 0

    total = len(lines)

    # 定位 §0「交接清单」：从 "## 0." / "## 0 " 或含「交接清单」的 "## " 起，
    # 到下一个 "## " 标题或分隔线 "------" 止。找不到则 0（多模块根索引/模块 mini 无此节）。
    sec0_lines = []
    in_sec0 = False
    for ln in lines:
        stripped = ln.rstrip("\n").strip()
        if not in_sec0:
            if (stripped.startswith("## 0.") or stripped.startswith("## 0 ")
                    or (stripped.startswith("## ") and "交接清单" in stripped)):
                in_sec0 = True
                continue
        else:
            if stripped.startswith("## ") or stripped == "------":
                break
            sec0_lines.append(stripped)

    # §0 只数「实义行」：空行、标题、">" 说明块不计（理由见文件头）。
    # 说明块仍然打印出来，只是不参与判定。
    def _is_content(s: str) -> bool:
        return s != "" and not s.startswith("#") and not s.startswith(">")

    sec0 = sum(1 for s in sec0_lines if _is_content(s))
    sec0_chars = sum(len(s) for s in sec0_lines if _is_content(s))
    note_lines = len(sec0_lines) - sec0
    note_chars = sum(len(s) for s in sec0_lines) - sec0_chars

    # 最长行（跳过代码围栏内容不做区分——MEMORY 里本来也不该有大段代码）
    longest_len = 0
    longest_no = 0
    for i, ln in enumerate(lines, start=1):
        n = len(ln.rstrip("\n"))
        if n > longest_len:
            longest_len = n
            longest_no = i

    problems = []
    if total > TOTAL_BUDGET:
        problems.append(f"全文 {total} 行 > 预算 {TOTAL_BUDGET}")
    if sec0 > SECTION0_BUDGET:
        problems.append(f"§0 实义 {sec0} 行 > 预算 {SECTION0_BUDGET}（空行 / 标题 / 说明块已不计）")
    if sec0_chars > SECTION0_CHAR_BUDGET:
        problems.append(
            f"§0 实义 {sec0_chars} 字符 > 预算 {SECTION0_CHAR_BUDGET}"
            "（指针堆在同一行里，行数看不出来）"
        )
    if longest_len > LINE_CHAR_BUDGET:
        problems.append(
            f"第 {longest_no} 行 {longest_len} 字符 > 单行预算 {LINE_CHAR_BUDGET}（该外移了）"
        )

    print(
        f"[check-memory-size] {path}: 全文 {total} 行 / "
        f"§0 实义 {sec0} 行·{sec0_chars} 字符"
        + (f"（另有 {note_lines} 行·{note_chars} 字符不计：空行 / 标题 / 说明块）" if note_lines else "")
        + f" / 最长行 {longest_len} 字符（第 {longest_no} 行）"
    )
    report_handover(path)
    report_references(path)
    if problems:
        for p in problems:
            print(f"  ✗ {p}")
        print("  裁剪 SOP 见 MEMORY.md §5「体量」节（战报→tests/ 指针，仓库地图→FRAMEWORK.md）。")
        return 1
    print("  ✓ 体量达标")
    return 0


if __name__ == "__main__":
    sys.exit(main())
