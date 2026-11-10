#!/usr/bin/env python3
"""Safely replace the managed Test Privateer project profile block."""

from __future__ import annotations

import argparse
import os
import stat
import tempfile
from pathlib import Path
from typing import Callable


START = "<!-- test-privateer-managed:start -->"
END = "<!-- test-privateer-managed:end -->"


class UnmanagedProfileError(RuntimeError):
    pass


class ProfileReadbackError(RuntimeError):
    pass


def _read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _validate_profile_location(profile_dir: Path, path: Path) -> None:
    if profile_dir.is_symlink():
        raise UnmanagedProfileError("profile directory must not be a symbolic link")
    if not profile_dir.is_dir():
        raise NotADirectoryError(f"profile directory is not a directory: {profile_dir}")
    if path.is_symlink():
        raise UnmanagedProfileError("profile file must not be a symbolic link")


def _version(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def _snapshot(path: Path) -> tuple[os.stat_result, str] | None:
    if path.is_symlink():
        raise UnmanagedProfileError("profile file must not be a symbolic link")
    try:
        before = path.stat()
    except FileNotFoundError:
        return None
    content = _read_text(path)
    after = path.stat()
    if _version(before) != _version(after):
        raise ProfileReadbackError("profile changed while reading; preserve it and retry")
    return after, content


def update_profile(
    project: Path,
    managed_content: str,
    prepare_candidate: Callable[[Path], None] | None = None,
) -> Path:
    project = project.resolve()
    if not project.is_dir():
        raise NotADirectoryError(f"project directory does not exist: {project}")

    profile_dir = project / ".test-privateer"
    if profile_dir.is_symlink():
        raise UnmanagedProfileError("profile directory must not be a symbolic link")
    if profile_dir.exists() and not profile_dir.is_dir():
        raise NotADirectoryError(f"profile directory is not a directory: {profile_dir}")

    path = profile_dir / "project.md"
    if path.is_symlink():
        raise UnmanagedProfileError("profile file must not be a symbolic link")
    initial = _snapshot(path)
    original = initial[1] if initial else None
    original_mode = stat.S_IMODE(initial[0].st_mode) if initial else 0o644

    if START in managed_content or END in managed_content:
        raise ValueError("managed content must not contain profile markers")
    if not managed_content.strip():
        raise ValueError("managed content must not be empty")

    newline = "\r\n" if original and "\r\n" in original else "\n"
    normalized = managed_content.replace("\r\n", "\n").replace("\r", "\n")
    normalized = newline.join(normalized.strip().split("\n"))
    block = f"{START}{newline}{normalized}{newline}{END}"
    if original is None:
        expected = f"# Test Privateer 项目配置{newline}{newline}{block}{newline}"
    else:
        if original.count(START) != 1 or original.count(END) != 1:
            raise UnmanagedProfileError(
                "existing profile needs exactly one managed marker pair"
            )
        start = original.index(START)
        try:
            end = original.index(END, start) + len(END)
        except ValueError as error:
            raise UnmanagedProfileError(
                "managed marker end must follow the start marker"
            ) from error
        expected = original[:start] + block + original[end:]

    profile_dir.mkdir(exist_ok=True)
    _validate_profile_location(profile_dir, path)
    directory_fd = os.open(profile_dir, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    candidate: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="", dir=profile_dir, delete=False
        ) as handle:
            candidate = Path(handle.name)
            handle.write(expected)
        candidate.chmod(original_mode)
        if prepare_candidate:
            prepare_candidate(candidate)
        _validate_profile_location(profile_dir, path)
        directory = profile_dir.stat()
        opened = os.fstat(directory_fd)
        if (directory.st_dev, directory.st_ino) != (opened.st_dev, opened.st_ino):
            raise ProfileReadbackError("profile directory changed; preserve current files")
        if candidate.is_symlink():
            raise ProfileReadbackError("candidate must not be a symbolic link")
        candidate.chmod(original_mode)
        prepared = _snapshot(candidate)
        if prepared is None or prepared[1] != expected:
            raise ProfileReadbackError("candidate differs from the confirmed draft")
        if stat.S_IMODE(prepared[0].st_mode) != original_mode:
            raise ProfileReadbackError("candidate permissions differ after preparation")
        current = _snapshot(path)
        if ((current is None) != (initial is None) or (current and initial and (
            current[1] != initial[1] or _version(current[0]) != _version(initial[0])
        ))):
            raise ProfileReadbackError("profile write conflict; current file was preserved")
        # shortcut: uncoordinated editors can race this check; use a shared lock if multi-writer isolation is required.
        os.replace(candidate.name, path.name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
        candidate = None
        _validate_profile_location(profile_dir, path)
        published = _snapshot(path)
        if (published is None or published[1] != expected
                or stat.S_IMODE(published[0].st_mode) != original_mode
                or published[0].st_ino != prepared[0].st_ino
                or published[0].st_dev != prepared[0].st_dev):
            raise ProfileReadbackError("profile readback mismatch; preserve current file and inspect it")
    except Exception as error:
        if isinstance(error, ProfileReadbackError):
            raise
        raise ProfileReadbackError(
            "profile update incomplete; current target was not rolled back; inspect it before retrying"
        ) from error
    finally:
        try:
            if candidate is not None:
                try:
                    os.unlink(candidate.name, dir_fd=directory_fd)
                except FileNotFoundError:
                    pass
        finally:
            os.close(directory_fd)
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        type=Path,
        required=True,
        help="existing project root; only .test-privateer/ may be created",
    )
    parser.add_argument(
        "--managed-content",
        type=Path,
        required=True,
        help="body between the managed markers, without either marker",
    )
    args = parser.parse_args()
    path = update_profile(
        args.project.resolve(),
        args.managed_content.read_text(encoding="utf-8"),
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
