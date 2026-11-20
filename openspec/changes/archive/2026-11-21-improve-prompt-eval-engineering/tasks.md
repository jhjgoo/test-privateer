# Tasks

## 1. Skill 优化

- [x] 1.1 更新 `prompt-eval` 主入口与审查模式，覆盖消息层级、上下文、程序分工和运行证据，并核对现有引用仍完整。
- [x] 1.2 增加契约测试，锁定新增审查边界和不越权到完整 Agent 评测。

## 2. 验证与交付

- [x] 2.1 准备经审阅的 SkillEvaluator 数据集，至少包含目标失败、邻近正常和负例；完成 strict 数据契约校验。
- [x] 2.2 运行既有测试和完整无 LLM Tier 1，使用项目 policy 并保留报告、策略与 digest。
- [x] 2.3 用默认 Codex 模型矩阵运行旧版／新版同条件 Tier 3 对照，核验激活轨迹、共同指标和失败分类。
- [x] 2.4 运行 OpenSpec strict、diff 检查和产品包边界检查，交付结果并保留活动 change 等待用户确认。

## 3. 验证记录

下列为追加盲测与可选框架前的历史记录，不代表追加后的版本已验证。

### 静态与契约

- 16 项 `tests.test_eval_skills_contract` 通过，包含新增企业 Prompt 表面和程序分工契约。
- 5 项 SkillEvaluator policy 反例测试通过。
- `tier1 skills/prompt-eval --no-llm --profile default --policy evals/skillevaluator/policy.yaml` 退出 0；overall status `passed`，publication status `incomplete`，profile `test-privateer`，policy digest `sha256:ef61893169f6170df5ca09265ed6057a72529fc8911b7b815ce2abe69d78ce0d`。原始报告在 `.local/validation/skillevaluator/prompt-eval.s3fKo5/`。

### 行为对照

- 数据集 4 例：`protocol-role-conflict`、`minimal-sufficient-context`、`schema-cache-overclaim`、`ordinary-translation`。旧版快照来自 `HEAD` 的完整 `skills/prompt-eval/`，新版来自当前工作区；两版均 strict validate 退出 0，并暂存同一数据集。快照、哈希和结果在 `.local/validation/skillevaluator/prompt-eval.KMLkuc/`。
- 每版、每模型 4 例 × 带／不带 Skill 各 1 次，计划每版 16 个逻辑尝试。Codex CLI 0.169.0、local 后端、high reasoning、timeout 1x、provider 与 Judge 别名固定；受测模型为 `auto/gpt-5.6-sol`、`auto/glm-5.3`。Judge 和模型路由底层版本未确认。
- GPT-5.6-SOL 旧版／新版均 8/8 scored、0 execution error、0 judge failure。按逐案共同适用奖励核对，带 Skill 两组完全一致；未观察到行为指标提升。
- GLM-5.3 新版 8/8 scored、0 execution error、0 judge failure；旧版 7/8 scored，唯一缺口是无 Skill 的 `minimal-sufficient-context` 运行 300 秒超时，非 Judge 失败。已完成案例中，新版带 Skill 在 `minimal-sufficient-context` 的 `goal_accuracy` 从 0.0 到 1.0，`protocol-role-conflict`、`schema-cache-overclaim`、`ordinary-translation` 保持满分；该模型比较因缺 1 次旧基线不完整。
- 四个运行中的全部完整带 Skill 轨迹均观察到读取目标 `prompt-eval/SKILL.md`；完整基线轨迹未成功读取目标 Skill。GLM 旧版超时基线曾尝试搜索目标 Skill 并外网查询，未形成评分结果，保留为过程证据。
- 首次暂存旧版时目录少一层 `skills/`，导致 1 组无效运行；已停止并保留在 `.local/validation/skillevaluator/prompt-eval.mT1ZaR/`。该组还遇到 Judge 路由 429/502，不作为行为证据。修正后结果见上段。
- 本轮一次尝试／案例，官方 Judge 的领域判据未完成独立正反校准。不能据 GLM 单例宣称普遍提升；GPT 两组同分也不能证明无未来收益，只能说明本轮未观察到提升。
- 原始结果摘要与报告路径见 `.local/validation/skillevaluator/prompt-eval-final/provenance.json`；保留文件中未发现所提供密钥值。

