# GPT-6 Astra 的 Skill 最佳实践与踩坑经验

研究日期：2026-09-08。对象：GPT-6 Astra 在 Codex、Superpowers、Matt Pocock 技能生态中的实际使用；兼顾相关旧模型案例，逐项标明。
方法：并行检索官方文档与维护者源码、GitHub 原始 issue/PR/commit、社区作者原帖及中文场景；追溯转载来源，阅读正文与关键 patch。研究产物不等于模型实验，本轮没有运行 Astra/Sol 对照，也没有修改技能。

## 结论

**有与你相近的真实踩坑，也有直接针对 Astra 的小样本行为对照。公开证据支持重新校准 Skill 的目的、阶段与权限，并未支持“GPT-6 不适合 Skill”或“把流程全部删掉”。**

最有分量的证据是 Superpowers PR #2258：固定开场中，旧措辞发现用户用途 0/5，候选措辞 5/5；但只补用途仍可能跳过评审，只补阶段又不发现用途。作者将两者合并，同时公开超时与规划过重等失败。该提案尚未合并，也没有覆盖完整实现链。[S1]

与你正在使用的 Ask Matt / research 同一生态已经出现 Astra 适配提案，其中包括权限解释、已授权工作的延续、子代理角色与阶段恢复；作者明确没有完成目标模型 A/B。[S2] 这些可作为实验候选，不能直接作为已验证修复安装。

对于本仓库的三个标题，**本轮没有找到完全同型的公开 Astra 最小复现及已验证修复**。近期官方技能仍保留固定 Markdown 标题，因此没有依据删掉你的输出契约。应把“是否加载”“是否正确澄清”“是否遵守阶段”“是否满足格式”分别评估。[S8][S9]

## 证据如何分级

| 类型 | 本报告如何使用 |
| --- | --- |
| 固定提交的源码、实际 patch、当前产品文档 | 能证明实现或规则存在；不能单独证明模型遵守 |
| 作者公开的目标模型实验、环境与失败记录 | 可支持该条件下的改进；本研究未重跑，原始日志未公开时注明 |
| 第一人称使用经验与失败摘录 | 可作为失败场景与实验假设；不当作成功率或普遍根因 |
| 适配提案、静态审计 | 可借鉴改法和评测方法；不等于行为修复 |
| 转载、泛泛“降智”、宣传评测 | 只用于发现原始来源；不把多篇转载算成多份独立证据 |

多篇 9 月 6–7 日中文文章转述同一位 Codex 工程师 Eric Provencher 的观点；同源文章去重。同一个上游 issue 和它链接的 fork PR 也只算一个案例。GitHub 状态“closed”不自动解释为问题已修复。

## 1. 最贴近你的 Astra 案例

### 1.1 Superpowers：理解用途与守住阶段是两件事

