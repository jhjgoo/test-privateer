# Tasks

- [x] 1. 撤回发布包新增 Skill、路由及相关用户文档与测试改动。
- [x] 2. 复用官方宿主 Skill，固定 CLI 版本并建立项目验证协议。
- [x] 3. 将协议接入 AGENTS.md、项目背景及 repository-workflow delta。
- [x] 4. 实际运行静态门禁与就绪探查，保留原始输出和真实状态。
- [x] 5. 运行包契约、OpenSpec strict、差异与产品边界检查。
- [x] 6. 用经审阅的代表案例跑通 Tier 3，核验实际加载、结果与失败分类。
- [x] 6.1 明确元数据适配边界并建立真实 validator 正反例测试。
- [x] 6.2 保存代表案例、来源及审阅结论，完成 strict 数据契约校验。
- [x] 6.3 使用项目 policy 运行完整 Tier 1，检查未削弱无关门禁。
- [x] 6.4 验证现有网关的真实推理、工具调用、Docker 连通性及官方 provider/agent 配置。
- [x] 6.5 用一个案例的两组运行验证官方运行器、真实加载、计分和报告，保留执行及 Judge 错误。
- [x] 6.6 核验激活轨迹与判定；完整 5 例、领域 Judge 校准和旧新版效果比较转为后续维护动作，不作为本阶段接线验收阻塞，后续运行仍保留失败和未评分项。

第 6 项属于验证体系验收，代表案例链路已跑通。发布包能力提炼已按用户要求暂停，不在本阶段扩展。完整 5 例、领域 Judge 校准和旧新版效果比较由验证协议约束后续维护执行。

## 2026-11-17 验证

- `skillevaluator --version`：0.9.0。官方宿主 Skill 可读，文件哈希与受测文件哈希已留本地。
- `skillevaluator tier1 skills/agent-eval --no-llm -r json,markdown -o <本地报告目录>`：退出 1。10 类静态检查执行完成；默认 schema 策略报 `author_missing` HIGH，门禁失败。质量分通过不抵消此失败。SkillSpector 2.13.3 和 Gitleaks 8.30.0 已自动安装并通过校验和验证。
- `skillevaluator doctor --env-mode docker`：退出 1，Docker prerequisite pass，但 provider 未配置；尚未确认 Harbor agent/model 可运行。
- `python3 -m unittest tests.test_eval_skills_contract tests.test_skill_package_integrity -v`：20 项通过；`openspec validate integrate-skill-evaluator --strict --no-interactive` 与 `git diff --check` 通过。
- `git diff --exit-code -- skills README.md docs tests`：退出 0；包仍为 30 个 Skill，无本 change 的产品路由、用户文档或契约测试改动。
- 原始证据位于 `.local/validation/skillevaluator-integration/20261117/`，包含报告、控制台日志、退出码和 provenance；已确认被 Git 忽略。

## 2026-11-17 策略适配与案例准备

- 项目 `policy.yaml` 仅将 `SCHEMA.author_missing` 从 HIGH 降为 MEDIUM，保留其报告。必填 name/description、非法 YAML、名称不符和不合法作者仍被真实 schema validator 拦截。5 项策略测试通过，含全部 30 个现有 Skill 的 schema 检查。
- 完整 `tier1 skills/agent-eval --no-llm --profile default --policy evals/skillevaluator/policy.yaml` 退出 0；报告 12 个 validator result 通过，静态门禁 PASS，publication INCOMPLETE。policy digest 为 `sha256:ef61893169f6170df5ca09265ed6057a72529fc8911b7b815ce2abe69d78ce0d`。这不是默认策略通过，也不是行为效果改善。
- 首批 5 例为 4 正例、1 负例，来源、改编和正反判据见 `evals/skillevaluator/agent-eval/EVAL.md`。独立上下文审阅 Galileo 未发现有证据的 P1/P2；未冒充用户验收或 Judge 校准。
- 暂存完整 agent-eval 快照后，`tier3 validate --strict --json` 退出 0。数据集仍为 provisional，未满足上游 10 例的充分性要求，不用于发布认证。
- 20 项现有契约测试、OpenSpec strict、diff 检查通过；发布包 `skills/`、README、用户 docs 和原 tests 没有本 change 的内容变更。
- 原始报告、审阅记录、日志、退出码、数据集与快照哈希在 `.local/validation/skillevaluator-integration/20261117-adapted/`。

