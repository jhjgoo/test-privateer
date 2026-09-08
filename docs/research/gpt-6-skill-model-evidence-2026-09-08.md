# GPT-6 Astra 与 skill 约束：官方文档证据

研究日期：2026-09-08。范围：官方提示指南中的指令遵循、技能披露、写作格式和消息优先级。未调用模型 API，未修改技能。

## 来源与获取边界

- [S1：OpenAI Model guidance](https://developers.openai.com/api/docs/guides/latest-model)，2026-09-08 通过 Exa 搜索后抓取页面全文；使用其中 GPT-6 Astra 的 Instruction following、Personality and writing style、Prompting best practices 段。直接 HTTP 请求返回 Forbidden，Jina Reader 未及时返回，最终依据是 Exa 返回的官方页面正文，而非搜索摘要。中间结果位于 `/tmp/gpt6-official-model-full.txt`，属于可清理的临时材料。
- [S2：OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)，同日通过 Exa 抓取页面正文；使用 Message roles and instruction following 和关于非确定性与评估的段落。中间结果位于 `/tmp/gpt6-official-prompt-full.txt`。
- [S3：本地 Offline Model Guide](/Users/jianghongjian/.agents/skills/skill-eval/references/openai-gpt-6-astra.md)，文件声明是用户于 2026-09-07 提供材料的编辑版，且未独立抓取或核实。它可提供调查线索，不能独立充当实时官方证据。本报告中能够用 S1/S2 核验的结论以官方页面为准。

## 已证结论

| 结论 | 证据 | 能支持到哪里 |
| --- | --- | --- |
| 官方指出 Astra 对上下文、技能和 AGENTS 指令更敏感；冲突或不清晰技能可能导致提前暂停。 | S1 Instruction following：更能遵循长指令，同时对上下文更敏感；直接举例 unclear or conflicting guidance in a skill file may cause 提前阻塞。 | 支持优先检查多层指令冲突；不证明本项目的某次失败由此造成，也不证明它不遵循技能。 |
| “用户要求优先于技能指南”在官方指南里是建议加入的提示示例。 | S1 建议 Make the priority of user instructions and skills explicit，并给出示例。 | 需要看宿主实际如何注入这些规则；不能把文档示例当作所有模型调用都天然具有的额外指令。 |
| “技能导致暂停时说明具体文件和指令”是用于透明度的提示示例。 | S1：Asking the model to identify the skill and instruction ... can also be effective ...，随后给出示例。 | 可以解释采用该示例的宿主为何要求披露；它不是仅由 GPT-6 型号自动带来的义务。 |
| 官方描述 Astra 默认倾向列表、表格和 Markdown。减少格式是应用可指定的偏好。 | S1 Personality and writing style：GPT-6 Astra tends to use lists, tables and Markdown ... If your application needs prose with less formatting, specify that preference. | 本段没有将“禁止章节标题”设为模型固有规则。固定标题丢失不能仅归因为模型天生拒绝标题。 |
| developer 与 user 的优先级属于通用消息角色机制。 | S2 Message roles and instruction following 明确 developer 优先于 user；instructions 参数优先于 input。 | 宿主的高优先级规则可约束用户技能的执行方式。该机制本身不是 GPT-6 独有。 |
| 单次输出不足以量化模型升级导致的遵循退化。 | S2 说明生成非确定、同家族不同快照也可能有差异，并建议固定快照和建立评估。 | 应在相同输入、相同宿主规则和相同加载材料下做模型对照与重复观察。 |

## 对当前问题的解释边界

本次会话中可观察到平台层面的写作格式偏好和技能导致暂停时的披露规则。这为“技能要求的标题或展示方式受到其他规则影响”提供了具体机制。平台层摘要只用于说明冲突类别，不导出内部指令原文。

历史失败任务是否具有相同的平台配置、实际运行模型和技能版本，仍需历史证据。当前机制成立，不等于历史归因已经成立。若历史输出保留了提问方式、澄清差异与暂停行为，却遗漏规定标题，应分别记录“行为契约遵守”和“输出结构缺失”，避免把整体技能判成未加载或完全无效。

若技能允许环境要求的披露例外，则披露本身不能直接记为违规；必须以历史实际加载版本为准。

## 待证问题与最小验证

1. 固定历史实际加载的技能正文与用户输入，确认对应模型与宿主配置；只有能取得证据的配置才写成事实。
2. 独立评分：是否加载正文、是否遵守流程边界、是否保留必需内容、是否输出规定标题、是否出现允许的环境披露。
3. 如需定位宿主冲突，比较同模型下“无冲突的最小环境”和“实际宿主环境”。如需证明 GPT-6 特异性，再保持其他条件一致比较旧模型与 GPT-6，并重复运行；本次未执行这些模型实验。

目前官方文档支持“技能冲突与宿主规则应优先排查”，不支持“GPT-6 无法被 skill 正常约束”或“标题丢失必然是 GPT-6 独有问题”的结论。
