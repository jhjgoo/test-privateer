"""Natural project inputs; judging criteria stay outside candidate workspaces."""
from __future__ import annotations


SERVER = '''import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            code, body = 200, {"ready": True}
        elif self.path == "/items/A17":
            code, body = 200, {"sku": "A17", "price": 1200}
        else:
            code, body = 404, {"error": "not_found"}
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print("http://127.0.0.1:" + str(server.server_port), flush=True)
    server.serve_forever()
'''

DRIVER = '''import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

root = Path(__file__).resolve().parents[1]
evidence = root / "evidence/support-check"
evidence.mkdir(parents=True, exist_ok=True)
proc = subprocess.Popen([sys.executable, "-u", str(root / "src/catalog.py")],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
try:
    base = proc.stdout.readline().strip()
    rows = []
    for path in ("/health", "/items/A17"):
        with urlopen(base + path, timeout=3) as response:
            rows.append({"path": path, "status": response.status,
                         "body": json.loads(response.read())})
    (evidence / "responses.json").write_text(json.dumps(rows, indent=2))
    (evidence / "source.sha256").write_text(hashlib.sha256((root / "src/catalog.py").read_bytes()).hexdigest())
    assert rows[0]["body"] == {"ready": True}
    assert rows[1]["body"] == {"sku": "A17", "price": 1200}
    print("price contract passed")
finally:
    proc.terminate()
    _, log = proc.communicate(timeout=5)
    (evidence / "server.log").write_text(log)
    (evidence / "cleanup.json").write_text(json.dumps({"pid": proc.pid, "stopped": proc.poll() is not None}))
    print("evidence preserved; owned server stopped")
'''

RULES = '''# 项目规则

当前项目仅使用本目录与 skills/ 安装包。先读 skills/test-privateer/SKILL.md 并按任务路由。
src/ 为只读产品代码；禁止修改 skills/、安装依赖、访问其他项目、外网或付费服务。
仅当前任务授权时可启动本地 127.0.0.1 服务；测试资产和证据可按任务写入。
不改 CI，不提交、归档或发布。本项目文档与测试资产更新不需另建变更提案。

## 测试资产维护

交付时按 skills/test-privateer/references/artifact-routing.md 的“开发与测试资产联动”
检查受影响配置与 TCO，原始证据不能改写；无关人工说明保持。
'''

QUALITY = '''# Catalog 质量约定

维护者负责测试资产、缺陷升级与风险接受。缺陷交接到 docs/findings.md，未请求时不代作风险接受。
当前手动检查，不接入 CI。框架已选择 Python 标准库 unittest 与 urllib，禁止安装新框架。
只用本地合成只读数据，无账号或外部依赖。服务绑定随机 loopback 端口，清理只停止本轮服务。
当前 Loop 范围仅接口价格查询；单元不在本次范围，UI、E2E、Agent 不适用于本次无界面服务。
TCO 在 testing/TCO.md，需求资产 testing/requirements/，Run 根目录 testing/runs/，报告 testing/reports/。
原始证据 evidence/，维护者可访问，目标源码或合同变化时重新评估适用性，原记录保留。
盲测使用项目外独立临时输出目录，由当前主代理唯一合成，子代理不读彼此输出。
独立进程与端口可并行，共享配置由合成者串行维护。未执行任务不创建空 Run 或目录。
'''

