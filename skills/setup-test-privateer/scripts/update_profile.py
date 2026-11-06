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


def _atomic_write(path: Path, content: str, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        temporary.chmod(mode)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _validate_profile_location(profile_dir: Path, path: Path) -> None:
    if profile_dir.is_symlink():
        raise UnmanagedProfileError("profile directory must not be a symbolic link")
    if not profile_dir.is_dir():
        raise NotADirectoryError(f"profile directory is not a directory: {profile_dir}")
    if path.is_symlink():
        raise UnmanagedProfileError("profile file must not be a symbolic link")


def _restore(
    profile_dir: Path,
    path: Path,
    original: str | None,
    mode: int,
) -> None:
    if profile_dir.is_symlink():
        raise UnmanagedProfileError("refusing to restore through a symbolic link")
    if profile_dir.exists() and not profile_dir.is_dir():
        raise NotADirectoryError(f"profile directory is not a directory: {profile_dir}")
    if path.is_symlink():
        path.unlink()
    if original is None:
        path.unlink(missing_ok=True)
    else:
        _atomic_write(path, original, mode)


def update_profile(
    project: Path,
    managed_content: str,
    after_write: Callable[[Path], None] | None = None,
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
    original = _read_text(path) if path.exists() else None
    original_mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644

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

    try:
        _atomic_write(path, expected, original_mode)
        if after_write:
            after_write(path)
        _validate_profile_location(profile_dir, path)
        path.chmod(original_mode)
        if _read_text(path) != expected:
            raise ProfileReadbackError(
                "profile readback differs from the confirmed draft"
            )
        if stat.S_IMODE(path.stat().st_mode) != original_mode:
            raise ProfileReadbackError("profile permissions differ after writing")
    except Exception as error:
        try:
            _restore(profile_dir, path, original, original_mode)
        except Exception as restore_error:
            raise ProfileReadbackError(
                "profile update failed and the original state could not be restored"
            ) from restore_error
        if isinstance(error, ProfileReadbackError):
            raise
        raise ProfileReadbackError(
            "profile update failed; the original state was restored"
        ) from error
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
