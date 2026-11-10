#!/usr/bin/env python3
"""Record real-model runs; exit status is not a behavioral verdict."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / ".local/validation/skill-contracts"
SNAPSHOT: Path
MODEL = "gpt-6.1-sol"

PROMPT = "Read ./AGENTS.md and ./task.md, then complete the request within its scope."


def file_hashes(root: Path) -> dict[str, str]:
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            hashes[str(path.relative_to(root))] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


def parse_events(text: str) -> tuple[str, str]:
    loads = []
    tools = []
    skill_pattern = re.compile(
        r"(?:\./)?skills/[a-z0-9-]+/(?:SKILL\.md|references/[a-z0-9._/-]+)"
    )
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") or {}
        if event.get("type") != "item.completed" or item.get("type") != "command_execution":
            continue
        command = item.get("command", "")
        tools.append(command)
        if item.get("exit_code") != 0:
            continue
        for match in skill_pattern.findall(command):
            if match not in loads:
                loads.append(match)
    return (
        "\n".join(loads) + ("\n" if loads else ""),
        "\n\n".join(tools) + ("\n" if tools else ""),
    )


def prepare_project(scenario):
    project=Path(tempfile.mkdtemp(prefix="client-workspace-"))
    shutil.copytree(SNAPSHOT,project/"skills",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    rules="""# Project rules
Work only in this project and the supplied skills snapshot. Do not access global skills or other projects, external network, installers or paid services. Do not modify skills/. Respect task-specific scope. Product src/ is read-only. Tests and evidence may be created only when requested.
"""
    if scenario.get("discovery"):
        rules+="Available skills (read the appropriate SKILL.md before applying it):\n"
        for f in sorted((project/"skills").glob("*/SKILL.md")):
            desc=next(x.removeprefix("description:").strip() for x in f.read_text().splitlines() if x.startswith("description:"))
            rules+=f"- {f.parent.name}: {desc} (skills/{f.parent.name}/SKILL.md)\n"
    else:
        rules+="Read skills/test-privateer/SKILL.md first and follow the route for the current task.\n"
    (project/"AGENTS.md").write_text(rules)
    (project/"task.md").write_text(scenario["task"])
    for name,content in scenario["files"].items():
        f=project/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(content)
    subprocess.run(["git","init","-q"],cwd=project,check=True)
    subprocess.run(["git","add","."],cwd=project,check=True)
    subprocess.run(["git","-c","user.name=Behavior Run","-c","user.email=behavior@example.invalid","commit","-qm","initial"],cwd=project,check=True)
    return project


def snapshot_project(project: Path, destination: Path) -> None:
    target = destination / "final-project"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(project, target, ignore=shutil.ignore_patterns(".git"))


def run_scenario(name: str, scenario: dict, output_root: Path, timeout: int) -> dict:
    destination = output_root / name
    destination.mkdir(parents=True, exist_ok=True)
    project = prepare_project(scenario)
    initial = file_hashes(project)
    (destination / "prompt.txt").write_text(PROMPT, encoding="utf-8")
    (destination / "task.md").write_text(scenario["task"], encoding="utf-8")
    (destination / "initial-files.sha256").write_text(
        json.dumps(initial, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    final_path = destination / "final.md"
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--json",
        "--color",
        "never",
        "--model",
        MODEL,
        "--sandbox",
        "workspace-write",
        "-c",
        'model_reasoning_effort="high"',
        "--cd",
        str(project),
        "--output-last-message",
        str(final_path),
        PROMPT,
    ]
    if scenario.get("local_http"):
        command[2:2] = ["-c", "sandbox_workspace_write.network_access=true"]
    started = time.time()
    try:
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        events = completed.stdout
        stderr = completed.stderr
        exit_code: int | str = completed.returncode
    except subprocess.TimeoutExpired as error:
        events = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(events, bytes):
            events = events.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        exit_code = "timeout"
    elapsed = round(time.time() - started, 2)
    (destination / "events.jsonl").write_text(events, encoding="utf-8")
    (destination / "stderr.txt").write_text(stderr, encoding="utf-8")
    (destination / "exit.txt").write_text(f"exit={exit_code}\n", encoding="utf-8")
    (destination / "time.txt").write_text(f"seconds={elapsed}\n", encoding="utf-8")
    load_trace, tool_trace = parse_events(events)
    (destination / "load-trace.txt").write_text(load_trace, encoding="utf-8")
    (destination / "tool-trace.txt").write_text(tool_trace, encoding="utf-8")
    tracked_diff = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--binary", "HEAD"],
        cwd=project,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=project,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=project,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    untracked_diffs = []
    for relative in untracked:
        result = subprocess.run(
            ["git", "diff", "--no-index", "--binary", "/dev/null", relative],
            cwd=project,
            text=True,
            capture_output=True,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        untracked_diffs.append(result.stdout)
    diff = tracked_diff + "".join(untracked_diffs)
    (destination / "project.diff").write_text(diff, encoding="utf-8")
    (destination / "project.status.txt").write_text(status, encoding="utf-8")
    (destination / "final-files.sha256").write_text(
        json.dumps(file_hashes(project), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    snapshot_project(project, destination)
    result = {
        "scenario": name,
        "model": MODEL,
        "reasoning": "high",
        "sandbox": "workspace-write",
        "codex_version": subprocess.run(
            ["codex", "--version"], text=True, capture_output=True, check=True
        ).stdout.strip(),
        "exit": exit_code,
        "seconds": elapsed,
        "loaded": [line for line in load_trace.splitlines() if line],
        "changed": bool(diff),
        "argv": command,
    }
    (destination / "meta.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    shutil.rmtree(project)
    return result


def main() -> int:
    global MODEL, SNAPSHOT
    cases = {}
    for suite in ("test-automation", "agent-eval"):
        cases.update(json.loads((ROOT / f"evals/{suite}/contract-cases.json").read_text()))
    parser = argparse.ArgumentParser(description="Run isolated Skill contract cases; raw evidence stays local.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=540)
    parser.add_argument("scenarios", nargs="*")
    args = parser.parse_args()
    selected = args.scenarios or list(cases)
    if set(selected) - cases.keys():
        parser.error("unknown scenarios: " + ", ".join(sorted(set(selected) - cases.keys())))
    MODEL = args.model
    output = VALIDATION / "attempts" / args.name
    output.mkdir(parents=True, exist_ok=False)
    SNAPSHOT = output / "skill-snapshot"
    shutil.copytree(ROOT / "skills", SNAPSHOT, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {pool.submit(run_scenario, name, cases[name], output, args.timeout): name for name in selected}
        for future in concurrent.futures.as_completed(pending):
            name = pending[future]
            try:
                result = future.result()
                print(f"{name}: exit={result['exit']} seconds={result['seconds']}", flush=True)
                failures += result["exit"] != 0
            except Exception as error:
                destination = output / name
                destination.mkdir(exist_ok=True)
                (destination / "runner-error.txt").write_text(repr(error))
                print(f"{name}: runner_error={error!r}", flush=True)
                failures += 1
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
