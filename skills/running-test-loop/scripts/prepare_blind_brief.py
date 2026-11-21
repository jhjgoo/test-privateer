import argparse
import os
import shlex
from pathlib import Path


def single_line(value):
    if not value.strip() or value.splitlines() != [value]:
        raise argparse.ArgumentTypeError("字段必须是非空单行，只填写本轮已确认事实。")
    return value


def main():
    parser = argparse.ArgumentParser(
        description="只生成盲测任务包，不执行测试。参数只填本轮事实，不补写共同规则。",
    )
    for field in ("run-id", "wave-id", "target-version", "view", "task", "evidence-dir"):
        parser.add_argument("--" + field, required=True, type=single_line)
    parser.add_argument(
        "--synthesizer", required=True, type=single_line,
        help="接收隔离 handoff 的唯一合成者身份，不是执行本任务的测试者。",
    )
    parser.add_argument("--exclude", action="append", default=[], type=single_line)
    parser.add_argument("--prerequisite", action="append", default=[], type=single_line)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--worker-contract",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "blind-test-worker.md",
        help="接收者可访问的共同契约；默认使用本 Skill 中的契约。",
    )
    entry = parser.add_mutually_exclusive_group(required=True)
    entry.add_argument("--entry", type=single_line, help="获准的页面、接口或其他非命令入口。")
    entry.add_argument(
        "--command", nargs=argparse.REMAINDER, type=single_line,
        help="最后填写获准入口的 argv；只记录，不运行。",
    )
    args = parser.parse_args()
    if args.command == []:
        parser.error("--command 需要至少一个命令参数。")
    contract = args.worker_contract.resolve()
    if not contract.is_file():
        parser.error("共同契约不可访问；先提供可读取的 --worker-contract。")
    contract.read_text(encoding="utf-8")
    output = args.output.absolute()
    if output.is_symlink() or not output.resolve().is_relative_to(Path.cwd().resolve()):
        parser.error("--output 必须位于当前工作区内，且不能是符号链接。")
    output = output.resolve()
    relative_contract = os.path.relpath(contract, output.parent.resolve())
    content = "\n".join([
        f"先读取相对本任务文件所在目录的 `{relative_contract}`，再执行本任务。",
        f"Run ID / wave ID：{args.run_id} / {args.wave_id}",
        f"目标版本：{args.target_version}",
        f"质量视角：{args.view}",
        f"业务契约：{args.task}",
        f"获准入口：{args.entry or shlex.join(args.command)}",
        *(f"专有前置：{value}" for value in args.prerequisite),
        f"覆盖排除项：{'；'.join(args.exclude) if args.exclude else '无'}",
        f"隔离输出：{args.evidence_dir}",
        f"唯一合成者：{args.synthesizer}",
        "",
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open("x", encoding="utf-8") as handle:
            handle.write(content)
    except FileExistsError:
        if output.read_text(encoding="utf-8") != content:
            parser.error("目标已存在且内容不同；保留原文件，请选择新的输出路径。")
    print(output)


if __name__ == "__main__":
    main()
