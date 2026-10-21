#!/usr/bin/env python3
"""Validate source skills and target platform skill packages."""

from __future__ import annotations

import argparse
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


@dataclass
class PackageProfile:
    entry: str = "SKILL.md"
    max_depth: int = 2
    max_files: int = 500
    max_bytes: int = 3 * 1024 * 1024


class IntegrityError(Exception):
    pass


def parse_scalar(value: str, path: Path, line_number: int) -> str:
    value = value.strip()
    if not value:
        raise IntegrityError(f"{path}:{line_number}: empty field value")
    if value[0] in "[{>|" or "[" in value or "]" in value:
        raise IntegrityError(f"{path}:{line_number}: unsupported YAML value: {value!r}")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        quote = value[0]
        result = value[1:-1]
        if quote == '"':
            if '"' in result:
                raise IntegrityError(f"{path}:{line_number}: unclosed quoted value")
            result = result.replace('\\"', '"')
        elif "'" in result:
            raise IntegrityError(f"{path}:{line_number}: unclosed quoted value")
        value = result
    elif re.search(r"[:#]", value):
        raise IntegrityError(
            f"{path}:{line_number}: mapping values are not allowed in this context; quote the value"
        )
    return value.strip()


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise IntegrityError(f"{path}: missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise IntegrityError(f"{path}: missing closing frontmatter delimiter") from error

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):(.*)", line)
        if not match:
            raise IntegrityError(f"{path}:{line_number}: invalid frontmatter line: {line!r}")
        key, value = match.groups()
        fields[key] = parse_scalar(value, path, line_number)
    return fields


def local_references(body: str, skill_dir: Path) -> list[Path]:
    references: list[Path] = []
    patterns = (
        re.findall(r"\[[^\]]+\]\(([^)#?]+(?:#[^)]*)?)\)", body),
        re.findall(r"\((references/[^)]+)\)", body),
    )
    for value in (item for group in patterns for item in group):
        target = value.split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        references.append((skill_dir / target).resolve())
    return references


def validate_skill(path: Path) -> None:
    fields = parse_frontmatter(path)
    for required in ("name", "description"):
        if not fields.get(required, "").strip():
            raise IntegrityError(f"{path}: required frontmatter field is missing or empty: {required}")
    if fields["name"] != path.parent.name:
        raise IntegrityError(f"{path}: name {fields['name']!r} does not match directory {path.parent.name!r}")

    lines = path.read_text(encoding="utf-8").splitlines()
    body_start = lines.index("---", 1) + 1
    body = "\n".join(lines[body_start:]).strip()
    if not body:
        raise IntegrityError(f"{path}: empty body")
    for reference in local_references(body, path.parent):
        if not reference.is_file():
            raise IntegrityError(f"{path}: referenced file does not exist: {reference}")


def routed_names(router: Path) -> set[str]:
    routing_table = False
    names: set[str] = set()
    for line in router.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 路由当前缺口"):
            routing_table = True
            continue
        if routing_table and line.startswith("## "):
            break
        if routing_table and line.startswith("|"):
            names.update(re.findall(r"`([a-z][a-z0-9-]+)`", line))
    return names


def validate_sources(skills_root: Path, docs: tuple[Path, ...]) -> None:
    entries = sorted(skills_root.glob("*/SKILL.md"))
    if not entries:
        raise IntegrityError(f"{skills_root}: no skills found")
    for path in entries:
        validate_skill(path)

    actual_names = {path.parent.name for path in entries}
    missing = routed_names(skills_root / "test-privateer" / "SKILL.md") - actual_names
    if missing:
        raise IntegrityError(f"test-privateer routes missing skills: {', '.join(sorted(missing))}")

    for doc in docs:
        if not doc.is_file():
            raise IntegrityError(f"documentation file does not exist: {doc}")
        if f"{len(entries)} 个 Skill" not in doc.read_text(encoding="utf-8"):
            raise IntegrityError(f"{doc}: skill count does not match actual count ({len(entries)})")


def validate_zip(path: Path, profile: PackageProfile) -> None:
    if path.stat().st_size > profile.max_bytes:
        raise IntegrityError(f"{path}: package is {path.stat().st_size} bytes, exceeding {profile.max_bytes}")
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
    except (OSError, zipfile.BadZipFile) as error:
        raise IntegrityError(f"{path}: cannot read zip: {error}") from error

    if profile.entry not in names:
        raise IntegrityError(f"{path}: zip root does not contain {profile.entry}")
    if len(names) > profile.max_files:
        raise IntegrityError(f"{path}: package has {len(names)} entries, exceeding {profile.max_files}")
    for name in names:
        pure = PurePosixPath(name)
        if pure.is_absolute() or ".." in pure.parts or "\\" in name:
            raise IntegrityError(f"{path}: unsafe or invalid path: {name}")
        if len([part for part in pure.parts if part and part != "."]) > profile.max_depth:
            raise IntegrityError(
                f"{path}: path exceeds depth {profile.max_depth} for this platform: {name}"
            )
    print(
        f"OK {path}: {len(names)} entries, max depth "
        f"{max((len([p for p in PurePosixPath(n).parts if p and p != '.']) for n in names), default=0)}, "
        f"{path.stat().st_size} bytes"
    )


def run(root: Path, package: Path | None, profile_name: str) -> None:
    profiles = {"workbuddy-flat": PackageProfile()}
    profile = profiles[profile_name]
    validate_sources(root / "skills", (root / "README.md", root / "docs/guide.md"))
    print(f"OK source skills: {len(list((root / 'skills').glob('*/SKILL.md')))} entries")
    if package:
        validate_zip(package, profile)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--package", type=Path)
    parser.add_argument("--profile", choices=("workbuddy-flat",), default="workbuddy-flat")
    args = parser.parse_args()
    try:
        run(args.root, args.package, args.profile)
    except IntegrityError as error:
        print(f"ERROR {error}", file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
