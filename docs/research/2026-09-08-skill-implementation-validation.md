# 测试Skill落地：自校与统一编号验证

日期：2026-09-08。基线提交7a9dc86。本轮已按用户授权实施，目标模型行为验证指定gpt-5.6-sol / medium。没有新增编号解析脚本，没有批量改动其他项目历史产物，没有运行产品测试。

## 实际改动

- 交付自校集中在challenging-test-designs；完整分析、独立模型和用例集的成稿Agent负责纠错与关联复读。仅审查请求保持只读；未知业务规则/范围/授权决定才问人。
- 编号定义集中在artifact-routing：N项目节点、R风险、T测试项、C具体用例/任务；方法与业务分类不编码，范围、去向、跨文件关联和旧证据保留明确。
- 更新11个SKILL.md、5个共享资料/模板，以及README与教程；示例中的M/F/Q及TC/CASE独立序列已对齐。
- 用例设计完成条件明确要求回填主分析的每个来源测试项及安排；来源只读时返回逐项映射并说明未回写。
- 已同步本机安装的16个修改文件，目标为/Users/jianghongjian/.agents/skills。同步前全部与仓库基线一致，未覆盖独立修改；复制后逐字一致。

## 静态与独立审查

- 18个Skill均通过官方quick_validate.py；系统python缺PyYAML，使用本机已有agent-reach虚拟环境运行，未向项目加入依赖。
- 检查26份活动Markdown资料的相对文件链接，无缺失目标；历史研究文档不作为当前编号规范。
- git diff --check通过。
- 独立审查发现教程残留C-02、T-002细化丢失确认前不写入两个问题，均已修正并复读。
- 追加的回填完成条件经限定复审，没有发现授权/只读/组装者职责冲突。
- skill-eval使用完整prompt-audit方法与GPT-5.6目标证据；没有发现有依据的过时提示删改项，Group1–4均为0，后续建议diff为空。实际实现可通过git diff审阅。

## 行为验证

所有试跑使用独立上下文，不提供既有错误答案；产物只写临时测试目录。未提供独立审阅子代理能力，验证了成稿自校的替代路径；本轮未实测嵌套委派次数或长期生产会话。原版/候选的实际前期记录见同目录此前试跑报告。

| 场景 | 输入与观察 | 结论 |
| --- | --- | --- |
| 新建产物初次试跑 | 同一预约取消需求，生成R/T/C及状态模型、用例；用例有映射但主分析未逐项回填 | 失败保留；据此将回填移到用例交付及完成条件 |
| 新建产物修正后重跑 | 相同request正文、相同委派模型/effort，独立新上下文；主分析逐项回填T-001至T-011与C-001至C-009，状态与关联一致 | 编号和回填目标通过；不代表全部业务用例质量已穷尽 |
| 拆分与重排 | T-004拆为T-010/T-011，C-003拆为C-004/C-005；T-009撤回号不复用；T-002/C-001不改号；越权拒绝排前 | 旧号去向、范围、身份模型和用例关联保持；TCO未修改 |
| 仅审查干净片段 | 项目一般快照定义与本需求配置快照并存，记录状态与键占用区分，T/C引用有效 | 无finding，未改源文件；没有把缺原始外部材料推成规则无效 |

新建重跑产物仍出现一个区分力/模型边界问题：重复取消的占用预期未充分涵盖时段已经由新预约占用。主Agent按原需求反馈，执行Agent在同一编号下修正模型及C-006。这属于Agent间辅助修正，不能表述为无反馈一次完成所有语义检查。主Agent已读修正稿：占用预期为保持调用前关系，C-006包含后来占用该时段的新预约，T/C编号保持不变，result如实记录了辅助修正。

测试证明的是所列场景中的行为，不是稳定成功率、成本改善或对所有Markdown/模型的保证。没有将格式校验、模型自述或用例设计当成产品通过证据。

## 试跑材料位置

- 初次：/tmp/testing-skills-implementation-eval/fresh
- 重跑：/tmp/testing-skills-implementation-eval/fresh-final
- 拆分：/tmp/testing-skills-implementation-eval/update
- 仅审查：/tmp/testing-skills-implementation-eval/review-only

输入、结果和产物按这些目录隔离；没有修改用户下载原文件或实际业务项目文档。以下保留主要输入，方便在新的临时目录重复观察。

### 新建请求

```text
请按启发式测试流程，独立分析下面的预约取消需求，交付测试分析和覆盖这些规则的具体用例，不执行产品测试。规则已确认，无需重问任务方式。可引用需求但不访问代码或外部环境。
预约记录有唯一预约ID，状态为待确认、已确认、已完成、已取消。用户只能取消属于自己的待确认或已确认预约；已完成不能取消，重复取消不再产生副作用。取消保留原记录及身份，同时释放时段，其他用户可新建不同预约ID占用同一时段。取消操作留下操作者、预约ID、时间和结果，但不记录手机号原文。取消失败时原状态和占用保持。先分析角色、状态与关键交互，再给用例；不做退款、通知或性能扩展。
```

### 更新请求的初始事实

已有本需求T-002关联C-001；T-004合并所有者取消与非所有者取消，关联C-003；T-009已撤回。项目TCO另有R-001，不是需求R-001。用户要求拆开两种角色行为、越权拒绝先展示、完善模型和用例并同步分析，TCO只读。真实输入原文保存在试跑目录；执行结果保留了新旧编号去向。