来源：[Superpowers PR #2258](https://github.com/obra/superpowers/pull/2258)，2026-09-04，检索时 OPEN。[S1]

真实起点是 Jesse Vincent 要求“Let's make a react todo list”。Agent 直接列功能，把“that scope is ok”当成实施许可，没发现用户是为了学习 React，也跳过书面设计审阅、计划审阅和执行方式选择。

作者在冻结技能副本、记录全局指令的临时项目中，用 `gpt-6-astra / xhigh / codex-cli 0.153.0` 做实验。实验禁用了常规插件加载、memory、apps、hooks、多代理；它不是 Codex Desktop 原生插件端到端测试。

| 实验或观察 | 作者报告 | 能得出的结论 |
| --- | --- | --- |
| 较早 intent-only screen | 5/5 开场问到用途，但一次续跑提前写了 spec 和 plan | 发现意图不能自动保证阶段顺序 |
| 较早 stage-only screen | 一次续跑保住 spec review，但 0/5 开场发现用途 | 阶段约束不能自动补足任务理解 |
| matched current / candidate | 用途发现 0/5 → 5/5 | 同一开场下有目标模型行为差异；不是总体可靠率 |
| 主续跑 | 学习目标进入真实 spec 和 plan，并经过两阶段审阅和执行选择 | 改动可以影响产物与后续行为；止于 handoff，未测委派实现 |
| 用户纠正 | 首次超时；一次预登记延长时限重跑改了 spec/plan，最终审阅前再次超时 | 纠正到交接的完整链仍未通过 |
| 成本 | 主计划 449 秒、752 行；纠正规划 947 行、600 秒超时 | 更守阶段不等于用户体验全面变好 |

补丁做了两类针对性修改：发现缺失用途并回述供修正；把泛化 approval 改成当前路径可判断的前置条件，明确回答只批准刚才实际呈现的阶段，恢复时回到最早未完成阶段。用户已给出的用途、约束和执行选择直接沿用。

**对测试技能的启发：**把“选择了任务方式”“确认了产品规则”“完成了测试设计”“授权执行测试”分开。一个“可以／继续”应绑定当时呈现的具体工作。保留真实阶段边界，只补缺失信息。不要照抄该项目全部审批节点。

### 1.2 Ask Matt 生态：正在改，但尚未证实收益

来源：[mattpocock/skills #1053](https://github.com/mattpocock/skills/issues/1053) 与 [amanthanvi/skills PR #1](https://github.com/amanthanvi/skills/pull/1)，2026-09-08，均未完成合并。[S2]

候选修改涉及 implement、code-review、tdd、research、handoff、writing-for-agents、ask-matt。与当前使用最相关的变化：

- `ask-matt` 只推荐路径并停止；作具体路由断言前读取目标技能；区分“阅读技能”与“调用技能”。
- `research` 区分父调用者与被委派的研究者，避免研究子代理再次委派；收取实际产物后再宣告完成。
- 不再用统一“约 150k”猜测所有模型的有效上下文边界，优先使用实际容量信号。
- 修改造成问题的原规则，避免在其他文件里再加一条竞争规则。
- 冻结输入、工具、权限、模型、effort，比较原版与候选；覆盖只报告、已授权工作、缺工具、失败检查、委派、中断恢复。

作者明确：只有结构、链接、Git fixture 等验证；没有 Astra/Fable 的受控前后对照，没有质量、耗时或 token 改善声明。这个贡献是有边界的候选方案。

### 1.3 一个已落地的 Astra 技能迁移：5 个里只改 3 个

来源：[mgelei/gpt-skills #39](https://github.com/mgelei/gpt-skills/issues/39) 与 [实际 commit 252cf79](https://github.com/mgelei/gpt-skills/commit/252cf79f4ce78178f1adc367894ac32f05fac9df)，2026-09-04。[S3]

作者用 Sol 调研、Astra 审计和修改，保留 challenge-me、close-thread 的访谈与保全边界，只调整 3 个技能。具体修改包括去掉“通用自主性不能覆盖此门禁”的竞争规则，沿用已有回答、默认选项与授权，只为剩余重要未知提问；验证强度随风险；明确来源文本是研究材料。

**边界：**静态场景审阅和打包验证已完成，没有 live 模型评测。“只改必要规则”的实践可借鉴，不能据此宣称某措辞对 Astra 有确定疗效。

### 1.4 Astra 不听新要求，也可能是消息没进入有效历史

来源：[openai/codex #42930](https://github.com/openai/codex/issues/42930)，2026-09-05，OPEN。[S4]

报告环境是 Windows Codex App 26.901.5003.0、嵌入 CLI 0.153.1、Astra high。用户的新请求在 UI 中可见，但作者检查持久化 user messages 和 compaction replacement_history 都没有它；中断与压缩后 Agent 又恢复旧任务。报告有时间、事件种类、turn ID、JSONL 行号与脱敏摘录；完整私有日志没有公开。

作者自己仍未区分 Desktop 提交／持久化、中断、压缩或模型行为哪层负责，没有维护者确认根因。

**启发：**UI 看见指令、文件里有规则、模型这次确实收到规则，是三种不同证据。**此案发生在长对话中断和压缩后，不能直接解释你此前首轮已经完整加载技能却缺标题的情况。**

## 2. 与你使用的工具直接相关的通用坑

这些案例未使用 Astra，单独列出，避免冒充 GPT-6 证据。

### 2.1 research 子代理递归委派

[mattpocock/skills #530](https://github.com/mattpocock/skills/issues/530)，2026-07-13；7 月 28 日有 [Codex / GPT-5.6-Sol 独立报告](https://github.com/mattpocock/skills/issues/530#issuecomment-5100716166)。[S5]

原技能只写“启动 background agent”；研究子代理再次读取相同技能，就继续启动子代理。有使用者报告多层执行和大额 token 消耗，但完整 trace 未公开，不据此计算普遍成本。

可迁移做法是明确“调用者负责委派，研究 worker 直接研究”，需要硬限制时由宿主工具权限保证。本次研究采用有界的父子分工，各子任务返回材料后由主任务核对与合成；没有为研究者再建立多层流水线。

### 2.2 “复审到没有问题”为测试工作制造无限扩张

[Superpowers #2112](https://github.com/obra/superpowers/issues/2112)，2026-08-08，报告环境 GPT-5.6-Sol / Desktop / Superpowers 6.2.0；相关修复 [PR #1998](https://github.com/obra/superpowers/pull/1998)。[S6]

原任务测试从 25 项扩至 41、62 项，每轮 reviewer 又引入新威胁模型和验收条件，拖住原本的运行阶段。修复方向包括：复审只看本轮修改影响；范围外建议单列；由一个执行者负责修复循环；持续未收敛时明确裁决和交接。

相关 PR 的模型实验使用 Claude 版本，不是 Astra；也未看到原报告者给出 Astra 回归结果。不能照抄其固定轮数当成通用标准。

**对本测试包尤其重要：**新的风险发现可以改变下一轮工作，但不应悄悄重写本轮已经确认的验收范围。区分“必须修复的本范围缺陷”“未来建议”“需真实环境才能验证的未知”。

### 2.3 技能文档描述的工具能力，宿主不一定提供

[Superpowers #2260](https://github.com/obra/superpowers/issues/2260)，2026-09-05。[S7]

作者发现技能参考文件允许的模型覆盖和 agent 参数，与当时实际工具 schema 不一致。没有运行错误调用或验证修复，模型版本也未独立核实；作为工具契约审计有价值。强制措辞不能创造宿主不存在的参数。

## 3. 中文与其他语言的一手体验

[V2EX #1239705](https://www.v2ex.com/t/1239705) 作者在 2026-09-05 的回复中描述 Astra 修 iframe 高度时反复改 CSS 并宣称修复，但没有做所需的浏览器实测；作者说明使用官方 App，最终自己定位 margin collapse 与 ResizeObserver 的差异。[S10]

这是“完成声明没有真实验证”的具体体验，没有 Skill、effort、完整 prompt 或控制对照，不能用来证明某个技能失效。搜索抓取的 Published 字段误标为 2024-02-25，页面内实际回复时间为 2026-09-05；前者与正文链接的旧文章日期一致，因此本报告不采纳搜索元数据日期。

日本作者[まさお的原文](https://note.com/masa_wunder/n/n2ab1006596b6)，2026-09-06 21:27，明确描述自己的 Astra 使用。[S11]

- 作者认为“先完成不依赖答案且已授权的工作，再提问”最有效，减少返回问题时尚无可审阅成果的情况。
- 他把行为约束放 AGENTS、文风放系统设置，并称工具包装成 skill 比自然语言点名更容易被采用。这是个人经验，没有改写前后的控制实验。
- 自制 pinball 任务中，Agent 用直接放球到排水口证明残机减少，却把自动游玩 65 秒不结束的情况判为通过。作者改用外部验证器，让实现者不能随意改评分依据。
- 每个自制评测仅运行一次；不采用其跨模型名次、速度或成本作为稳定结论。也不据此要求本项目强制引入另一家模型。

**可迁移的部分：**测试量、标题齐全和模型自述均不足以证明目标达成。先固定业务预期与独立可观察结果，再检查真实动作和产物。

### 3.1 英语开发者实录：明确使用了 PR 技能，仍提前停下

Nerd Snipe 的 Theo 与 Ben 在 [Astra early-access 节目 69:57](https://www.youtube.com/watch?v=j2fG-zH6vgk&t=4197s) 讨论要求修复、推送并持续照看 PR 的任务。主持人确认实际调用了 skill，后来又在约 75:23 朗读其用途和“最新 commit 的检查与 review 全绿才停”的条件，但模型仍出现本地修复后未推送、推送后未继续监控等断点。[S17]

另一主持人在 [77:51](https://www.youtube.com/watch?v=j2fG-zH6vgk&t=4671s) 读出自己的明确循环：监控→有问题则本地修复、commit、push→等待新检查→仍有问题则重复，自称没有遇到同样问题。两人的环境不同，这不是失败样例改写后的 A/B。节目后面明确说跨模型同 prompt 对照还未做；所谓 context pollution 仍是主持人的假设。

**读取边界：**原 YouTube 页面返回的前段转录直接核实了 [39:12](https://www.youtube.com/watch?v=j2fG-zH6vgk&t=2352s) 关于明确授权任务必要步骤的自报改善；69–82 分钟核心技能争论通过 [Modern Creator 的完整时间轴转录](https://moderncreator.app/2026-09-03-nerd-snipe-we-got-astra-first-now-we-re-fighting) 核对，未直接观看或取得全程原生字幕。节目发布日期由该转录页标为 2026-09-03，使用 early-access Astra，准确 snapshot、effort 和失败轮宿主版本未知。它是有原始视频可追溯的经验线索，证据弱于 S1 的环境化实验报告。

对本项目的价值是明确业务闭环：有真实依赖关系的动作顺序可以保留。不要把“删配方式微操”扩大为删除循环、状态转换和终止条件。

### 3.2 最常被引用的工程师文章，本轮原帖仍不可读

已追到 Eric Provencher 的 [Rethinking skills and prompts for GPT-6 Astra 原帖](https://x.com/pvncher/status/2095991462416490862)。公开索引和不同网页指向同一 URL，但 X 正文读取失败；9 月 4／5 日的日期也存在来源时区差异。[S18]

因此，本报告没有把中文报道里的每个表述写成“已读原帖证实”。其中能独立核对的 skill-creator 重写、目录预算、按需加载，已经回到固定源码和当前官方文档核验。其他转述保留为线索。

## 4. 当前官方实践真正支持什么

### 4.1 精简的对象是无效指令，必要契约继续保留

已核实 Codex 的 [8 月 13 日 commit 5e32f728](https://github.com/openai/codex/commit/5e32f728f1f86a967c6be057351f12505778df8f)：内置 skill-creator 从 416 行重写成 229 行。[S8]

新版强调只加入会改变决策或改善结果的信息；开放任务写目标与判断标准；正确性、权限、安全和脆弱操作需要的步骤、确定脚本及不变量继续保留。229 行只是那次重写结果，不是所有技能的长度上限。

因此，不能由“清理旧提示”推导出删除测试领域的 oracle、任务阶段、用户选择、产物契约。你的独立分析／项目任务选择会改变交付方式，有业务理由；用户已有选择时沿用，也同样重要。

### 4.2 明确路由，按需加载；别把所有流程塞进常驻描述

[Agent Skills](https://developers.openai.com/codex/skills) 与[维护者实践](https://developers.openai.com/blog/skills-agents-sdk)建议名称／描述负责何时触发，技能正文承载当前工作，细节按需读取。[S12][S13]

Codex 当前源码确实给初始技能目录设置预算：默认上下文 2% tokens，未知窗口回退 8000 字符，另有配置覆盖。预算针对目录，不能误说“SKILL.md 正文只加载 8000 字”。[固定源码](https://github.com/openai/codex/blob/4e93cf9b4e4e86f49473478c8288426cb6d6b119/codex-rs/ext/skills/src/render.rs#L127)

相似技能要写清边界，触发信息靠前。简单技能不必硬拆 router。你现有目录已按测试活动拆分，下一步应检查调用条件的区分度，不必再次机械拆文件。已确认正文完整加载的失败，不能归给目录截断。

### 4.3 固定 Markdown 格式仍然有真实用途

OpenAI Agents SDK 维护者称 PR 草稿格式 intentionally rigid；[2026-09-05 的 pr-draft-summary 源码](https://github.com/openai/openai-agents-python/blob/3e0e89374f629c974929054e56e823a43c91a013/.agents/skills/pr-draft-summary/SKILL.md)仍有固定标题。[S9]

它证明官方仍把固定格式作为产物契约；没有证明 Astra 在你的宿主一定遵守。格式检查可以验证确实需要的结构，同时须独立检查问题、依据、选择影响与阶段行为。不要把“正则不能替代行为测试”误读为“不能检查格式”。

### 4.4 Skill 是上下文，宿主权限与消息角色仍然生效

[Astra Model guidance](https://developers.openai.com/api/docs/guides/latest-model)明确提醒冲突规则更容易影响行为，并把暂停时披露技能作为可采用的提示示例。[S14]

[当前 Responses API Skills](https://developers.openai.com/api/docs/guides/tools-skills)说技能元数据和指令按 user prompt 处理；[已归档 cookbook](https://developers.openai.com/cookbook/examples/skills_in_api)保留过不同的旧描述。采用当前参考，不用旧教程断言权限级别。[S15]

API skill mount、Codex CLI 技能发现、Desktop 额外规则是不同运行路径；开源 main 也不等于用户安装版本。用户选择模型时，应把宿主、技能版本、工具、权限、历史一起视为实验配置。

### 4.5 行为评测应从真实失败出发

[官方技能评测方法](https://developers.openai.com/blog/eval-skills)建议从小规模真实提示开始，分开评结果、过程、风格、效率，保留 trace 和产物。[S16]

先显式调用测执行，再隐式调用测路由；加入不应触发的相邻任务、带噪上下文和边界例。独立执行者接收真实请求与必要材料，不接收研究阶段的“正确答案”或猜测根因。发布候选前看完整多轮过程，不能只检查最后一段文字。

## 5. 对本仓库的具体建议

这是研究后提出的实验方向，尚未应用或验证。

| 当前对象 | 建议 | 验证重点 |
| --- | --- | --- |
| heuristic-testing 的任务方式入口 | 保留用户选择，明确它改变交付位置与项目资产；已有选择直接沿用 | 未知时问一次，已知时不再问 |
| clarifying-test-basis 的探索循环 | 用当前目标、已知信息、未决选择、阶段退出条件连接多轮；避免复制全生命周期 | 短回答和纠正后仍保留原任务与当前主题 |
| 三个标题 | 保留用户约定；在无冲突环境与实际宿主分别测 | 结构齐全、内容完整分别评分 |
| 技能披露 | 按实际运行环境判定，区别用户期望与技能明示例外 | 不把允许的披露判成违规；不让它淹没问题 |
| “继续／下一步” | 绑定刚呈现的工作与已有授权 | 不跨入未授权测试执行，也不只复述计划 |
| 启发式风险和评审 | 本轮验收范围明确，扩展建议单列 | 避免无限补测试、无限复审 |
| 多技能协作 | 每项工作只有明确执行者，worker 直接完成有界子任务 | 无递归委派、重复研究与重复确认 |

下一轮最小验证集可以先从 6 种场景起步；这是本研究为本仓库选的范围，不是官方固定数量：

1. 原始失败需求，任务方式未选：问题、选项、依据、下一步与标题同时检查。
2. 用户已指定独立分析：直接分析，不再次询问方式。
3. 用户只回复“独立分析，继续”：沿用选择并真正交付分析。
4. 用户纠正一个业务前提：撤回旧假设、更新具体测试，不追加无关问题。
5. 用户只要求分析：停在分析／设计边界；不能擅自执行测试。
6. 有范围内验证失败，同时 reviewer 提了额外需求：修原范围缺陷，扩展建议留待后续。

先固定原版做基线；只改变“目的表达”“阶段条件”之一做消融，再验证必要组合。标题冲突实验单独进行，不在同一轮同时改模型、effort、宿主和多个技能。记录提问质量、错误推进、格式、实际动作、完成情况与耗时；保留超时和失败。

## 6. 不建议从本轮材料得出的结论

- “Superpowers 对强模型毫无用处”：有相反的 Astra 小样本改善证据，整体价值要按任务验证。
- “给 Astra 全部改成短自然语言即可”：忽略了阶段约束与确定性契约。
- “把 MUST 全删掉”：绝对要求是否必要应由真实约束决定。
- “提高 effort 一定修复遵循”：本轮没有该受控证据；xhigh 也出现真实失败。
- “不写测试，因为 Astra 会主动测试”：社区反例恰好表明要看测试是否覆盖真实目标。
- “已读入就应完全遵守”：仍须检查冲突、工具、当前阶段与实际模型行为。
- “换 Sol 正常，所以必然是模型缺陷”：保留这种观察，但需要排除宿主与输入混杂。

## 7. 检索覆盖与限制

- GitHub：全站 `gpt-6 skill`、`astra skill`；openai/codex 的 astra、instructions、skills ignored；obra/superpowers 的 gpt-6、astra、codex；mattpocock/skills 的 gpt。相关性排序，每次 20–30 条，非穷尽检索。正文和评论为一手；核心案例进一步读 patch/commit。
- 网页／中文：Exa 9 组检索，含 `GPT-6 skill 踩坑`、`gpt-6-astra skills AGENTS experience`、`GPT-6 技能 Codex`、`site:v2ex.com GPT-6`、`site:v2ex.com Astra 指令`、`GPT-6 skill 忽略`、`GPT-6 Superpowers`、`GPT-6 Astra skill headings`、`GPT-6 SKILL.md ignored`；另有代理独立的官方／英文检索。
- 中文原文读取：掘金、硬是要学、V2EX 相关帖子及评论、80aj。新闻转述未作为独立实验。
- 小红书：OpenCLI 的 `GPT6 skills` 和 `GPT-6 Astra` 两次结果均为空数组，只能报告本轮无返回。
- B 站：bili-cli 搜索 `GPT-6 skill` 网络连接失败，未据此判断平台没有内容。
- X／Reddit：已检查可用后端，但直接读取遇到 Failed to fetch；使用公开搜索、精确 URL 抓取及原始链接追溯补充。受限页面不会被描述为完整社区覆盖。
- V2EX API：两次主题详情调用超时，改读公开页面正文。发布日期以页面内可核对记录为准，避免索引日期污染。
- 已检查 Agent Reach 更新，当前 v1.5.0 为最新。没有安装升级、联系作者或发布评论。

本轮没有发现足以证明“所有 GPT-6 Skill 的统一最佳结构”的公开证据。发布初期的小样本与作者经验更适合作为可检验候选。研究结论的边界是已读来源，不是全网共识。

## 来源索引

[S1] https://github.com/obra/superpowers/pull/2258  
[S2] https://github.com/mattpocock/skills/issues/1053 ; https://github.com/amanthanvi/skills/pull/1  
[S3] https://github.com/mgelei/gpt-skills/issues/39 ; https://github.com/mgelei/gpt-skills/commit/252cf79f4ce78178f1adc367894ac32f05fac9df  
[S4] https://github.com/openai/codex/issues/42930  
[S5] https://github.com/mattpocock/skills/issues/530  
[S6] https://github.com/obra/superpowers/issues/2112 ; https://github.com/obra/superpowers/pull/1998  
[S7] https://github.com/obra/superpowers/issues/2260  
[S8] https://github.com/openai/codex/commit/5e32f728f1f86a967c6be057351f12505778df8f  
[S9] https://github.com/openai/openai-agents-python/blob/3e0e89374f629c974929054e56e823a43c91a013/.agents/skills/pr-draft-summary/SKILL.md  
[S10] https://www.v2ex.com/t/1239705  
[S11] https://note.com/masa_wunder/n/n2ab1006596b6  
[S12] https://developers.openai.com/codex/skills  
[S13] https://developers.openai.com/blog/skills-agents-sdk  
[S14] https://developers.openai.com/api/docs/guides/latest-model  
[S15] https://developers.openai.com/api/docs/guides/tools-skills ; https://developers.openai.com/cookbook/examples/skills_in_api  
[S16] https://developers.openai.com/blog/eval-skills  
[S17] https://www.youtube.com/watch?v=j2fG-zH6vgk ; https://moderncreator.app/2026-09-03-nerd-snipe-we-got-astra-first-now-we-re-fighting  
[S18] https://x.com/pvncher/status/2095991462416490862 （原帖正文读取受限）

临时原文与分工笔记保存在 /tmp；本文件为整合后的仓库研究交付。新增在线证据补充上一轮本地诊断，并不替代对历史失败任务的运行配置核对。