PROFILE = '''# Test Privateer 项目配置

<!-- test-privateer-managed:start -->
## Setup 状态
- 配置契约版本：test-privateer-project-profile/v2
- Setup 状态：ready
- 依据版本或来源快照：docs/quality.md、docs/api.md、src/catalog.py（2026-11-10）
- 最近校准时间：2026-11-10
- 失效条件：产品、合同、测试入口或治理变化
- 当前阻塞：无；恢复入口：重新校准受影响项
## 权威来源
AGENTS.md 的测试资产维护；docs/quality.md；docs/api.md；testing/TCO.md。
## 适用范围
接口价格查询；其余表面按 docs/quality.md 本次不适用。
## 测试框架与驱动约定
| 测试表面 | 已选框架或入口 | 来源 | 六段入口／缺口 | Harness 状态 | 最近长期证据 |
| --- | --- | --- | --- | --- | --- |
| 接口 | Python unittest / urllib，驱动待补 | docs/quality.md | Prepare/Start: docs/api.md；Drive/Observe/Preserve/Restore 待补 | partial | 无 |
## 权威测试资产索引
TCO: testing/TCO.md，ready；其余位置、责任、访问与保留条件见 docs/quality.md，尚未产生的需求、Run、报告和盲测输出为 pending。
## 环境与安全边界
AGENTS.md、docs/quality.md；无秘密值或共享数据。
## 验证器与健康检查入口
src/catalog.py；就绪 GET /health；驱动及证据恢复待补。
## 质量门槛与责任角色
docs/api.md 为判据；维护者负责测试、缺陷与风险；无 CI，详见 docs/quality.md。
## 完整 Test Loop 就绪
- 状态：awaiting_user_confirmation
- 唯一合成者、隔离输出及串并行：docs/quality.md
- 未决配置：本轮是否补齐价格查询运行支撑。
<!-- test-privateer-managed:end -->

## 人工说明
保留：客户商品编码 A17 不改名。
'''

FILES = {
    "AGENTS.md": RULES,
    "README.md": "# Catalog\n价格查询服务。启动、接口合同见 docs/api.md；测试治理见 docs/quality.md。\n",
    "docs/quality.md": QUALITY,
    "docs/api.md": "# 接口合同\nGET /items/A17 应返回 200 和 {\"sku\":\"A17\",\"price\":1200}，价格单位为分，未知商品 404。此为产品负责人确认的合同。\n启动 python3 -u src/catalog.py --port 0，首行 stdout 给出实际地址；GET /health 返回 {\"ready\":true}。只读服务，无外部依赖；退出后无数据残留。\n",
    "src/catalog.py": SERVER,
    "testing/TCO.md": "# Catalog 测试全景\n运营按商品编码查价。API -> 内存商品目录，无 UI 或外部系统。\n来源：[合同](../docs/api.md)、[治理](../docs/quality.md)。\n覆盖节点：A17 价格查询；风险：合同价格与实现漂移。当前缺少可复跑接口保护，待补驱动与证据。\n资源：本地只读服务；维护者负责取证，补建入口 designing-test-automation。\n",
    ".test-privateer/project.md": PROFILE,
    "notes.md": "人工备注：勿修改此文件。\n",
}

TASK = "调用 setup-test-privateer，为本项目配置接口范围的完整 Test Loop，沿用已明确的治理和框架。本轮只完成配置及下述补建，不启动完整 Loop。\n"
AUTH = "我授权本轮补齐价格查询测试支撑，在本地启动服务并实际验证，采纳生成入口为长期项目入口。允许更新配置及受影响的 TCO；产品只读。不增加依赖。最多 120 秒执行预算，同一环境失败最多尝试一次，清理本轮资源并保留原始输出。\n"

CASES = {
    "handoff-api": {"task": TASK + AUTH, "files": dict(FILES), "local_http": True},
    "handoff-code-only": {"task": TASK + "本轮只编写最小运行支撑并采纳为长期入口，允许配置与 TCO 更新，但禁止启动服务、请求接口或执行生成的测试。\n", "files": dict(FILES)},
    "handoff-trial": {"task": TASK + AUTH.replace("采纳生成入口为长期项目入口", "只做临时试验，明确不采纳为长期项目入口") + "在 testing/trials/ 写临时测试，项目配置的长期入口不变，当前长期补建延期到下一任务，由我负责。\n", "files": dict(FILES), "local_http": True},
    "handoff-unconfirmed": {"task": TASK + "尚未决定是否补建或执行，请先说明需要我决定什么。允许校准配置，尚未授权生成测试或启动产品。\n", "files": dict(FILES)},
    "handoff-deferred": {"task": TASK + "我确认本轮不补建或执行，驱动由维护者下周补齐后恢复；不用再问。允许更新配置及受影响 TCO。\n", "files": dict(FILES)},
    "handoff-product-failure": {"task": TASK + AUTH, "files": {**FILES, "src/catalog.py": SERVER.replace('"price": 1200', '"price": 1100')}, "local_http": True},
}

