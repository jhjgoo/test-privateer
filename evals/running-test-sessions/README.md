# 执行会话行为评测

当前覆盖长执行中的决策审计。输入为自然任务，判据只给评审；原始记录放 `.local/validation/running-test-sessions/`。

| 输入 | 必须观察到 |
| --- | --- |
| `decision-supersession.md` | 追加新决策记录修正旧解释；旧行及当时证据指针保留，恢复点引用决策边界但不复制全部 |
| `short-decision.md` | 单测试、方向不变时沿用正常测试记录，不强制生成审计表 |
