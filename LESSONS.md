# 本项目错题本

记录真实返工、验证缺口和纠正办法；当前有效规则在 [AGENTS.md](AGENTS.md)，本文件保留事件、依据与状态。

## 本轮范围与统计

建立日期：2026-10-13。工作区为 `main`，已提交基线为 `7b47b88e69dd4efcb67bc59977b8ed9531c08ddc`；本次 Skill 与流程改动仍未提交。

本轮审查集合：当前 `maintain-project-lessons` 的 proposal、design、tasks、delta、评测判据和本地验证／审阅记录；本会话中用户对归档与默认规则位置的纠正；历史 `2026-10-10-improve-test-communication` 的 proposal、design、tasks 及 `evals/test-communication/README.md`。历史原始评测输出与全部提交 diff 未逐一读取，历史问题仅按可定位的归档记录回填，未重新执行其行为评测。

没有完整连续历史审查，因此**不设置 reviewed-through 水位**。下列次数按每条教训的独立事件统计；同一 change 的多个补丁、审阅意见与重跑不作为同类复发。用户已明确的约束和已有规格可以直接落实到 AGENTS.md，次数不作为落实这些要求的前置门槛；其他条目保持教训或候选，不因条数自动晋升。

## L-001 完成验证不等于用户确认 change 完成

- **事件：** `TP-20261013-ARCHIVE`，独立事件 1，审查日期 2026-10-13。本轮先按原仓库流程执行了归档；用户随后明确要求“不要自动 achive，需要用户确认才能本次 change 已完成”。同一 change 已恢复为活动状态，提前同步的新规格撤回并保留本地快照。
- **依据：** [活动 change 的恢复决定](openspec/changes/maintain-project-lessons/design.md#migration-plan)、[待确认任务与验收范围](openspec/changes/maintain-project-lessons/tasks.md#3-集成验收与用户确认)。恢复记录是本次事实，不能把补充要求倒写成事前已有约定。
- **机制与纠正：** 工具校验、任务完成与用户接受承担不同角色。今后严格校验通过也保持活动 change，直到取得用户对本次完成的明确确认；规则见 [变更与确认](AGENTS.md#变更与确认)。
- **状态与验证：** 用户明确约束已落实；本轮已核对活动目录与待确认任务。未建立自动拦截钩子，未来是否持续遵循尚未验证。恢复、补 delta 和再次校验都属于本事件，不增加次数。

## L-002 只验证文字回答，不能证明实际维护契约

- **事件：** `TP-20261013-EVAL-COVERAGE`，独立事件 1，审查日期 2026-10-13。首批四个输入全部要求只回复，无法观察 Skill 是否真的更新文件；晋升后再犯的判据也未明确要求合并编号、重算事件数及消解展示／写入边界。
- **依据：** [设计中的评测覆盖修正](openspec/changes/maintain-project-lessons/design.md#decisions)、[当前场景与判据](evals/project-lessons/cases.md)、[验收范围](openspec/changes/maintain-project-lessons/tasks.md#验收范围)。详细原始审阅留在 `.local/validation/project-lessons/review.md`，不随发布分发。
- **机制与纠正：** 文字建议正确仍可能掩盖未执行编辑或错误归并。补充临时复制品的授权维护，核对真实差异、源证据与无关条款保持、事件身份及有效规则；这是同一评测设计中的两项缺口，不拆成多次复发。规则见 [Skill 维护与验证](AGENTS.md#skill-维护与验证)。
- **状态与验证：** 判据已修正，既有规范与默认 AGENTS.md 两个文件维护分支均已实际执行并核对。无 Skill 与带 Skill 的四个文字输入都通过，因此没有前后提升证据；四例各组共享上下文的限制保留。这些通过不能证明长期防复发或跨宿主稳定。

## L-003 共享规则变了，模板与实际读取入口也要核对

- **事件：** `TP-20261010-SHARED-CONSUMERS`，历史变更记录 1，回填审查日期 2026-10-13。表达优化的归档记录指出：详细依据模板仍强制 Case 表格；执行计划候选只读主入口与方案检查，未读取共享表达。
- **依据：** [历史 design 的“首轮实际对照后的修正”](openspec/changes/archive/2026-10-10-improve-test-communication/design.md)、[历史验收任务](openspec/changes/archive/2026-10-10-improve-test-communication/tasks.md)、[真实入口与加载协议](evals/test-communication/README.md#当前协议)。本轮读取的是这些记录，未重新检查全部历史加载轨迹。
- **机制与纠正：** 共享参考存在不代表消费者已经读取，模板也可能继续强制旧约定。按实际消费链核对入口、被引用参考、模板和交付自校；在读取存在缺口时补指针，在规则矛盾时同步修正。规则见 [Skill 维护与验证](AGENTS.md#skill-维护与验证)。
- **状态与验证：** 归档记录报告已修正模板和主入口；当前文档规则已落实。本轮未重跑历史样本，也不根据一份归档总结虚构多个独立事故。后续改变共享参考时检查受影响消费者，不把此条变成全包无差别复测要求。

## L-004 精简不能删掉执行和判定所需的信息

- **事件：** `TP-20261010-CONCISION`，历史变更记录 1，回填审查日期 2026-10-13。[历史 proposal](openspec/changes/archive/2026-10-10-improve-test-communication/proposal.md#why) 明确记录此前短句化使 tasks 丢失执行信息；多个修订轮次仍属于该变更的观察，未逐轮计作复发。
- **依据：** [当前表达与用途规格](openspec/specs/test-artifact-quality/spec.md)、[task-plan 与相邻正常判据](evals/test-communication/README.md#固定输入与判据)。这些是已有项目契约，本轮不是再次验证其生成效果。
- **机制与纠正：** 字数减少不能替代用途验收。改写后按原任务核对前置、依赖、对象、动作、判据与失败处理；保持技术符号、条件与例外。规则见 [Skill 维护与验证](AGENTS.md#skill-维护与验证)，正常短答复仍不强制扩写。
- **状态与验证：** 历史记录报告已按 A/B 与用户评阅修正，当前规格与判据保留了相应要求；本轮仅回填与接入。历史局限及未稳定遵循的情况继续保留，不宣称已经根治。

## 正确做法与后续维护

本轮文字基线全部通过时，保留“未观察到提升”的结论；实际文件维护另行验证。历史表达优化保留原始生成稿和另存交付修订稿，[历史 proposal](openspec/changes/archive/2026-10-10-improve-test-communication/proposal.md) 明确不以人工改稿证明生成改善。评测证据规则见 [证据与工具](AGENTS.md#证据与工具)。

后续新增事件复用相关条目，补事件 ID、版本与证据；没有机制依据的相似现象先关联待查。已落实的规则再次被违反时，查入口是否可读、要求是否明确、验证是否行使对应路径，再决定修改位置；条目写好不等于自动防复发。历史全面审查仍未执行，本轮不以初始化账本关闭该范围。
