# Test Privateer 主流程与 Skill 分层优化实施计划

> **面向 AI 代理的工作者：** 必需子技能：使用 `superpowers:executing-plans` 逐任务执行此计划。步骤使用复选框（`- [ ]`）跟踪进度。

**目标：** 参考 Ask Matt 的主流程、旁路、词汇层和阶段边界，重组 Test Privateer 的入口编排，使不同 Agent 能稳定区分路径、阶段、handoff 和停止条件。

**架构：** 保留 `test-privateer` 作为用户显式入口；由它编排测试分析主航线，专项 Skill 只负责自己的阶段并返回统一 handoff。Codex 的隐性入口保持关闭，其他宿主不依赖文档模拟开关；宿主差异只通过真实配置和行为探针验证。

**技术栈：** Markdown Skill、Agent Skills frontmatter、Codex `agents/openai.yaml`、Codex CLI 行为探针、`quick_validate.py`。

---

## 文件清单

| 文件 | 职责 |
|---|---|
| `skills/test-privateer/SKILL.md` | 主流程、旁路、阶段边界和路线状态 |
| `skills/test-privateer/references/artifact-routing.md` | 产物归属、编号和统一 handoff 契约 |
| `skills/setting-test-mission/SKILL.md` | 使命阶段的 handoff |
| `skills/clarifying-test-basis/SKILL.md` | 澄清阶段的前沿、阻塞和返回主航线 |
| `skills/mapping-project-test-space/SKILL.md` | 项目地图阶段及下一阶段入口 |
| `skills/mapping-test-space/SKILL.md` | 有界测试空间旁路 |
| `skills/scanning-product-with-sfdipot/SKILL.md` | SFDIPOT 旁路 |
| `skills/analyzing-test-space-with-mfq/SKILL.md` | MFQ 旁路 |
| `skills/analyzing-change-for-testing/SKILL.md` | 变化分析阶段 |
| `skills/analyzing-product-risks/SKILL.md` | 风险聚焦阶段 |
| `skills/modeling-tests-with-ppdcs/SKILL.md` | PPDCS 建模阶段 |
| `skills/designing-test-experiments/SKILL.md` | 用例设计阶段 |
| `skills/designing-test-automation/SKILL.md` | 自动化设计旁路 |
| `skills/writing-unit-tests/SKILL.md` | 单元测试切片旁路 |
| `skills/challenging-test-designs/SKILL.md` | 终稿自校阶段 |
| `skills/running-test-sessions/SKILL.md` | 获准执行阶段 |
| `skills/investigating-findings/SKILL.md` | 观察／finding 旁路 |
| `skills/assessing-test-confidence/SKILL.md` | 证据判断阶段 |
| `skills/selecting-regression-tests/SKILL.md` | 回归保护旁路 |
| `skills/test-privateer/agents/openai.yaml` | Codex 主入口调用策略，保持显式启动 |
| `README.md`、`docs/guide.md` | 用户入口、安装和流程说明 |
| `docs/research/2026-09-09-test-privateer-p2-validation.md` | 记录探针命令和结果，不作为运行时规则 |

## 任务 1：冻结基线并建立行为探针

**文件：**

- 创建：`/tmp/test-privateer-structure-eval/` 下的临时 PRD、项目规则和控制提示；不写入仓库。
- 读取：当前所有活动 Skill 和 `agents/openai.yaml`。

- [ ] **步骤 1：记录当前基线**

保存当前主入口文件哈希、Skill 安装目录哈希、Codex 版本、模型和 reasoning effort。记录 GPT‑6 Astra 与 GPT‑5.6 Sol 的显式入口结果：是否提问路径、是否调用项目地图、是否写入 TCO、是否生成用例。

- [ ] **步骤 2：固定四类探针**

使用同一 PRD 和同一任务目录准备：显式入口、隐性入口、同一会话续接、新会话恢复。每个探针记录原始 JSONL、最终回复、工具调用、文件变化和退出码。

- [ ] **步骤 3：确认红灯**

当前预期红灯是：显式项目任务选择后直接写大篇分析、没有 handoff、没有阶段状态或没有真实产物。没有红灯证据的规则不在后续任务中新增。

## 任务 2：重写主入口为 Ask Matt 风格的分层流程

**文件：**

- 修改：`skills/test-privateer/SKILL.md`

- [ ] **步骤 1：保留入口契约**

保持主入口用户显式调用；`agents/openai.yaml` 的 `allow_implicit_invocation` 继续为 `false`。description 只保留职责和入口说明，不增加广泛触发词。

- [ ] **步骤 2：整理五层结构**

按以下顺序重排主入口：

```text
主航线：路径准备 → 澄清 → 项目地图/测试空间 → 变化分析 → 风险 → 建模 → 用例 → 自校 → 执行 → 信心
旁路：使命不清、finding、回归、自动化、单元测试、超大项目
词汇层：SFDIPOT、MFQ、PPDCS、TCON、oracle
阶段边界：继续、handoff、等待、执行授权
前置条件：项目规则、TCO、需求资产和权限
```

