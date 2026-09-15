#!/usr/bin/env python3
"""检查 docs/memory/MEMORY.md 的体量是否在 kit 约定的预算内。

规则（与 templates/MEMORY.md §5「体量」节一致）：
- 全文 ≤ ~400 行
- §0「交接清单」≤ ~15 行 且 ≤ ~900 字符（多模块根索引 / 模块 mini 若无此节，§0 计 0，只查全文）
- 单行 ≤ ~300 字符

为什么除了行还要查字符：行数上限管不住「单行变长」。§0 是「一句话 + 指针」的写法，
每加一份 TEST-LOG 就多一个链接——**行数还是 13 行，字符却一路涨**，
只数行的门闸一次都不会响。（实测某项目 §0 一行塞了 3 个链接、243 字符。）

用法：
    python scripts/check-memory-size.py [path/to/MEMORY.md]
默认路径：docs/memory/MEMORY.md
退出码：0 = 达标；1 = 超预算（需裁剪）
"""
import sys

# Windows 默认 GBK 控制台会因 ✗/✓ 等符号抛 UnicodeEncodeError；强制 UTF-8 输出。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOTAL_BUDGET = 400
SECTION0_BUDGET = 15
SECTION0_CHAR_BUDGET = 900
LINE_CHAR_BUDGET = 300


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/memory/MEMORY.md"
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[check-memory-size] 未找到 {path}，跳过（可能还没 init）")
        return 0

    total = len(lines)

    # 定位 §0「交接清单」：从 "## 0." / "## 0 " 或含「交接清单」的 "## " 起，
    # 到下一个 "## " 标题或分隔线 "------" 止。找不到则 0（多模块根索引/模块 mini 无此节）。
    sec0 = 0
    sec0_chars = 0
    in_sec0 = False
    for ln in lines:
        stripped = ln.rstrip("\n").strip()
        if not in_sec0:
            if (stripped.startswith("## 0.") or stripped.startswith("## 0 ")
                    or (stripped.startswith("## ") and "交接清单" in stripped)):
                in_sec0 = True
                sec0 += 1
                sec0_chars += len(stripped)
                continue
        else:
            if stripped.startswith("## ") or stripped == "------":
                break
            sec0 += 1
            sec0_chars += len(stripped)

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
        problems.append(f"§0 {sec0} 行 > 预算 {SECTION0_BUDGET}")
    if sec0_chars > SECTION0_CHAR_BUDGET:
        problems.append(
            f"§0 {sec0_chars} 字符 > 预算 {SECTION0_CHAR_BUDGET}"
            "（指针堆在同一行里，行数看不出来）"
        )
    if longest_len > LINE_CHAR_BUDGET:
        problems.append(
            f"第 {longest_no} 行 {longest_len} 字符 > 单行预算 {LINE_CHAR_BUDGET}（该外移了）"
        )

    print(
        f"[check-memory-size] {path}: 全文 {total} 行 / "
        f"§0 {sec0} 行·{sec0_chars} 字符 / 最长行 {longest_len} 字符（第 {longest_no} 行）"
    )
    if problems:
        for p in problems:
            print(f"  ✗ {p}")
        print("  裁剪 SOP 见 MEMORY.md §5「体量」节（战报→tests/ 指针，仓库地图→FRAMEWORK.md）。")
        return 1
    print("  ✓ 体量达标")
    return 0


if __name__ == "__main__":
    sys.exit(main())
