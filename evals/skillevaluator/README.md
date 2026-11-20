# 本仓库的 SkillEvaluator 验证协议

本协议供 Test Privateer 维护者开发、优化本仓库 Skill 使用。入口为根 `AGENTS.md`；操作方法由宿主已安装的 NVIDIA 官方 `skillevaluator` Skill 提供。本目录不是可分发 Skill，不向使用方项目写配置。客户选用框架时由 `prompt-eval` 的[接入参考](../../skills/prompt-eval/references/skillevaluator-integration.md)约束，不继承本协议的模型矩阵或策略。

Tier 3 使用未修改的官方 Harbor 与维护者已有兼容网关。可信仓库 Skill 可使用官方 experimental local 后端，需更强隔离时使用 Docker。目标与验收见 [变更设计](../../openspec/changes/archive/2026-11-17-integrate-skill-evaluator/design.md#tier-3-执行方式修订)；不维护自定义子代理执行或评分后端。

官方来源：<https://github.com/NVIDIA/SkillEvaluator>。CLI 固定为 `0.9.0`，Python 使用 `3.13`。安装或升级官方 Skill 时记录来源 revision；运行时保存其文件哈希，不把官方 Skill 的版本号当作 CLI 版本号。上游 main 的新命令不一定适用于固定版，以本地 `--help` 为准。

## 1. 确定本轮需要的证据

| 改动或主张 | 必须执行 |
| --- | --- |
| 新增或实质修改 Skill、共享参考、模板 | 既有契约测试；沿消费关系对受影响 Skill 执行完整无 LLM Tier 1 |
| 路由、加载、文件／工具操作等行为变化 | 上述检查，加 SkillEvaluator Tier 3 的目标失败场景、相邻正常场景及必要负例；核对实际读取／动作 |
| 优化现有 Skill，声称优于旧版 | 同一固定数据集、模型、宿主、工具、初始状态、权限、预算及判据下比较旧版与新版 |
| 声称 Skill 相比模型自身有贡献 | 另设无 Skill 组；结果判据允许无 Skill 组做到，不以调用 Skill 为正确答案 |
| 重复指导或多 Skill 重叠是本轮风险 | 按官方入口运行 Tier 2，记录 embedding/provider 配置 |
| 仅维护仓库规则、验证文档 | 检查入口引用和命令可用性；无产品 Skill 变化时不虚构效果比较 |

`quality-check` 是快速诊断，不能替代完整 Tier 1。Tier 1 通过也不能证明行为有效。Tier 2 不是所有改动的强制前置；Tier 3 不能由静态分数替代。当前没有自动执行钩子或 CI 门禁，维护者必须主动执行并在 change 中交付证据。

## 2. 安装和静态门禁

使用宿主安装能力安装官方 `NVIDIA/SkillEvaluator` 的 `skills/skillevaluator`，实际读取其 `SKILL.md`。不复制到本仓库 `skills/`。CLI 单独安装：

```sh
uv tool install --python 3.13 'skillevaluator[all]==0.9.0'
skillevaluator --version
```

已有其他版本时先说明差异再按当前授权处理，不静默升级。已获本轮安装授权不重复询问。执行前核对官方 Skill；缺失时报告缺口，不能用本协议冒充官方操作说明。

### 本仓库静态策略

所有 30 个现有 Skill 使用 `name`、`description` 的扁平 frontmatter；包检查器 `scripts/check_skill_package.py` 将这两项作为必填。作者归属和版本由仓库历史维护。[Agent Skills 格式规范](https://agentskills.io/specification) 也将 `metadata` 定为可选字段。SkillEvaluator 0.9.0 默认策略的作者必填要求属于额外治理规则。

[policy.yaml](policy.yaml) 在默认策略上仅将 `SCHEMA.author_missing` 从 HIGH 改为 MEDIUM。缺作者仍出现在报告中；不伪造姓名或邮箱，不修改发布 Skill。已有作者值不合法仍阻断，必填字段、名称与目录匹配、安全、许可证、密钥和依赖扫描均保持默认。中文标题、触发词等启发式告警保留人工审查；本次不改质量分权重、阈值或英文规则。

适配是选择符合项目约定的治理规则，不是证明 Skill 质量改善。报告必须保留 `profile: test-privateer` 和 policy digest，不能将项目策略通过说成上游默认策略通过。升级 CLI 时重新运行反例检查：

```sh
uv run --no-project --python 3.13 --with 'skillevaluator==0.9.0' \
  python -m unittest discover -s evals/skillevaluator -p test_policy.py -v
```

这些测试调用真实 schema validator，覆盖无作者可用、缺必填字段、非法 YAML、名称错误、作者格式错误和其他默认严重级别保持，并检查现有全部 Skill 的 schema。它们不替代安全扫描或 Tier 3。

下例在仓库根目录运行。将 `skill_dir` 换为受影响 Skill；每次用新目录，保留失败运行。默认不调用 LLM，但静态门禁可能下载官方扫描器。

```sh
(
skill_dir=skills/agent-eval
mkdir -p .local/validation/skillevaluator
run_dir=$(mktemp -d .local/validation/skillevaluator/run.XXXXXX)
uvx --python 3.13 --from 'skillevaluator[all]==0.9.0' \
  skillevaluator tier1 "$skill_dir" --no-llm \
  --profile default --policy evals/skillevaluator/policy.yaml \
  -r json,markdown -o "$run_dir" > "$run_dir/console.log" 2>&1
eval_exit=$?
printf '%s\n' "$eval_exit" > "$run_dir/exit-code.txt"
exit "$eval_exit"
)
```

检查退出码与 JSON 中各项结果，不仅看字母等级；示例在子 shell 中返回门禁状态，不能将最后一个写日志命令的成功当作门禁成功。非零、缺扫描器、被跳过项或 `INCOMPLETE` 必须说明影响。报告区分“本轮静态门禁”和上游“publication eligibility”，后者未完成不自动说明静态扫描失败，静态通过也不等于可发布。安全失败不得被平均分抵消；中文标题启发式告警逐条审查，不为提分改成英文或跳过检查。

## 3. 准备行为评测

复用 `evals/<相关套件>/` 的真实请求、夹具和外部判据。通用隔离／盲评原则见 [Agent 行为协议](../agent-eval/README.md)。对新领域缺少真实需求时收集用户任务；拟定案例明确标为草案，经审阅后冻结，不让 Skill 自己生成的单例成为验收集。

首批接线案例见 [agent-eval/evals.json](agent-eval/evals.json)，来源、正常／负例及正反判据见 [EVAL.md](agent-eval/EVAL.md)。共 5 例，其中 4 个评估任务、1 个非触发请求；固定版工具将其标为 provisional，未满足上游 10 例的数据集充分性要求。只用于链路验收，不据此申请发布认证。

- 在 `.local/validation/skillevaluator/<run-id>/` 中暂存旧版与新版完整快照；记录 commit、未提交 diff 和文件哈希，不能只复制 `SKILL.md` 而漏掉引用。
- 将经审阅的数据集暂存为对应快照内的 `evals/evals.json`；目录名与 Skill frontmatter 的 `name` 一致。可复用输入与判据仍在仓库 `evals/<相关套件>/` 跟踪，运行输出不提交。
- 真实入口或多 Skill 路由的测试必须保留所需包布局和依赖，按官方 group 模式配置。隔离单 Skill 的直接加载结果不能证明 `test-privateer` 能自动路由到它。
- 操作类任务使用临时文件、夹具或 sidecar，核对前后差异与无关内容保持。只生成建议的案例只支持建议质量结论。
- 评分器先用独立已标注的正反样本检查区分能力；确定性检查优先。候选不能看到隐藏判据、比较标签或历史答案。

先检查运行条件和数据格式：

```sh
skillevaluator doctor --env-mode docker
skillevaluator tier3 validate /path/to/staged/skills/skill-name --strict
```

不要使用会自动生成 starter case 的便捷流程来替代数据集审阅。记录 provider、agent/model、judge/model、attempts、sandbox 和预算；只检查凭据是否存在，不打印值、不扫描私有配置文件找密钥。不从当前交互 Agent 的登录状态推断 Tier 3 可用。

### 评分器接线检查

先复用固定版随包的已标注正反例，不另写评分器。以下只检查两个参考案例各一次，不是完整评分器认证，也不能证明中文领域判据的可靠性：

```sh
skillevaluator tier3 validate-grader --check-suite --json
mkdir -p .local/validation/skillevaluator
grader_dir=$(mktemp -d .local/validation/skillevaluator/grader.XXXXXX)
skillevaluator tier3 validate-grader \
  --case arithmetic --case wrong-answer --repeats 1 \
  --max-false-pass-rate 0 --max-false-fail-rate 0 \
  --max-unjudgeable-rate 0 \
  -o "$grader_dir" --json
```

检查 `overall` 和各指标的 expected/observed、错误及未评分项。2026-11-17 的网关接线发现：错误答案的 accuracy 和 goal_accuracy 已识别失败，但 overall 仍通过。未指定失败率阈值的命令还可能退出 0。因此该配置的汇总通过不能独立作为项目门禁；关键业务结果、必需 assertions 或安全判据失败时，项目验收不得被总分抵消。先保留反例及其影响，不能为通过而修改已冻结的标签或降低判据。只有评分器区分能力与实际任务判据都已核验，才能声明行为验收通过。

首批案例按以下方式暂存，不写回发布包。`staged_skill` 供下一节命令使用；每次新建目录：

```sh
mkdir -p .local/validation/skillevaluator
stage_root=$(mktemp -d .local/validation/skillevaluator/stage.XXXXXX)
cp -R skills/agent-eval "$stage_root/agent-eval"
staged_skill="$PWD/$stage_root/agent-eval"
mkdir "$staged_skill/evals"
cp evals/skillevaluator/agent-eval/evals.json \
  evals/skillevaluator/agent-eval/config.yml \
  evals/skillevaluator/agent-eval/EVAL.md "$staged_skill/evals/"
skillevaluator tier3 validate "$staged_skill" --strict --json
```

## 4. 运行与比较

运行前读取官方 Skill 的 Tier 3 指南，确认凭据、模型、沙箱和费用在当前授权内。一次最小冒烟示例（单 agent、单案例、每组一次，共两个逻辑尝试，另有 judge 调用）：

```sh
skillevaluator tier3 evaluate "$staged_skill" \
  --env-mode docker --max-cases 1 --n-attempts 1 \
  --max-attempts-total 2 --harbor-keep-jobs \
  --results-dir "$stage_root/smoke-results"
```

上述命令还需补入已选的单个 agent 与模型参数。受支持 provider 和配置方式以官方 Skill 的 `references/providers.md` 为准；例如已有 OpenAI-compatible 网关时由操作者设置 `SKILL_EVAL_LLM_PROVIDER`、`SKILL_EVAL_LLM_BASE_URL`、`SKILL_EVAL_LLM_API_KEY`，并明确 agent 与 judge 的模型 ID。只将非敏感模型配置和凭据存在性写入清单，不把 key 放进 config.yml、日志或聊天。

对可信的仓库 Skill，已有 Codex CLI 且网关支持 Responses API 时，可以改用官方 local 模式，省去 Docker 镜像构建：

```sh
agent_model=auto/gpt-5.6-sol
skillevaluator doctor --env-mode local -a codex \
  --agent-model "codex=$agent_model" --verify-models
skillevaluator tier3 evaluate "$staged_skill" \
  -a codex --agent-model "codex=$agent_model" \
  --env-mode local --max-cases 1 --n-attempts 1 \
  --max-attempts-total 2 --harbor-keep-jobs \
  --results-dir "$stage_root/local-smoke-results"
```

Codex CLI 行为评测默认同时验证 GPT-5.6-SOL 和 GLM-5.3；维护者明确追加其他模型时，新模型与这两个默认模型一同运行，不替换默认组。2026-11-17 的现有网关分别提供 `auto/gpt-5.6-sol`、`auto/glm-5.3`；其他网关先核对实际 ID。每个模型分别运行完整双组并使用独立结果目录，不能只替换模型后复用旧基线。Judge 单独通过 `LLM_JUDGE_MODEL` 固定，本轮沿用 `group/j.a.r.v.i.s`，不随 `agent_model` 切换。路由别名不等于底层模型版本固定；这两个模型是本项目维护验证矩阵，不是所有使用方的依赖。

该后端使用每次尝试的独立 HOME；macOS 依靠 Seatbelt，隔离弱于 Docker，并默认可访问网络。只运行已审查的可信 Skill，不复用个人 CLI 登录；凭据仍由环境提供。Agent、后端或预算改变时重跑完整双组，不与之前的单臂结果拼接。

本地网关先在宿主验证真实 Chat Completions 与工具调用，再检查容器端地址；Docker 中的 `127.0.0.1` 不代表宿主。本机网关可经 `host.docker.internal` 到达，但宿主 catalog 探查与容器实际执行必须分别记录，catalog 警告不能当作推理失败或成功。不要为连接网关默认开启 host network 或修改全局 DNS。若模型 ID 是路由别名，保留实际可取得的上游模型及版本；无法确认底层模型固定时，只作接线证据，不声称同模型版本的优化比较。

冒烟只证明运行链路。正式评测按冻结的案例和尝试数运行，记录完整矩阵与预算，不把 `--max-cases 1` 冒烟当作发布证据。旧版、新版分别运行；官方 `--compare-to`、`--reuse-baseline` 仅在配置和快照可比时使用。

首次镜像构建可能超过默认环境启动时限。保留 `EnvironmentStartTimeoutError` 为环境错误；需要时使用官方 `--timeout-multiplier 3` 在新目录重跑完整双组。该参数也会扩大 Agent 等阶段的时间预算，必须记录，不能将不同预算的成功单臂拼成同条件对照。

`tier3` 的进程退出码不能单独判定效果通过；同时读取 verdict、各维度结果、激活轨迹和运行完整性。`pass@k` 只表示多次中至少成功一次，不代表每次可靠。未确认激活不能解释为 Skill 贡献；两版都通过不证明改善；对文件的人工修订不计入生成效果。

## 5. 交付与保留状态

原始日志、JSON 报告、轨迹和快照放 `.local/validation/` 或 `evals/<suite>/runs/`。change 只写命令、配置、验收结论、范围和剩余项，不提交原始记录。至少记录：

```text
目标及主张：
受影响 Skill／消费关系：
旧版／新版 revision、diff 和快照哈希：
官方 Skill 来源与哈希、CLI/Python 版本：
数据集／夹具／判据版本与审阅状态：
provider、模型、judge、宿主、沙箱、权限和预算：
命令、退出码、报告目录：
静态门禁／行为回归／旧新比较／无 Skill 贡献：
实际激活与文件／工具动作证据：
行为失败／环境错误／无效案例／评分器错误：
未运行项、受阻原因、解除动作：
支持的结论及不支持的结论：
```

缺凭据、沙箱、数据集或实际轨迹时保留 `未完成／受阻／未知`，不降低必需证据。验证体系的文档与静态入口可分阶段交付；首轮真实 Tier 3 未跑通前，不宣称行为评测链路已验收。同步规格和归档仍需用户明确确认。
