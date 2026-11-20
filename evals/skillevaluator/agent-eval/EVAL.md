# Agent 评估证据的代表案例

## 范围

对象为 `agent-eval` 的评估报告审查行为。本组用于首次接线验收，不代表全包覆盖、真实文件维护或 `test-privateer` 自动路由。全部材料在提示中给出，因此可比较无 Skill 与带 Skill 的回答结果；实际 Skill 加载由轨迹独立判断。

## 来源与改编

| ID | 来源 | 本次改编及作用 |
| --- | --- | --- |
| environment-noise | `evals/agent-eval/inputs/environment-noise.md` | 将原文“两个完成”明确为业务断言通过，避免把完成自动当通过；显式指定评估能力，测试状态及分母 |
| self-report-only | `evals/agent-eval/inputs/self-report-only.md` | 去掉受测文件路径，保留自述不能证明加载；补明确缺少旧版结果，测试改善主张 |
| trajectory-conflict | `evals/agent-eval/inputs/trajectory-conflict.md` | 以客服退款为上下文，明确完整事件记录；区分未验证与产品真实失败 |
| bounded-valid-evidence | 本轮针对前三例设计的邻近正常对照 | 证据足够支持有限结论时应认可，防止机械拒绝一切通过结论 |
| plain-translation | 本轮设计的非评估请求 | 普通翻译不应进入评估流程 |

后两例是本轮设计的控制场景，不冒充历史用户请求。`expected_output` 和 assertions 只供评审；候选只接收 prompt。没有文件／工具执行契约，因此不以人工文件修订作为本组结果。

## 判据校准

本轮在设计层对下列正反答案做区分性审阅；这不是模型 Judge 已校准的证明。真实 Judge 调用前仍需检查实际评分能否保持这些区分。

| ID | 应接受的要点 | 应拒绝的错误 |
| --- | --- | --- |
| environment-noise | 2 pass、1 行为失败、1 环境错误、1 案例无效；比例给分母 | 将超时算通过得出 60%，或不说明分母 |
| self-report-only | 回答可评，加载和版本改善无法确认；补轨迹及配对旧版 | “候选说读过，所以已确认使用并改善” |
| trajectory-conflict | 退款正常未验证；查询证据需在授权范围内 | “退款服务已经失败”或“退款已验证正常” |
| bounded-valid-evidence | 限定结论成立，但不证明改善和稳定性 | 无理由否认已给证据，或声称新版全面提升 |
| plain-translation | “会议明天上午九点开始。”等同义译文 | 评测框架、风险矩阵或擅自查询日历 |

## 运行计划

先运行 `environment-noise` 一例，每组一次、一个 agent，共 2 个逻辑尝试，另有 Judge 调用；预算上限为 2 attempts。就绪且冒烟完整后，再运行全部 5 例，每组一次，共 10 个逻辑尝试，另有 Judge 调用。首轮只验收链路和案例可判定性，不以这一次执行宣称稳定效果。

固定 provider、agent/model、judge/model 和 sandbox 后记录到运行清单。未提供凭据时只进行 strict 数据契约校验，禁止使用假 key、伪造结果或绕过沙箱来宣称 Tier 3 跑通。

## 本轮审阅

2026-11-17，成稿 Agent 按 `challenging-test-designs` 自校，独立上下文审阅者 Galileo 核对三个原输入、五例 prompt／expected_output／assertions、策略与官方数据契约，未发现有证据的 P1/P2 问题。审阅接受本组作为接线验收候选，未代替用户对产品效果的验收，也未执行真实 Judge 校准。

本地 `tier3 validate --strict --json` 退出 0，确认 4 正例、1 负例，预期与断言均完整。工具把 5 例标为 provisional；尚未满足上游 10 例的数据集充分性要求。以上是设计审阅与数据契约结果，不是 Tier 3 执行结果。

## 后续执行边界

2026-11-17，通过官方 local 后端、Codex CLI 0.169.0 与所提供网关完成 `environment-noise` 的双组冒烟：2/2 scored，两组回答均满足该例三项断言，配对 Skill Lift 为 0.00，并观察到带 Skill 组真实读取。其余四例尚未执行；不将冒烟的结果或单个读取动作推广到全套案例。

另用官方随包的 `arithmetic`、`wrong-answer` 已标注样本检查评分器，发现错误答案的关键指标失败但 overall 通过。显式失败率阈值能阻断该检查，汇总评分仍不能独立用于验收。这不是本表五组领域正反答案均已完成模型校准；后续状态与证据位置见[活动 change](../../../openspec/changes/integrate-skill-evaluator/tasks.md)。

同日按维护者推荐，保持该快照与案例、Codex CLI/local 后端及 Judge 别名不变，分别对 `auto/gpt-5.6-sol`、`auto/glm-5.3` 重跑完整双组。每个模型均为 2/2 scored，带 Skill 实际读取已确认，配对 Skill Lift 均为 0.00。四份回答均满足三项断言。GLM 基线出现两次路径调用错误后恢复，并读取宿主内置 `review-agent`，未读取目标 `agent-eval`；基线定义仍是无目标 Skill。以上仍为单例接线结果，不扩展案例覆盖，也不证明模型优劣或稳定提升。
