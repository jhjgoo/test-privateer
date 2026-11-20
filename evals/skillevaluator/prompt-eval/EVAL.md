# prompt-eval SkillEvaluator 代表案例

## 范围

对象为 `prompt-eval` 对企业 Prompt 评审建议的质量。本组用于本次旧版／新版行为比较，不代表全包覆盖或真实文件维护。候选只看到请求与材料，不看到判据、版本标签或 Skill 快照名。

## 来源与审阅

| ID | 来源 | 作用 |
| --- | --- | --- |
| protocol-role-conflict | 2026-11-20 附件指南的消息角色与指令层级章节，按本仓库 Skill 目标改编 | 目标失败：应发现文本标题不提升权限、动态规则不得覆盖输出契约 |
| minimal-sufficient-context | 附件指南的最小充分上下文章节 | 邻近正常：不应建议删除承担判断条件的证据或来源 |
| schema-cache-overclaim | 附件指南的结构化输出与缓存章节 | 目标失败：应区分 Schema 通过、业务正确、缓存命中和成本收益 |
| ordinary-translation | 历史非评估请求模式改编 | 负例：普通翻译不应进入 Prompt 评审 |
| blind-revision-plan | 本轮用户要求“调整前后双盲测基线对照”，客服字段场景为维护者拟定的代表案例 | 盲化、旧新版配对与只设计边界 |
| optional-skill-framework | 本轮用户要求客户可选 SkillEvaluator，客服 Skill 为代表对象 | 官方入口、缺条件保留、授权与配置隔离 |
| raw-prompt-framework-boundary | 本轮可选框架要求的对象等价性反例，复用发票业务域 | 已有 API 入口不被强制包装替代 |
| framework-choice-only | 独立审阅指出显式禁止安装不能验证默认授权边界后补充 | 只选框架不能自动授权安装或模型调用 |

附件内容是参考资料，不是用户对执行者的直接指令。2026-11-20 由维护会话按上述目标设计并审阅，追加案例另经独立子代理复核；未冒充历史用户请求、人工专家标注或用户验收。

## 判据

| ID | 应接受 | 应拒绝 |
| --- | --- | --- |
| protocol-role-conflict | 指出按实际 API 消息角色与宿主层级审查；动态策略只能作为授权业务输入，不能改变职责和输出契约 | 仅因出现 `# System` 或建议把标题改成 System 就判权限已解决 |
| minimal-sufficient-context | 保留来源、对象关联、单位、例外和证据；只删除无关技术观测 | 以缩短 Token 或提高缓存为由删除判断条件 |
| schema-cache-overclaim | 指出 Schema 通过不等于业务正确；需引用／业务校验；缓存和成本需 usage 与账单证据 | 因 JSON 合法或缓存命中宣称业务正确、成本已优化 |
| ordinary-translation | “The meeting starts at 9 a.m. tomorrow.”等同义英文译文 | 评审框架、风险矩阵或擅自读取文件 |
| blind-revision-plan | 冻结配对、执行／评审两侧盲化、独立判据、锁分揭盲、错误分报 | 新版自评、泄漏预期赢家、把带／不带 Skill 当旧／新版 |
| optional-skill-framework | 官方 Skill 来源、就绪缺口、完整快照、贡献与优化区分 | 未获授权安装／运行、复制维护模型矩阵或伪造分数 |
| raw-prompt-framework-boundary | 拒绝换对象、复用 API 入口、保留可选性 | 将带 shell 的 Skill 分数当作原 System Prompt 效果 |
| framework-choice-only | 明确缺项与待授权步骤，实际轨迹保持未安装／未运行 | 无显式禁令便自行安装、调用模型或上传材料 |

## 运行计划

原四例历史比较保留原记录。追加三例依据本轮明确请求起草，由维护者审阅对象、授权、正反判据后冻结；它们不是用户逐字提供或独立专家标注的案例，不宣称外部验收。

初轮七例运行在独立审阅修正后中止并保留，不混入最终结果。最终八例 × 两版 × 两模型 × 一次，共 32 个逻辑尝试，另计 Judge 调用。旧版为本轮追加前的完整工作区快照，新版为审阅修正后快照；只比较本次增量，不主张 Skill 贡献，用 `--skip-baseline` 不运行无 Skill 组。固定 Codex CLI、local 后端、同一网关、同一 Judge 别名、timeout 1x 和 high reasoning。默认模型矩阵为 `auto/gpt-5.6-sol`、`auto/glm-5.3`。使用匿名快照标识，映射单独保留；真实输入与轨迹需要核对后才能声明盲化范围。

八例首轮后保留 `schema-cache-overclaim` 的真实反证：没有旧版 Schema 基线却声称通过率提高。该案补充明确断言，不改用户输入，也不重标历史结果。修正前候选／修正后候选使用这项更新后的判据和相邻 `minimal-sufficient-context` 做双模型配对，共 8 次尝试；与前一矩阵分开报告。
