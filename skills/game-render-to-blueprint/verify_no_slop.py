#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_no_slop.py - 游戏复刻与施工图防糊弄硬性验收脚本
用法: python verify_no_slop.py <目标代码文件.html/js/ts> [最少SVG数量] [最少交互函数数量]
"""
import sys
import re
from pathlib import Path

# 1. 偷懒违禁词正则黑名单
LAZY_PATTERNS = [
    (r"//\s*TODO", "包含 // TODO 未完成标记"),
    (r"//\s*\.\.\.", "包含 // ... 省略号偷懒注释"),
    (r"/\*.*?(其余|省略|同理|TODO).*?\*/", "包含省略/其余同理块注释"),
    (r"<!--.*?(其余|省略|同理|TODO).*?-->", "包含 HTML 省略注释"),
    (r"placeholder", "包含 placeholder 占位符敷衍"),
]

# 2. 常见被用来敷衍游戏图标的 Emoji 范围
EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]+",
    flags=re.UNICODE,
)

def verify_file(filepath: str, min_svgs: int = 5, min_funcs: int = 5) -> int:
    path = Path(filepath)
    if not path.exists():
        print(f"❌ [FAIL] 找不到文件: {filepath}")
        return 1

    content = path.read_text(encoding="utf-8")
    errors = []

    # 检查 1: 违禁省略词
    for pattern, reason in LAZY_PATTERNS:
        matches = re.findall(pattern, content, flags=re.IGNORECASE | re.DOTALL)
        if matches:
            errors.append(f"🚨 检测到偷懒省略语法 ({reason}): 共 {len(matches)} 处")

    # 检查 2: SVG 矢量图数量是否达标（防止用色块或 Emoji 敷衍美术）
    svg_count = len(re.findall(r"<svg\b", content, flags=re.IGNORECASE))
    path_count = len(re.findall(r"<path\b", content, flags=re.IGNORECASE))
    if svg_count < min_svgs or path_count < min_svgs * 2:
        errors.append(
            f"🚨 美术细节严重缩水: 当前仅 {svg_count} 个 <svg> ({path_count} 条 <path>)，"
            f"要求至少 {min_svgs} 个独立精细矢量 SVG 图标！严禁用纯色块或 Emoji 敷衍！"
        )

    # 检查 3: 交互函数数量是否达标（防止写成死页面）
    func_count = len(re.findall(r"\bfunction\s+\w+|\bconst\s+\w+\s*=\s*\([^)]*\)\s*=>", content))
    if func_count < min_funcs:
        errors.append(
            f"🚨 交互逻辑缺失: 当前仅检测到 {func_count} 个函数，要求至少 {min_funcs} 个完整交互状态机函数！"
        )

    if errors:
        print("=" * 60)
        print("❌ [ANTI-SLOP GATE REJECTED] 验收未通过！发现以下糊弄行为：")
        for err in errors:
            print("  " + err)
        print("👉 请立即补全所有缺失的 SVG 路径、交互函数并删除所有省略写法后重新运行本脚本！")
        print("=" * 60)
        return 1

    print(f"✅ [ANTI-SLOP GATE PASSED] 验收通过！({svg_count} SVGs, {path_count} Paths, {func_count} Functions, 0 偷懒标记)")
    return 0

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    min_s = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    min_f = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    sys.exit(verify_file(target, min_s, min_f))
