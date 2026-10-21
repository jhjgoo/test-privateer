# Proposal

## Why

对 `mattpocock/skills` v1.0.0～v1.3.1 与 `ask-matt` 路由的调研显示，本包在测试证据和授权边界上已较强，但在事实／决策分离、环境复盘、证据摘要和 Skill 包格式自检上存在可落地改进。近期 Workbuddy 打包连续暴露根路径、目录层级和 frontmatter 解析问题，也证明需要确定性检查而非依赖人工试错。

## What Changes

- `shaping-ai-tasks` 增加事实与决策分离：事实先自行调查；业务决策交用户选择，并给出推荐、影响和等待点。
- `maintaining-project-lessons` 增加环境复盘分支：机械错误优先沉淀为检查、钩子或 CI；判断问题进入规则；导航与信息缺口进入入口指针或取证动作。
- `assessing-test-confidence` 增加最小证据摘要：测试目标、最小示意、前基线、后结果、证据限制、风险与下一步，先服务读者决策再展开明细。
- 新增仓库级 Skill 包自检：校验 frontmatter 可解析与必填字段、引用路径存在、路由 Skill 存在、文档 Skill 计数正确，以及目标平台包的根路径、层级和大小限制。
- 增加代表性输入与契约测试；行为评测按风险最小执行，不新增通用运行器。

## Capabilities

### New Capabilities

- `skill-package-integrity`: 规定发布源与目标平台 Skill 包的确定性完整性检查和失败边界。

### Modified Capabilities

- `shaping-ai-tasks`: 任务升级在原始请求与任务契约中区分可调查事实与必须由用户决定的业务选择。
- `project-lessons`: 错题本维护在授权范围内将可自动检查的教训导向环境改进，不只追加文字规则。
- `test-artifact-quality`: 测试报告先提供面向决策的最小证据摘要，再展开主张、证据和限制。

## Impact

影响 `skills/shaping-ai-tasks/SKILL.md`、`skills/maintaining-project-lessons/SKILL.md`、`skills/assessing-test-confidence/SKILL.md`、相关测试与评测输入、OpenSpec 规格及可能的打包自检脚本。不引入外部依赖；不复制 `ask-matt`、不新增通用路由、不实现多 Agent 编排或通用 PR Skill。
