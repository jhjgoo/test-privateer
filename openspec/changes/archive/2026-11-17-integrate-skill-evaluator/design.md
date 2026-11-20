# Design

## Decisions

1. 按用户纠正收敛为仓库维护基础设施。保留官方宿主 Skill 与 CLI，删除未发布的包装 Skill 及产品路由；本次不向 `agent-eval` 提炼方法。
2. 复用官方命令和既有 `evals/`，不再写 CLI 包装器。AGENTS.md 引用唯一项目协议，执行者先读取官方 Skill，版本差异以固定版帮助为准。
3. 完整无 LLM Tier 1 是实质 Skill 改动的静态门禁，quick quality score 只作诊断；既有契约测试继续承担包结构及项目契约回归。
4. 行为变化用 Tier 3 验证。优化是否进步用旧版／新版比较；Skill 是否有贡献用带／不带 Skill 比较。共享依赖和真实路由按消费链进入夹具，不能用直接注入替代入口测试。
5. 原始输出留本地；保留版本、配置、轨迹、失败和未运行项。未跑通 Tier 3 就保留体系验收缺口，不声称已完成闭环。
6. 默认 `SCHEMA.author_missing` 与当前 30 个 Skill 的 name/description 约定不匹配。按 Agent Skills 可选 metadata 契约，用项目 policy 将这一条降为 MEDIUM 提示；其余默认严重级别和检查不变。真实 validator 反例测试验证缺必填、错误名称、非法 YAML 和不合法作者仍失败。
7. 首批选 `agent-eval` 的三个历史案例改编，加一例证据充分的正常对照和一例普通翻译负例。5 例为接线集合，不伪造历史用户请求；模型 Judge 尚未校准时明确保留该缺口。
8. 复用官方 `validate-grader` 已标注正反例检查评分链路，显式设置失败率阈值。本轮发现错误答案的关键指标失败但 overall 通过；保留官方输出，项目验收不允许总分抵消关键结果失败。该汇总门禁未通过校准前，不把 CLI 成功当作 Skill 验收通过。

## Tier 3 执行方式修订

用户提供已有网关并授权选择较小方案，采用未修改的官方 Tier 3。此前子代理方案只做过源码调查和设计，没有实现；不继续新增宿主桥接或评分后端。

- 固定 SkillEvaluator 0.9.0，复用官方数据集校验、Harbor、两组执行、Judge、计分与报告。
- 使用 OpenAI-compatible provider，OpenCode 需 Chat Completions，Codex 需 Responses；agent 与 Judge 显式指定模型，不依赖默认值。
- 密钥只通过进程环境传入，不写入可复用配置或报告。先做宿主真实推理、工具调用及容器访问检查；容器内 localhost 不代表宿主，必须验证实际使用的网关地址。
- 一个案例 × 一次 × 一个 Agent × 两组 = 2 个逻辑尝试，另有 Judge 调用。检查真实加载和判读后，再运行五例共 10 个逻辑尝试。
- 保留运行错误、未评分、轨迹缺失和失败结果；同一 Judge 的已标注正反样本检查不替代实际案例评测。

实际 Docker 冷启动两组均超过默认 600 秒；扩大超时后仍在依赖版本回退，停止该次重试并保留中断状态。现有 Codex CLI 0.169.0、官方 local 前置检查与网关 Responses 推理均通过，因此当前可信 `agent-eval` 改用官方 experimental local 后端。它使用每次尝试的独立 HOME 与 macOS Seatbelt，不复用用户 CLI 登录；不宣称与 Docker 等强隔离，也不将其默认用于不可信 Skill。更换后端与 Agent 后重新跑完整双组，不与 Docker 单臂混算。

最小验收仍为官方报告与真实轨迹闭环。隔离单 Skill 的文字任务不能证明主入口自动路由、真实文件维护或全包行为覆盖。

## Codex CLI 模型选择

Codex CLI 行为评测默认同时验证 GPT-5.6-SOL 和 GLM-5.3；维护者明确追加其他模型时，新模型与默认组一同运行。当前网关 ID 为 `auto/gpt-5.6-sol`、`auto/glm-5.3`；两者已分别通过 Responses 工具调用探针和官方 local doctor。每个模型在独立结果目录运行同一快照、同一 `environment-noise` 案例的完整双组，共 4 个逻辑尝试，Judge 别名固定为 `group/j.a.r.v.i.s`。不修改官方运行器或产品 Skill。

这轮判断两个配置能否接入验证体系，不选出“更强模型”。网关回显路由别名，底层模型版本未确认；Codex 对不同模型提供的系统提示和工具表示也有差异。单次接线结果不支持模型排名、成本比较或 Skill 优化结论。

## Validation

核对 `skills/`、用户文档、原契约测试相对 HEAD 无本 change 差异；运行既有包检查和 OpenSpec strict。用已有 `agent-eval` 做静态工具接线探查，结果仅证明扫描路径及当前发现，不触发本次产品内容修订。

## Risks

官方 Skill 与 CLI 分别演进，必须记录来源和哈希。扫描器下载、模型凭据和沙箱可能阻塞；静态基线可能存在真实失败。保留其状态，不为了通过而跳过检查或改变产品提示词。项目规则不是自动 CI，当前依赖维护者执行。