## 未闭合项

本轮 doctor 再次退出 1：Docker ready，但 public LLM provider 未配置，agent 自动选择也无法完成。所检查的 `SKILL_EVAL_LLM_PROVIDER`、`SKILL_EVAL_LLM_API_KEY`、`SKILL_EVAL_LLM_BASE_URL`、`NVIDIA_API_KEY`、`OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 均未导出；只记录存在性，未搜索配置文件或读取密钥。

上述缺 provider 是此前运行的历史状态。用户随后提供现有网关并授权选择较小方案，当前恢复官方 Harbor/provider 路径；子代理桥接未实现且不再属于本 change。

6.4 至 6.6 按实际新运行结果更新，不用数据校验或网关连通代替 Tier 3 验收。

## 2026-11-17 已有网关接线

- 用户提供现有 OpenAI-compatible 网关后，选择未修改的官方 Tier 3。宿主 Chat Completions 返回 HTTP 200 和预期文本，工具调用返回合法 `record_probe` 参数。模型请求 ID 为 `group/j.a.r.v.i.s`，网关回显相同别名，底层模型版本尚未确认。
- Docker Engine 29.8.2 可用；隔离容器经 `host.docker.internal:3425` 访问网关 catalog 返回 HTTP 200。宿主使用 `127.0.0.1:3425`。凭据仅经进程环境传入，不持久化到项目文件。
- `doctor --env-mode docker -a opencode --agent-model opencode=openai/group/j.a.r.v.i.s --verify-models` 退出 0；模型 catalog 可达，但官方明确提示 catalog 不证明推理凭据。一次附带 `--timeout 30` 的探查退出 2，因为固定版不支持将该选项用于 Tier 3；已按帮助移除并保留失败日志。
- 官方 `validate-grader --check-suite --json` 退出 0，assessment 套件共 14 例。只选 `arithmetic` 与 `wrong-answer` 各一次，未指定失败率阈值时退出 0；两个样本的 accuracy 与 goal_accuracy 均符合标签，但唯一错误答案的 overall 被判为 pass（0.82）。
- 为验证阻断方式，以同两例再运行并显式设置 false-pass、false-fail、unjudgeable 上限均为 0，退出 1，仍观察到该错误答案的汇总误放行。两轮结果均保存；这是有限正反例的真实失败，不推算一般误判率。协议已增加关键结果不可被总分抵消和显式评分器阈值。
- 5 项 policy 测试、20 项原契约测试、OpenSpec strict 与 diff 检查通过；发布包边界检查退出 0。
- 证据位于 `.local/validation/skillevaluator-integration/20261117-gateway/`，含命令、版本与哈希、网关探查、评分器报告、退出码和失败日志。

汇总门禁尚未通过校准。双组冒烟用于诊断运行链路，不能据此放行 Skill；完整五例及领域判据校准保留未完成，先消解汇总误放行的验收影响。

## 2026-11-17 官方 local 冒烟完成

- Docker 初次双组冒烟退出 1，`INCOMPLETE`，0/2 scored；两组都在构建阶段发生 600 秒 `EnvironmentStartTimeoutError`，不是 Skill 行为失败。设置 `--timeout-multiplier 3` 的第二次 Docker 运行仍在 pip 版本回退，主动中断，退出 1；中断日志保留，不当作自然超时或评分结果。未修改官方引擎。
- 官方 local 就绪检查退出 0，网关 Responses API 实际推理 HTTP 200。使用现有 Codex CLI 0.169.0、`codex=group/j.a.r.v.i.s`、默认 timeout 1x、每组一次与独立 HOME/macOS Seatbelt 执行；只面向当前已审阅的可信 Skill，不能据此声称 Docker 级隔离。
- `tier3 evaluate <完整暂存快照> -a codex --agent-model codex=group/j.a.r.v.i.s --env-mode local --max-cases 1 --n-attempts 1 --max-attempts-total 2 --harbor-keep-jobs --results-dir <local-smoke-results>`：退出 0，`execution_status: succeeded`，2/2 scored，执行错误和 Judge 错误均为 0。
- 带 Skill 轨迹实际读取暂存的 `agent-eval/SKILL.md`，报告激活 1/1；无 Skill 组未加载该 Skill，其尝试读取原仓库 `skills/` 的操作被拒绝。这只证明本轮所观察路径，未全面验证安全隔离。
- 两组 accuracy、goal_accuracy、behavior_check 与 security 均为 1.0。带 Skill discoverability 为 0.9375、efficiency 为 1.0。报告按双方共同适用指标计算 paired overall 均为 1.0，Skill Lift 为 0.00；不能用单臂原始 overall 0.9875 与 1.0 直接相减来替代配对结果。人工核对两组回答均满足本案例三项断言，未观察到结果改善。
- 仅执行 `environment-noise`，未运行其余四例及负例，也未做旧新版比较。数据充分性为 provisional；上游模型版本仍未固定，费用为未知，不伪造金额。官方评分器正反例的汇总误放行仍是独立未闭合项。
- 报告：`.local/validation/skillevaluator-integration/20261117-gateway/local-smoke-results/agent-eval/20261117_125606_49816_69a1490f89b4/report.html`。同目录保留 result、run_config、双组轨迹和 lift。已扫描本轮保留文件，未发现所提供密钥值；本轮 Docker 构建均已停止。

第 6.5 项的执行／加载／评分／报告链路已跑通；第 6 项整体及 6.6 保持未完成。保留活动 change，不同步当前规格、不归档、不提交或推送。

## 2026-11-17 推荐模型接线

- 按维护者推荐，分别使用 `auto/gpt-5.6-sol` 和 `auto/glm-5.3`。网关 catalog 包含两者，Responses API 强制工具调用均返回正确 `record_probe` 参数；回显分别为 `group/auto-gpt-5-6-sol`、`group/auto-glm-5-3`，底层版本未确认。
- 两次 `doctor --env-mode local -a codex --agent-model codex=<模型> --verify-models` 均退出 0；catalog 提示不证明推理授权，已用上述真实调用单独验证。
- 两次 `tier3 evaluate <同一暂存快照> -a codex --agent-model codex=<模型> --env-mode local --max-cases 1 --n-attempts 1 --max-attempts-total 2 --harbor-keep-jobs --results-dir <模型独立目录>` 均退出 0。Judge 固定 `group/j.a.r.v.i.s`，Codex 0.169.0、high reasoning、timeout 1x、local 后端保持一致。
- 每个模型均为 2/2 scored、execution succeeded，官方运行错误与 Judge 错误均为 0。带 Skill discoverability 为 0.9375，其余四维均为 1.0；共同适用指标的配对 overall 两组均为 1.0，各模型 Skill Lift 均为 0.00。人工核对四份回答满足本例三项断言，未观察到答案质量改善。
- 两个带 Skill 轨迹均有成功读取目标 `agent-eval/SKILL.md` 的工具返回。基线未读取目标 Skill；GLM 基线有两次错误工作目录调用并恢复，还读取了宿主内置 `review-agent/SKILL.md`。因此“无 Skill”指无目标 Skill，不是无任何宿主指导；运行成功不代表过程零工具错误。
- 保留逐组 token 数据。GLM 基线反复寻找不存在的目标 Skill，不能将本例 token 差直接推广为稳定效率提升。GPT 轨迹的费用是 LiteLLM 估算，GLM 缺价格，网关实际账单未知，不比较费用。不同模型的 CLI 系统提示和工具表示有差异，本轮不作模型排名。
- 5 项 policy 测试与 20 项原契约测试通过；发布包边界检查退出 0。本轮保留文件的凭据扫描未发现所提供密钥值。
- 证据根目录为 `.local/validation/skillevaluator-integration/20261117-models/`，包含两份探针、doctor 与评测命令／退出码、provenance 和报告。GPT 报告位于 `gpt-5.6-sol/results/agent-eval/20261117_131710_61741_bfc334225276/report.html`，GLM 报告位于 `glm-5.3/results/agent-eval/20261117_131710_61740_334f61683a37/report.html`。

两模型均可接入当前验证链路。本阶段只运行 `environment-noise`；完整五例、领域 Judge 校准和旧新版效果比较未执行，转为后续维护动作。此前已标注反例的汇总误放行问题仍需在后续评分器校准中闭合，项目验收规则已禁止总分抵消关键失败。

2026-11-17，用户确认本阶段验证体系接入完成，允许同步规格并归档。
