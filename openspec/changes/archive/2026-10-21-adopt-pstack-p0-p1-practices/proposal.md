# Proposal

## Why

横向对比 pstack 后发现四个可直接提升本包能力上限、且不破坏测试授权边界的缺口：

1. 长任务和评测缺少先行的可判定退出条件，容易在过程中临时解释目标；
2. Agent 行为评测缺少统一的盲评、匿名判定和加载轨迹核验协议；
3. 长任务暂停后缺少冷启动恢复点，恢复时也容易重做已完成工作；
4. 项目缺少“生成可持续真实产品验证器”的方法，现有能力偏一次性执行或具体测试编写。

这些能力分别对应 pstack 的 `autonomous-run`、`eval`、`pause-safely`／`session-pickup` 和 `create-verification-skill`。本包应吸收其可判定性和审计思想，但不复制其自动 merge、平台专属模型编排或全自主默认。

## What Changes

- `shaping-ai-tasks`：对连续执行、批量维护、比较评测或长任务建立**可判定退出条件**；条件可观察、可复跑、含截止边界，不得临时放宽以宣布完成。
- `agent-eval`：新增 Agent 行为评测协议：
  - 候选提示使用自然任务措辞，避免评测意图泄漏；
  - 评测判据只给评审，不给候选；
  - 比较输出使用匿名标签；
  - 从真实加载轨迹判断 Skill 是否被读取，不以自述替代；
  - 保留环境异常、无效案例和失败边界。
- `running-test-sessions`：新增暂停与恢复协议：
  - 暂停前完成或退回当前原子步骤；
  - 写冷启动恢复点，记录已验证事实、未验证结论、产物路径和下一动作；
  - 恢复时先继承权威轨迹，仅抽查关键断言，不重做已完成工作。
- `designing-test-automation`：新增项目验证器生成路径：
  - 从仓库和现有测试取证，访谈项目而非用户；
  - 生成项目本地验证说明或 Skill，覆盖启动、健康检查、真实用户路径驱动、证据、隔离和清理；
  - 生成后至少真实驱动一条用户路径并保留证据，否则只能交付草案；
  - 不默认引入框架，不替代现有测试资产。
- 增加最小静态契约检查与行为评测输入，覆盖 P0/P1 的正常路径和反例。

## Capabilities

### Modified Capabilities

- `shaping-ai-tasks`: 长任务在执行前具备可判定退出条件。
- `testing-workflow`: 执行会话支持可审计暂停、恢复和评测轨迹核验。
- `test-automation`: 支持生成并验证项目级真实产品验证器。
- `solution-agent-quality`: Agent 评测结论区分输出、加载轨迹与配置证据。

## Impact

- 修改：
  - `skills/shaping-ai-tasks/SKILL.md`
  - `skills/agent-eval/SKILL.md`
  - `skills/running-test-sessions/SKILL.md`
  - `skills/designing-test-automation/SKILL.md`
  - 相关规格、契约测试和评测资产。
- 新增行为评测输入与判据；真实模型运行记录按仓库规则放 `.local/validation/`。
- 不新增 Skill。
- 不实现自动 merge、夜间循环、宿主专属模型配置、通用 UI 自动化框架或跳过人工审批。
