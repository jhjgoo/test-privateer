# Design

## Context

本 change 来自对 `mattpocock/skills` v1.0.0～v1.3.1 与 `ask-matt` 的调研。`ask-matt` 的可借鉴点不是复制其工程主线，而是四类机制：事实／决策分离、环境复盘、面向读者的最小证据摘要、以及格式与路由的确定性维护。Workbuddy 打包失败进一步证明包完整性检查需要自动化。

## Goals / Non-Goals

**Goals:**

- 用最小改动吸收 P0/P1 实践，并保持现有 27 个 Skill 结构。
- 让任务升级在关键决策上停得准，事实不推给用户。
- 让错题本维护能产生环境改进，而不是只堆规则文字。
- 让测试报告先服务决策，再展开证据。
- 用一个脚本同时检查发布源和目标平台包结构，防止重复打包试错。

**Non-Goals:**

- 不引入 `ask-matt`、`grilling`、`wizard`、`retro`、`pr` 的同名新 Skill。
- 不实现多 Agent 并行编排、通用 PR 生成或交互式人工操作脚本。
- 不建立通用 Skill 写作理论；只补充本项目可观察的检查。
- 不把 Workbuddy 元数据写入发布源；目标包仍按平台临时构建。

## Decisions

1. **事实／决策分离放进 `shaping-ai-tasks`。** 该 Skill 已是任务前置入口，新增独立 grilling 会重复澄清职责。
2. **环境复盘扩展 `maintaining-project-lessons`。** 项目已有错题本与规则权威位置，另建 retro 会形成两套返工记录。
3. **最小证据摘要扩展 `assessing-test-confidence`。** 报告职责已在当前 Skill，`test-artifact-quality` 只沉淀跨产物契约。
4. **新增一个 Python 自检脚本而不引入依赖。** 使用标准库解析 frontmatter、路径与 zip；YAML 值采用受限标量解析，足够覆盖当前 Skill frontmatter。
5. **目标平台配置内置于脚本参数。** 首个支持 `workbuddy-flat`：根 `SKILL.md`、路径最多二级、3MB 上限；后续平台可加配置，不做通用打包框架。
6. **行为验证用代表样本。** 事实／决策、环境复盘和证据摘要各选正反场景；包自检用真实 Workbuddy 失败形态做单测。

## Risks / Trade-offs

- [事实调查扩大范围] → 仅调查授权内且会改变任务方向的事实，记录来源与边界。
- [复盘越权改 CI] → 只在用户授权对应文件或配置时落地；否则交付建议和未实施状态。
- [摘要模板化] → 明确“只有比文字清楚才用图”，短报告不强制新增章节。
- [自检脚本误报] → 校验范围从当前包结构出发，失败输出文件、路径和原因，允许按目标平台显式配置。

## Migration Plan

1. 扩展三个 Skill 的行为规则。
2. 实现 `scripts/check_skill_package.py` 与单元测试。
3. 增加代表性评测输入和判据。
4. 运行自检、单元测试、OpenSpec 校验和 `git diff --check`。
5. 保留活动 change，等待用户确认后归档。

## Open Questions

无。