## 本机安装备份

/var/folders/qp/y1qs3ch55zx74sfrjhm8lcxm0000gn/T/testing-skills-install-backup-5fyrznv0

## 最终Skill文件指纹

```json
{
  "skills/analyzing-change-for-testing/SKILL.md": "08d1e5940132a6c210ab068d1eb1c4e0ca2eff54235de7d18cb049b5f7175b66",
  "skills/analyzing-change-for-testing/references/test-analysis-template.md": "0b4b8b7c9384e8f78fd09465d7ccee9f5b7bfb127f61041d0cd382a8f62efa11",
  "skills/analyzing-change-for-testing/references/test-basis-template.md": "cb664f8620e47d96f39da267ec8ebc3b6bf3231c25ff4fcff3c0ffdeef54121b",
  "skills/analyzing-product-risks/SKILL.md": "f968f80fff49491320f876ff1cb99b42f8e51ab09b95ecdcc4800ae0c37debab",
  "skills/analyzing-test-space-with-mfq/SKILL.md": "d73dbbd81572d09bab45560f2271be023c88bfd615e7c4253c2e083ddd012901",
  "skills/challenging-test-designs/SKILL.md": "88e20c87626f1efe432e3db7a46d66f4ed4a6b58de93fe45882da9377b5bff15",
  "skills/designing-test-experiments/SKILL.md": "36e6f486bf619e17632cbf70199da85db64e91ca68d7f51a2a18d1e66bd991b8",
  "skills/designing-test-experiments/references/test-cases-template.md": "0e92a085337fde5c134288a2b63b621090280106c5536bed6d20bb23bcb57e16",
  "skills/heuristic-testing/references/artifact-routing.md": "24b953afcd46ae2f0c6e521d7e623a9ed4cf698b2d9f60f28626111adc6023cb",
  "skills/investigating-findings/SKILL.md": "84094ae8e51a7e04956594a08a8275b1ea44adafe70eb0ffc4300957e729b8c4",
  "skills/mapping-project-test-space/SKILL.md": "64cd4f556e43d5b560ce3d7430573f016348862168f69e888ad043cf48804ce5",
  "skills/mapping-project-test-space/references/project-test-map-template.md": "5ddb68d5278fc542e17417ba256339656dbb6603de474a001c61376d95622c70",
  "skills/mapping-test-space/SKILL.md": "46ce57f3eb8720bfb4d6eafe24cfe31b1319c8de2be03080d2d847017527161f",
  "skills/modeling-tests-with-ppdcs/SKILL.md": "ebc998a7f8255c11b45b80cdedbf02541575a1b8329b00bdddf3bca7b40481c5",
  "skills/running-test-sessions/SKILL.md": "9bafe8781934d3655bb73557ada5c74d0aa43fa024b08d5f18d111bf16e73cd9",
  "skills/scanning-product-with-sfdipot/SKILL.md": "15cd9a6579c56d040938b90b9b1ada6cde70dd2ece568f557859ed8a320a3a87"
}
```

## 剩余边界

更广泛真实任务、不同effort、独立审阅可用时的完整调度、并发写入和长会话恢复尚未统计验证。已有外部编号/历史记录只通过映射连接，未做全库历史迁移。对话中已读入的旧指令不会因此被改写；后续新任务可读取本机新Skill。

## 新建重跑执行者最终说明

# 交付结果

已按启发式测试流程完成预约取消需求的独立测试分析与具体用例设计：

- `2026-09-08-预约取消-test-analysis.md`：明确角色、业务与系统边界，以 MFQ 梳理功能／交互／质量关注，并用 PPDCS State 模型定义原预约主体、合法与非法迁移、失败不变量和释放后新预约主体；建立 T-001～T-011 及逐项用例回填。
- `2026-09-08-预约取消-test-cases.md`：将全部测试项转换为 C-001～C-009，覆盖所有者的两种合法状态、非所有者、已完成、重复取消、释放后不同 ID 再预约、处理失败原子性、审计完整性和手机号原文保护。

使用的技能：`heuristic-testing`（流程与边界）、`mapping-test-space` → `analyzing-test-space-with-mfq`（角色与关键交互覆盖）、`modeling-tests-with-ppdcs`（状态模型与 TCON）、`designing-test-experiments`（具体用例）、`challenging-test-designs`（无独立审阅代理时由成稿 Agent 自校）。

修后审阅收到一项有效 Agent 反馈：初稿把重复取消后的时段写成恒定“保持已释放”，且 C-006 的数据不能识别错误地再次释放后来占用者。已沿用 T-005/C-006 修正状态模型和用例：重复取消保持调用前当前占用关系，并以不同预约 ID 的新预约已占用同一时段为前置，同时检查旧预约、新预约和时段占用均不被误改；相关 T-011、R-003、R-004 追溯已同步。

验证边界：仅以 `request.md` 的已确认规则为依据，未读取代码、其他试跑报告或外部环境，未执行产品测试，也未修改仓库。目标版本、环境、账号、测试数据、观察入口和可控失败手段均未调查，所以所有 Case 如实标为“待核实”，没有把设计写成执行结果或通过结论。