保留现有业务规则和安全边界，只调整结构和行动表达。

- [ ] **步骤 3：明确阶段门槛**

每个阶段写清“进入条件 → 调用 Skill → 产物 → 下一阶段 → 停止条件”。项目任务必须经过项目地图和变化分析；用户没有要求用例时停在分析/模型边界；未授权不能进入执行。

- [ ] **步骤 4：保留路线状态**

保留当前简短路线状态模板，但把它与每阶段 handoff 关联，避免状态只是展示文字而不影响下一动作。

## 任务 3：统一 handoff 和直接调用边界

**文件：**

- 修改：`skills/test-privateer/references/artifact-routing.md`
- 修改：任务 1 文件清单中的所有专项 Skill

- [ ] **步骤 1：固定 handoff 字段**

统一使用：`当前阶段`、`已完成`、`未完成`、`证据与产物`、`阻塞`、`下一动作`、`执行许可`。

- [ ] **步骤 2：更新专项 Skill 交付段**

每个专项 Skill 增加一句：直接用户调用时交付自身产物后停止；被主入口调用时返回 handoff，不进入未授权的下一专题。

- [ ] **步骤 3：区分阶段完成与整条链完成**

项目地图完成不代表变化分析完成；分析完成不代表用例完成；用例完成不代表执行通过。完成条件使用当前阶段名称，主入口负责汇总全局状态。

## 任务 4：收紧澄清前沿但保持简洁

**文件：**

- 修改：`skills/clarifying-test-basis/SKILL.md`

- [ ] **步骤 1：保留当前短判断**

保留“会改变范围、模型、风险重点或 oracle 就先澄清，否则记录后继续”的短规则。

- [ ] **步骤 2：明确回到原阶段**

用户回答后，澄清 Skill 返回认知变化、受影响测试和原路线的下一动作，不重新扫描整份需求。

- [ ] **步骤 3：验证 GPT‑5.6**

用一个包含明确快照时点未知的 PRD 探针，确认它先提问；用一个只有已知事实的 PRD 探针，确认它直接分析，不制造问题。

## 任务 5：优化 P2 宿主入口配置

**文件：**

- 修改：`skills/test-privateer/SKILL.md` frontmatter
- 修改：`skills/test-privateer/agents/openai.yaml`
- 修改：`README.md`、`docs/guide.md`

- [ ] **步骤 1：保持 Codex 主入口显式**

`allow_implicit_invocation: false` 作为 Codex 的真实策略，避免普通代码、回滚和一般分析误触发测试流程。

- [ ] **步骤 2：保持标准 frontmatter**

不把宿主私有字段塞进标准 `SKILL.md` frontmatter。description 使用 Ask Matt 风格的短职责描述，避免暴力触发词。

- [ ] **步骤 3：补入口说明**

README 和教程说明：主入口显式启动；同一任务沿 handoff 续接；新会话提供阶段状态和产物路径。不要把宿主差异写成运行时规则。

## 任务 6：终稿自校、验证和发布前检查

**文件：**

- 修改：`docs/research/2026-09-09-test-privateer-p2-validation.md`
- 验证：所有 Skill、README、教程、相对链接和本地安装目录

- [ ] **步骤 1：运行 Skill 校验**

运行：

```bash
/Users/jianghongjian/.agent-reach-venv/bin/python /Users/jianghongjian/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/test-privateer
```

再对 18 个 Skill 全量运行同一校验，预期全部通过。

- [ ] **步骤 2：同步本地安装**

将项目 `skills/` 同步到 `/Users/jianghongjian/.agents/skills/`，删除项目已移除的旧文件，逐文件比较字节内容。

- [ ] **步骤 3：运行模型回归**

至少运行 GPT‑5.6 Sol 的显式入口、同会话续接和澄清前沿探针；GPT‑6 仅作为观察性回归，不把 GPT‑6 结果作为本轮阻塞。

- [ ] **步骤 4：核对真实产物**

确认项目任务产生 TCO/分析文件时，路径存在、链接闭合、编号关联同步、未执行内容没有冒充结果；无写入权限时回复明确未写入原因。

- [ ] **步骤 5：形成一个提交**

提交 Skill、模板、README、教程和必要验证记录；不提交模型原始提示词、临时 `/tmp` 产物或宿主会话日志。

## 回滚策略

每个任务使用独立提交；如果主流程让 GPT‑5.6 出现过度提问、重复扫描或无故停止，先回滚任务 2，再保留 handoff 契约和验证报告单独评估。不要用更多规则覆盖行为回归。

## 计划完成条件

- 主入口结构能像 Ask Matt 一样回答“现在在哪条路线、下一步调用谁、何时停止”；
- 专项 Skill 能返回统一 handoff；
- GPT‑5.6 对高影响未知先澄清，对非阻塞未知继续分析；
- 显式主入口策略在 Codex 与标准 frontmatter 上保持一致；
- 18 个 Skill 校验通过，本地安装一致，项目产物路径可核对；
- GPT‑6 观察性结果单独记录，不改变 GPT‑5.6 的发布判断。
