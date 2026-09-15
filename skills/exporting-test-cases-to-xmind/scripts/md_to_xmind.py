#!/usr/bin/env python3
"""Convert a test-case Markdown file to a native XMind 2020+ file."""

import argparse
import json
import re
import tempfile
import uuid
import zipfile
from pathlib import Path


CASE_COLUMNS = {"id", "场景／前置条件", "怎么操作", "预期结果"}
IGNORED_TABLE_COLUMNS = {"用例", "版本与环境／时间", "req id", "需求功能点"}
SKIPPED_HEADING_PREFIXES = ("执行记录", "附录")


def make_id():
    return uuid.uuid4().hex[:24]


def topic(title, children=None):
    node = {"id": make_id(), "title": str(title).strip()}
    clean_children = [child for child in (children or []) if child]
    if clean_children:
        node["children"] = {"attached": clean_children}
    return node


def split_cell(value):
    value = re.sub(r"<br\s*/?>", "\n", value or "").strip()
    return [part.strip() for part in value.splitlines() if part.strip()]


def parse_table(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    cells, current, escaped = [], [], False
    for char in row:
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
            continue
        if char == "\\" and not escaped:
            escaped = True
            continue
        current.append(char)
        escaped = False
    cells.append("".join(current).strip())
    return cells


def is_table_boundary(row):
    cells = parse_table(row)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def table_name(header):
    return {cell.casefold() for cell in header}


def row_value(header, row, name):
    try:
        return row[header.index(name.casefold())]
    except (ValueError, IndexError):
        return ""


def case_topics(header, row):
    title_parts = [row_value(header, row, "ID")]
    check = row_value(header, row, "要检查什么")
    if check:
        title_parts.append(check)
    fields = [
        ("场景／前置", row_value(header, row, "场景／前置条件")),
        ("操作", row_value(header, row, "怎么操作")),
        ("预期", row_value(header, row, "预期结果")),
        ("安排", row_value(header, row, "本轮安排")),
        ("条件", row_value(header, row, "当前条件")),
        ("证据", row_value(header, row, "需要保留什么")),
        ("依据", row_value(header, row, "关联风险／依据")),
    ]
    children = []
    for label, value in fields:
        values = split_cell(value) or ["待确认"]
        children.extend(topic(f"{label}：{item}") for item in values)
    return topic(" · ".join(part for part in title_parts if part), children)


class TreeBuilder:
    def __init__(self, title):
        self.root = topic(title)
        self.parents = [self.root]

    @property
    def current(self):
        return self.parents[-1]

    def add_heading(self, level, title):
        node = topic(title)
        parent = self.parents[min(level - 1, len(self.parents) - 1)]
        parent.setdefault("children", {"attached": []})["attached"].append(node)
        self.parents = self.parents[:level]
        self.parents.append(node)

    def add_case(self, header, row):
        current = self.current
        current.setdefault("children", {"attached": []})["attached"].append(
            case_topics(header, row)
        )


def document_title(markdown, source):
    for line in markdown.splitlines():
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip()
    return source.stem


def markdown_to_topic(markdown, source):
    tree = TreeBuilder(document_title(markdown, source))
    lines = markdown.splitlines()
    in_code = False
    skip_level = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith("```"):
            in_code = not in_code
            index += 1
            continue
        if not in_code and line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is not None:
                index += 1
                continue
            if title and title.startswith(SKIPPED_HEADING_PREFIXES):
                skip_level = level
            elif title and not (level == 1 and title == tree.root["title"]):
                tree.add_heading(level, title)
            index += 1
            continue
        if not in_code and line.lstrip().startswith("|") and index + 1 < len(lines):
            header = [cell.casefold() for cell in parse_table(lines[index])]
            if not is_table_boundary(lines[index + 1]):
                index += 1
                continue
            names = set(header)
            if names & IGNORED_TABLE_COLUMNS:
                index += 1
                continue
            if CASE_COLUMNS.issubset(names):
                index += 2
                while index < len(lines) and lines[index].lstrip().startswith("|"):
                    row = parse_table(lines[index])
                    if len(row) == len(header):
                        tree.add_case(header, row)
                    index += 1
                continue
        index += 1
    return tree.root


def write_xmind(root, destination):
    sheet = {
        "id": make_id(),
        "class": "sheet",
        "title": root["title"],
        "rootTopic": root,
    }
    content = json.dumps([sheet], ensure_ascii=False, indent=2)
    metadata = json.dumps(
        {"creator": {"name": "test-privateer-xmind-export", "version": "1.0"}},
        ensure_ascii=False,
    )
    manifest = json.dumps({"file-entries": {"content.json": {}, "metadata.json": {}}})
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.json", content)
        archive.writestr("metadata.json", metadata)
        archive.writestr("manifest.json", manifest)


def count_titles(node, needle):
    count = 1 if needle in node["title"] else 0
    return count + sum(count_titles(child, needle) for child in node.get("children", {}).get("attached", []))


def convert(source, destination=None):
    source = Path(source)
    markdown = source.read_text(encoding="utf-8")
    output = Path(destination) if destination else source.with_suffix(".xmind")
    write_xmind(markdown_to_topic(markdown, source), output)
    return output


def self_test():
    sample = """# 登录测试

## 表单验证

| ID | 关联风险／依据 | 本轮安排 | 要检查什么 | 场景／前置条件 | 怎么操作 | 预期结果 | 需要保留什么 | 当前条件 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | R-001 | P0 | 空密码 | 已打开登录页 | 点击登录<br>观察提示 | 显示必填提示 | 页面截图 | 可执行 |

## 执行记录

| 用例 | 版本与环境／时间 | 实际结果 | 证据 | 发现及后续 |
| --- | --- | --- | --- | --- |
"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source = Path(temp_dir) / "cases.md"
        source.write_text(sample, encoding="utf-8")
        output = convert(source)
        with zipfile.ZipFile(output) as archive:
            assert {"content.json", "metadata.json", "manifest.json"} <= set(archive.namelist())
            sheet = json.loads(archive.read("content.json"))[0]
        assert sheet["rootTopic"]["title"] == "登录测试"
        assert [x["title"] for x in sheet["rootTopic"]["children"]["attached"]] == ["表单验证"]
        assert count_titles(sheet["rootTopic"], "C-001") == 1
        assert count_titles(sheet["rootTopic"], "显示必填提示") == 1
        assert count_titles(sheet["rootTopic"], "执行记录") == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", help="Markdown test-case file")
    parser.add_argument("-o", "--output", help="Destination .xmind file")
    parser.add_argument("--self-test", action="store_true", help="Run the built-in check")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test passed")
        return
    if not args.source:
        parser.error("source is required unless --self-test is used")
    output = convert(args.source, args.output)
    print(f"XMind exported: {output}")


if __name__ == "__main__":
    main()
