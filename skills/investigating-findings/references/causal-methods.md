# 原因调查方法卡

按当前调查障碍选方法。方法的产物用于提出和检验解释，不代表原因已经证实。

| 当前障碍 | 方法 | 带走的结果与边界 |
| --- | --- | --- |
| 类似对象有的异常、有的正常 | 发生／未发生对照与变化分析 | 对象、位置、时间、程度及关键差异；同时变化不等于因果 |
| 原因停在表面或候选太窄 | 连续追问（5 Why）或鱼骨图 | 有证据或待取证的原因分支；不固定追问次数，不把末端词语当根因 |
| 稳定失败涉及很大输入或多个版本 | 差分缩减、Git 二分定位 | 保持同一失败的最小输入或引入变化的版本；其他报错不能替代原失败，定位后继续解释机制 |
| 多个条件共同造成不良结果 | 故障树 | 顶层事件、与／或关系和待验证分支；没有可靠数据不计算概率 |
| 跨系统、跨角色且反复发生的事故 | 控制与反馈分析、无责复盘 | 控制责任、约束、反馈、促成条件及验证行动；不能以个人疏忽结束调查 |

跨服务问题先利用已有日志、指标和追踪串联同一对象的时间线，核对采样和关联限制；缺少关键证据时再提出补观测。调用关系与时间先后只提供线索。

例如回滚后恢复：若同时重启并清空缓存，先保留版本变化和状态重置两种解释，再寻找能区分它们的对照。恢复现象本身不足以决定采用哪种修复。

研发前分析潜在伤害时，可用故障树或控制反馈视角生成风险与测试条件；事后的原因结论必须来自实际事件证据。完整 STPA／CAST 需按原方法展开，仅借用部分问题时如实说明范围。

## 方法来源

- [ASQ：5 Why](https://asq.org/quality-resources/five-whys) 与[原因分析工具](https://asq.org/quality-resources/root-cause-analysis/tools)
- [Kepner-Tregoe：发生／未发生对照](https://kepner-tregoe.com/blogs/8d-is-or-is-not-that-is-the-question/)
- [NASA：故障树手册](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Fault%20Tree%20Handbook_NASA.pdf)
- [MIT：STPA／CAST 手册](https://psas.scripts.mit.edu/home/books-and-handbooks/)
- [Google SRE：无责复盘](https://sre.google/sre-book/postmortem-culture/)
- [Zeller：差分调试](https://www.st.cs.uni-saarland.de/dd/)；[Git 二分定位](https://git-scm.com/docs/git-bisect)