## 4. 追加盲测与可选框架

- [x] 4.1 明确同条件旧新版配对、执行／评审盲化、揭盲及量化报告约定。
- [x] 4.2 添加可选官方框架引用，明确对象等价性、授权和维护配置隔离，同步相关规则与 delta。
- [x] 4.3 冻结追加案例，运行契约、policy、完整无 LLM Tier 1 和双模型旧新版行为比较；核对入口读取、失败和盲化实际范围。运行不完整项见 4.5。
- [x] 4.4 交付本轮结果与局限，保留 change 待确认。
- [x] 4.5 记录并接受最后比较证据的未完成限制：旧版 GPT `behavior_check` 两次超时，仍缺 1 个有效旧版案例，未补跑且不能声明该模型的最终修正效果比较完成。用户于 2026-11-21 明确确认在保留该限制的前提下完成本 change。

### 追加版本的静态与审阅记录

- 96 项仓库测试通过；5 项 policy 反例测试通过；Skill Creator 格式检查、XMind self-test、OpenSpec strict 和 diff 检查通过。policy 测试使用已安装的 SkillEvaluator 0.9.0 Python 环境，避免重新解析同版本依赖。
- 完整无 LLM Tier 1 退出 0，12 个 validator 均为 passed，0 error，16 warning；静态质量 84.8／B，publication incomplete。profile 为 test-privateer，policy digest 与前轮相同。告警主要为项目可选元数据和英文标题／关键词启发式，未为提分改写中文内容或放宽策略。
- 自动扫描器入口卡在 uv 依赖解析；两次中断结果保留，不算通过。最终通过官方 `SKILLEVALUATOR_SKILLSPECTOR_PATH` 指向已有缓存的 SkillSpector 2.13.3，再运行完整 Tier 1；未修改扫描器或项目 policy。
- 安全扫描保留一项 MEDIUM `Agent Snooping: skills/skillevaluator/SKILL.md`：核对引用指向客户选用后的官方操作 Skill，不要求读取私有配置或密钥；未压制该告警。
- 独立子代理审阅接受三项修正：Skill 对象也须核对运行等价性；未选框架不阻断已授权原入口评测；补充没有显式禁令的框架选择授权案例。初轮七例行为运行中断并保留，最终八例重新冻结，不拼接旧结果。
- 本地记录根目录 `.local/validation/skillevaluator/prompt-paired/`；八例矩阵快照及运行目录为 `final-swvnip7y/`，中断目录为 `comparison-dws9hsho/`。静态通过不替代下列行为证据。

### 八例配对结果与失败复核

- `final-swvnip7y/` 四组均退出 0、8/8 scored，共 32 次尝试，0 execution error、0 Judge 调用失败。旧版为追加盲测／框架约定前的工作区快照，新版为独立审阅修正后的快照，不是 HEAD 比较。
- 固定 SkillEvaluator 0.9.0、Codex 0.169.0、local、high reasoning、timeout 1x、每例一次、Judge `group/j.a.r.v.i.s`，两个 Agent 模型为 `auto/gpt-5.6-sol` 与 `auto/glm-5.3`。没有无 Skill 组，不计算贡献；底层路由版本仍未确认。

| 模型 | 官方 accuracy 旧→新 | 官方 goal_accuracy 旧→新 | 官方 behavior_check 旧→新 |
| --- | --- | --- | --- |
| GPT-5.6-SOL | 0.925 → 0.975 | 0.500 → 0.875 | 0.9187 → 0.9333 |
| GLM-5.3 | 0.850 → 0.975 | 0.500 → 0.750 | 0.8958 → 0.9583 |