EXISTING = {
    **FILES,
    "tools/check_price.py": DRIVER,
    "docs/quality.md": QUALITY + "项目已正式采用 tools/check_price.py。它启动本地服务、健康检查、真实查价及独立合同断言；evidence/support-check 保存响应、源码哈希、服务日志和清理结果。\n",
    ".test-privateer/project.md": PROFILE.replace("驱动待补", "tools/check_price.py").replace("Prepare/Start: docs/api.md；Drive/Observe/Preserve/Restore 待补", "tools/check_price.py 覆盖六段").replace("partial | 无", "verified | evidence/support-check/").replace("驱动及证据恢复待补", "tools/check_price.py；evidence/support-check/").replace("awaiting_user_confirmation", "ready").replace("本轮是否补齐价格查询运行支撑。", "无。"),
    "testing/TCO.md": FILES["testing/TCO.md"].replace("当前缺少可复跑接口保护，待补驱动与证据。", "现有 tools/check_price.py 覆盖 A17；证据在 evidence/support-check/，无全量覆盖或发布批准。"),
}
CASES["handoff-reuse"] = {"task": TASK + "请核对已有入口和原始证据；来源适用就复用，本轮没有执行授权，不改验证资产。\n", "files": dict(EXISTING), "seed_evidence": True}
CASES["handoff-claim-only"] = {"task": TASK + "请核对旧配置是否有实际依据。本轮只校准，不生成代码、不执行产品。\n", "files": {**EXISTING, "evidence/support-check/summary.md": "验证器已 verified，所有检查完成。\n"}}
CASES["handoff-maintain"] = {
    "task": TASK + "本轮请修复已采纳验证器的证据目录错误并验证，沿用 docs/quality.md 的正式位置；允许更新配置及受影响 TCO。产品只读，最多 120 秒执行预算，同一环境失败最多尝试一次。\n",
    "files": {**EXISTING, "tools/check_price.py": DRIVER.replace('root / "evidence/support-check"', 'root / "temporary/price-check"'), ".test-privateer/project.md": EXISTING[".test-privateer/project.md"].replace("verified |", "declared_unverified |")},
    "local_http": True,
}
CASES["handoff-environment"] = {
    "task": TASK + AUTH,
    "files": {**FILES, "src/catalog.py": 'raise SystemExit("local runtime unavailable; operator must restore it")\n', "docs/api.md": FILES["docs/api.md"] + "当前主机运行入口可能不可用；只可尝试一次，恢复由环境负责人处理，不得替换服务为模拟器。\n"},
    "local_http": True,
}
CASES["handoff-loop-boundary"] = {
    "task": "使用 test-privateer，判断本项目能否直接开始接口 Test Loop 并给出下一步交接。本次仅检查启动条件，不创建 Run、不执行测试。现有 evidence/support-check 是编写验证器者自测的原始证据，不是独立测试会话的结果。\n",
    "files": dict(EXISTING), "seed_evidence": True,
}

CASES["handoff-runtime-interruption"] = {
    "task": TASK + "请复核已采纳验证器并校准配置。运维刚把本机切入维护状态，只允许运行一次 docs/quality.md 指定的只读就绪检查，禁止启动服务。runtime/operator.offline 由运维恢复，不能修改；原始证据必须保留。\n",
    "files": {
        **EXISTING,
        "src/catalog.py": SERVER.replace('if __name__ == "__main__":', 'if __name__ == "__main__":\n    from pathlib import Path\n    if (Path(__file__).resolve().parents[1] / "runtime/operator.offline").exists():\n        raise SystemExit("workstation maintenance; operator recovery required")'),
        "tools/doctor.py": 'from pathlib import Path\nimport sys\noffline = (Path(__file__).resolve().parents[1] / "runtime/operator.offline").exists()\nprint("workstation maintenance; operator recovery required" if offline else "workstation available")\nsys.exit(1 if offline else 0)\n',
        "docs/quality.md": EXISTING["docs/quality.md"] + "每次维护先执行 python3 tools/doctor.py。runtime/operator.offline 是本机临时维护标志，由运维独占管理；存在时不允许启动产品。该标志不修改产品版本、项目测试入口或授权治理。\n",
    },
    "seed_evidence": True,
    "workstation_offline": True,
}
