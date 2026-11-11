#!/usr/bin/env python3
"""Use the existing recorder with Setup handoff project inputs."""
import argparse
import concurrent.futures
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

from handoff_cases import CASES

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("contract_recorder", ROOT / "evals/agent-eval/run_contract_cases.py")
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)
original_prepare = recorder.prepare_project


def prepare_project(case):
    project = original_prepare(case)
    if case.get("seed_evidence"):
        subprocess.run([sys.executable, "tools/check_price.py"], cwd=project, check=True, capture_output=True, timeout=30)
        subprocess.run(["git", "add", "evidence"], cwd=project, check=True)
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "record existing check"], cwd=project, check=True)
    if case.get("workstation_offline"):
        (project / "runtime").mkdir()
        (project / "runtime/operator.offline").write_text("operator-owned temporary maintenance\n")
        subprocess.run(["git", "add", "runtime/operator.offline"], cwd=project, check=True)
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "record workstation maintenance"], cwd=project, check=True)
    return project


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("scenarios", nargs="*")
    args = parser.parse_args()
    selected = args.scenarios or list(CASES)
    if set(selected) - CASES.keys():
        parser.error("unknown scenario")
    output = ROOT / ".local/validation/setup-handoff/attempts" / args.name
    output.mkdir(parents=True, exist_ok=False)
    recorder.SNAPSHOT = output / "skill-snapshot"
    shutil.copytree(ROOT / "skills", recorder.SNAPSHOT, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    recorder.prepare_project = prepare_project
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(recorder.run_scenario, name, CASES[name], output, args.timeout): name for name in selected}
        for future in concurrent.futures.as_completed(jobs):
            name = jobs[future]
            try:
                result = future.result()
                print(f"{name}: exit={result['exit']} seconds={result['seconds']}", flush=True)
                failures += result["exit"] != 0
            except Exception as error:
                (output / name).mkdir(exist_ok=True)
                (output / name / "runner-error.txt").write_text(repr(error))
                print(f"{name}: runner_error={error!r}", flush=True)
                failures += 1
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
