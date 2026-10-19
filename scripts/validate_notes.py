"""Check this skill's section-note structure; not a math or rendering verifier."""

import argparse
from pathlib import Path
import re


def check_note(path):
    errors = []
    text = path.read_text(encoding="utf-8-sig")
    # Ignore YAML and fenced examples, whose headings are not Outline entries.
    text = re.sub(r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", "", text, count=1, flags=re.S)
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence is None:
            lines.append(line)
    text = "\n".join(lines)
    headings = [(len(m[1]), m[2].strip()) for m in re.finditer(r"^(#{1,6})[ \t]+(.+)$", text, re.M)]
    if [title for level, title in headings if level == 3] != ["一、概念", "二、重点题型"]:
        errors.append("H3 必须且只能依次为“一、概念”“二、重点题型”")
    for level, pattern, label in [(1, r"第\s*\S+\s*章\s+\S", "章名"), (2, r"第\s*\S+\s*节\s+\S", "节名")]:
        titles = [title for depth, title in headings if depth == level]
        if len(titles) != 1 or not re.match(pattern, titles[0]):
            errors.append(f"必须有且仅有一个 H{level} {label}")
    levels = [level for level, _ in headings]
    if levels[:4] != [1, 2, 3, 3] or any(level != 4 for level in levels[4:]):
        errors.append("标题顺序应为章 H1、节 H2、概念 H3、重点题型 H3、各题型 H4")
    types = list(re.finditer(r"^####[ \t]+(.+)$", text, re.M))
    if not types:
        errors.append("缺少重点题型；若来源确无题型，应人工复核并说明")
    for i, match in enumerate(types):
        title = match[1].strip()
        if not re.match(r"题型[^：:]+[：:]\S", title):
            errors.append(f"题型标题格式不正确：{title}")
        body = text[match.end():types[i + 1].start() if i + 1 < len(types) else len(text)]
        for field in ["题型特征", "解题方法", "核心公式", "典型例题", "易错点"]:
            if not re.search(r"\*\*" + field + r"(?:\s*\d+)?\*\*", body):
                errors.append(f"{title} 缺少字段：{field}")
    if re.search(r"\{\{[^{}]+\}\}", text):
        errors.append("存在未替换的模板占位符")
    # Remove escaped dollars and count delimiters; balanced does not mean valid LaTeX.
    math = re.sub(r"\\\$", "", text)
    if math.count("$$") % 2:
        errors.append("独立公式 $$ 未配对")
    if math.replace("$$", "").count("$") % 2:
        errors.append("行内公式 $ 未配对")
    return errors, len(types)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="课程笔记根目录，不是 Skill 目录")
    args = parser.parse_args()
    if not args.folder.is_dir():
        parser.error("笔记目录不存在")
    # Match the numbered section filenames specified by the skill, not indexes.
    notes = sorted(p for p in args.folder.rglob("*.md") if re.match(r"^\d+(?:\.\d+)+\s+", p.stem))
    if not notes:
        parser.exit(1, "没有找到形如“2.1 节名.md”的分节笔记。\n")
    failures = 0
    total_types = 0
    for path in notes:
        errors, count = check_note(path)
        total_types += count
        failures += bool(errors)
        print(f"{'FAIL' if errors else 'OK'} {path.relative_to(args.folder)} ({count} 类题型)")
        for error in errors:
            print(f"  - {error}")
    print(f"共 {len(notes)} 节、{total_types} 类题型；{failures} 个文件未通过结构检查。")
    print("本检查不验证数学正确性、资料覆盖、链接、渲染或设备同步。")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
