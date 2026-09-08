# Test Privateer Skills

一套面向测试全生命周期的黑帆测试官 Skill。它以产品价值确定方向，以产品风险选择重点，以测试证据驱动下一轮学习。

`test-privateer` 是主入口；其余 Skill 提供澄清、测试空间扫描、风险分析、测试建模、测试设计、执行、回归、自动化与信心评估能力。

## 安装

这是一套由 18 个 Skill 组成的完整工作流。`npx skills` 不会自动安装 Skill 依赖，因此必须安装全集。

```bash
# 交互式安装
npx skills add jhjgoo/test-privateer --skill '*'

# Codex 全局安装
npx skills add jhjgoo/test-privateer --skill '*' --agent codex --global --yes

# Codex 项目级安装
npx skills add jhjgoo/test-privateer --skill '*' --agent codex --yes
```

安装前查看可用 Skill：

```bash
npx skills add jhjgoo/test-privateer --list
```

不要只安装 `test-privateer`。主入口会路由到其他 Skill，缺少任一组件都会削弱工作流。

## 使用

在支持 Agent Skills 的客户端中显式调用 `test-privateer`，并提供 PRD、Spec、代码、测试对象或当前观察。它会先判断独立测试与项目测试路径，再路由到当前真正需要的测试活动。

第一次使用请阅读[《海盗派黑帆测试官：方法与 Skill 使用教程》](docs/guide.md)。它通过完整案例讲解这套测试方法，以及何时调用哪个 Skill、应取得什么产物、何时停止或转向。

也可以直接调用方法 Skill，例如：

- `scanning-product-with-sfdipot`
- `analyzing-test-space-with-mfq`
- `modeling-tests-with-ppdcs`
- `writing-unit-tests`

接口／页面自动化目前提供测试设计入口，均通过 `designing-test-automation` 使用；框架接入、脚本编写暂未实现。单元测试可使用 `writing-unit-tests` 编写并验证；已有测试可在授权范围内执行。

Skill 按当前任务与信息缺口协作，不按职业或资历分流。测试设计、执行准备和实际结果分别说明；具体用例写好不代表目标版本与环境已就绪。

## Skill 清单

| 阶段 | Skill |
| --- | --- |
| 主入口 | `test-privateer` |
| 使命与上下文 | `setting-test-mission`, `clarifying-test-basis` |
| 项目与变化 | `mapping-project-test-space`, `analyzing-change-for-testing` |
| 测试空间 | `mapping-test-space`, `scanning-product-with-sfdipot`, `analyzing-test-space-with-mfq` |
| 风险与模型 | `analyzing-product-risks`, `modeling-tests-with-ppdcs` |
| 测试设计 | `designing-test-experiments`, `writing-unit-tests`, `challenging-test-designs` |
| 执行与发现 | `running-test-sessions`, `investigating-findings` |
| 回归与自动化 | `selecting-regression-tests`, `designing-test-automation` |
| 证据与信心 | `assessing-test-confidence` |

## 更新

```bash
npx skills update
```

`update` 只更新已经安装的 Skill。仓库新增组件后，请重新执行全集安装命令。

## 兼容性

仓库遵循 [Agent Skills specification](https://agentskills.io/specification)，并使用 `npx skills` 的标准多 Skill 目录结构。不同客户端对 Skill 路由和工具调用的执行能力可能不同；格式兼容不等于行为完全一致。

## License

[MIT](LICENSE)

## 测试文档

持久化时，每个需求使用共同稳定前缀的 `-test-analysis.md` 与 `-test-cases.md`；详细依据和模型按需放 `-test-basis.md`。已有需求目录直接沿用，否则放 `testing/requirements/<前缀>/`。项目地图仍为唯一 `testing/TCO.md`。分析保留全体已识别测试点、动态风险和当前行动；用例开始设计时创建，执行证据单独记录。

编号与跨文档追溯统一遵循 [artifact-routing](skills/test-privateer/references/artifact-routing.md#统一编号与追溯)。完整分析、独立模型和用例集交付前，Agent自行复核并修正文档错误；只有真正需要业务选择或扩大授权时才提问。