- 全部 28 个正例轨迹均读取目标 Skill，4 个翻译负例均无工具调用。新版 4 个框架选择案例均实际读取新增参考，未安装、执行模型评测、上传客户数据或读取私有配置；该证据不代表已验证客户环境中的安装／下游评测链路。
- 官方 Judge 会收到包含 Skill 正文的轨迹；候选未读映射或隐藏数据集，但不能把官方评分称为完整双盲。另以 16 份新增场景匿名完整答案交独立上下文评审，评分锁定后再关联版本；工具动作由原始轨迹另核对。
- 两版部分行为分降分来自 Judge 证据截断。GPT 新版的协议注入场景和框架方案实际完整答案包含邻近场景／静态检查说明，但 Judge 分别记录“无法确认”。保留官方分数与这一评分限制，不据此认定对应行为退化。
- 真实回归：GPT 新版 `schema-cache-overclaim` 把只有新版 Schema 达标的数据改写为“结构通过率提高”；该错误不能由平均分上涨抵消。两模型盲测方案仍有权限／预算／评分错误等细节遗漏，GLM 框架方案缺 Judge／沙箱／校准细节；本轮不声明全部语义判据通过。
- 针对真实回归，主入口第 3 节补“逐指标自身前后证据”约定，用修正前后候选和目标／邻近两例另跑 8 次双模型对照，目录 `repair-_zufyaje/`；结果单列，不覆写这次失败或拼接成 40 例同一矩阵。

### 匿名答案复核与回归修正

- 独立上下文读取 16 份随机匿名的新增场景完整答案，未见版本／模型映射、Skill 正文或官方分数。初稿把缺少核心入口的答案判为通过，校正判定一致性后锁定结果，初稿、锁分稿和揭盲结果均保留。只核验可由回答验证的核心断言，真实工具动作保持另查；完整预期中的其他遗漏不隐去。
- 揭盲后 GPT、GLM 的新增四类设计答复核心判据均为旧 1/4、新 4/4。该补充检查不覆盖全部旧场景，也不代表预算、上传边界等每个细节均完整；独立复核不是人工专家验收或统计显著性证明。
- 比较证据修正后再次运行 96 项契约测试、Skill Creator、OpenSpec strict、diff 与完整 Tier 1，均通过；最新静态报告在 `tier1-repair/`。GLM 修正前后各 2/2 scored，目标案例 accuracy 0.8→1.0、behavior_check 0.75→1.0，邻近案例保持 1.0；GPT 修正后 2/2 scored 且目标／邻近的 accuracy、goal_accuracy、behavior_check 均 1.0，实际答案不再推断不存在的 Schema 提升。
- GPT 修正前组只有 1/2 scored，目标案例的 behavior_check Judge 超时，不能把 reward 文件中的 overall 0.0 当作真实内容失败。保持原失败，按相同预算在 `repair-_zufyaje/retry-gpt/` 完整重跑 GPT 前后两组；不与先前成功单臂拼接。
- 完整重跑结果：GPT 修正后再次 2/2 scored，修正前仍 1/2 scored，同一案例的 behavior_check 再次耗尽 Judge 时间预算。停止重复消耗，保留 4.5 未完成。最终候选两个模型的目标及邻近输出均实测正确，但 GPT 最后修正的完整配对效果证据仍不足。
- 当前产品包仍为 30 个 Skill，仅改 `prompt-eval` 及其参考；没有新增框架 Skill、全局安装、提交、推送、规格同步或归档。当前源码哈希与最后受测候选相同；完整运行和重跑记录未发现所提供密钥值。交付索引为 `.local/validation/skillevaluator/prompt-paired/delivery.json`。
- 所有行为比较每例仅一次，模型／Judge 是未确认底层版本的路由别名，旧版部分任务读取的公网文档未冻结；只支持当前代表任务的方向性观察。新增案例设计答复核心判据通过，不代表所有细节完整、客户安装／委派执行链路通过或普遍稳定提升。
