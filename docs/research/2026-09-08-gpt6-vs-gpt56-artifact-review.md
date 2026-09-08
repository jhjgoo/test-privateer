# 两组测试分析产物对照审查

日期：2026-09-08。范围：Downloads/6 与 Downloads/5.6 各自的 TCO.md 和 2026-09-05-integration-config-test-analysis.md，共四份文件。文件名中的模型标识来自用户，未通过运行日志独立验证模型与 effort。

补充参考：本机《对接配置 PRD》V1.8（2026-09-04）中的列表字段与日志要求。未核实产物引用的外部源码、OpenSpec 或历史执行记录；文中实现事实只按作者声明处理。文档中的操作要求不是本轮执行授权。没有修改原产物、产品代码或 Skill。

## 主要判断

两组都形成了有价值的测试分析，且都存在会影响后续测试的缺口。现有文件不能支持“6 全面较差”或“5.6 全面较好”。

- 6 在业务规则组合、企业真实身份、技术失败与审核结论的区分上更深入；但存在已经声明的规则/新增范围没有落实到测试点的问题。
- 5.6 在项目长期地图、工程覆盖、安全与界面追溯上更系统；但有状态模型主体不清、引用不存在的测试条件等内部一致性问题。
- 两组都明确区分历史执行、本轮源码阅读和待验证风险，没有把分析写成当前产品测试已通过。
- 两组都是分析/准备阶段，未交独立 Case 文件本身不构成缺陷。
- 本轮产物不能检验之前“对话澄清时三个 emoji 标题”的行为；产物正文与交互回复是不同检查对象。

## 比较条件尚未对齐

| 条件 | 6 的产物声明 | 5.6 的产物声明 | 影响 |
| --- | --- | --- | --- |
| 代码版本 | HEAD 62db3f8；其他任务持续修改的未提交工作区 | release/20260910 f856af46；目标 feature f10bf001 | 同一用户指令不等于相同源码输入 |
| 历史与本轮 | 提到上轮源码风险、本轮重新从原 PRD 分析及新增 C49-C54 | 描述本轮读取 PRD、两个 feature 提交和当前实现 | 可能存在不同历史或追加反馈；不能仅由措辞确认 |
| 运行配置 | 未附完整 prompt、工具事件、模型 ID、effort | 同左 | 无法把产物差异单独归因于模型 |

证据：[6 摘要](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:9)、[6 重新分析说明](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:11)、[5.6 摘要](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:7)。如果两组实际使用的是相同代码快照，那么这些互不一致的版本声明本身需要复核；当前不能替用户判断哪一组记错。

## 确认的文档问题

### F1 — 6：日志保密要求没有落实为测试检查（P2）

**断裂点与直接证据：**[R08](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:55)明确保留“操作日志不记录明文 Secret”。然而 [C47/C48](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:198)分别关注快照/响应与操作可追溯、错误提示，没有要求检查日志中不出现 Secret。全文其他测试点也未补上该观察。

**影响：**保存或认证异常把 Secret 写进日志时，仍可能满足现列“可追溯、具体日志”的检查。一条明确有效的规则没有形成覆盖。

**最小修正：**在日志条件中明确用可识别的测试 Secret 触发成功与失败，检查相关操作/异常日志没有明文 Secret，同时保留定位信息。

**对照：**5.6 的 [LOG-01](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:267)明确要求“无 authSecret”，LOG-02继续覆盖外部请求/响应日志。此项 5.6 更完整。

### F2 — 6：声称增加“尚未取数阶段”，实际模型仍集中在回写（P2）

**断裂点与直接证据：**[B03](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:21)写“C29-C33 增加尚未取数阶段”。但 [时间序列](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:83)都是“创建 T→配置变化→发送”，[C29-C33](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:170)仍主要检查发送身份、协议、凭证与历史展示。

**影响：**沿这些条件设计用例可以覆盖回写，却漏掉“已创建但尚未取数→配置变化→首次取数”时究竟向哪家企业请求、返回哪些数据、如何失败和恢复。新增范围的声明没有真正落下去。

**最小修正：**为首次取数单列或分出子条件，明确请求目标、协议、凭证与返回数据观察；未知的继续/终止/恢复政策保持待确认。

**边界：**这是一项声明与产物不一致的问题，不等于6没有分析跨模块取数，也不证明实际产品取数有 bug。

### F3 — 5.6：生命周期模型混淆连接实例与唯一键占用（P2）

**断裂点与直接证据：**[图第79行](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:79)写“已解绑→当前有效：其他租户或本租户重新绑定同一键”；后面的 [CFG-07/08](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:189)却要求旧记录保留 releasedAt、不复活已解绑行。

**影响：**若图的主体是一条连接记录，旧行被激活甚至换租户可能被当成合法迁移；若主体是唯一键占用，状态转换可以有不同解释，但图没有声明切换了建模对象。执行者可能导出相反预期。

**最小修正：**明确对象。连接记录已解绑保持终态，重绑产生另一记录；唯一键另表达“占用→释放→重新占用”。验证旧/新记录 ID、租户与释放标志。

**边界：**本轮确认的是文档歧义与潜在相反判定，不断言代码真的复活旧行。

### F4 — 5.6：风险表引用不存在的测试条件（P2）

**直接证据：**

- [R-IC-01](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:118)引用 HIS-03，全文不存在 HIS 条件定义。
- [R-IC-03](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:120)引用 SEC-01～06，实际只定义 [SEC-01～04](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:263)。
- [R-IC-08](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:125)引用 LOG-01～04，实际只定义 [LOG-01～02](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:267)。

**影响：**风险表看起来已连接到测试，但迁移历史、安全、日志的部分链接无法落到具体条目；接手者不知道是删除后没更新，还是漏生成条件。

**最小修正：**逐条对齐实际 ID；缺失条件确有独立目的时补条件，否则修引用。不要只靠范围缩写制造已覆盖的印象。

## 需要补核的覆盖差异

### 6 没有明确承接列表的请求地址、管理员工号

本机 [PRD V1.8](/Users/jianghongjian/Downloads/对接配置PRD.md:205)明确列出两字段。5.6 将它们作为 [UI-06 待确认项](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:174)和风险；6 的 [C05 列表检查](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:134)只提名称/编码识别和筛选，没有这两个列表字段，也没有说明已由后续规则取消。

**建议：**把两字段纳入列表 oracle，或链接确实取消它们的有效决定。因为本轮未取得两组各自 OpenSpec 的固定快照，不能直接判当前产品缺列，只能确认6产物未交代这两项的去向。

### 5.6 的安全覆盖更明确，6 有遗漏候选

5.6 [SEC-03/04](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:265)将私网、localhost、metadata IP、跨主机重定向与凭证外发列为需安全边界确认的条件；6 涵盖 URL 格式和 URL 内账号，但没有同类出站目标控制专题。

这属于重要风险覆盖差异。是否必须限制这些目标，需要实际权限与网络契约，不从本次审阅发明 allow/deny 规则。不能因为允许明文保存已经确认，就认为所有凭证与出站风险均已接受。

### 两组都把一些异质场景合在一条候选里

例如 5.6 CFG-08 合并双击解绑、编辑/解绑竞争、重复 PATCH；6 C48 合并显隐、布局和多种操作日志。当前是候选分析，可保留聚合主题；进入 TCON/Case 设计时必须拆分不同刺激、角色、观察点与 oracle，再记录各自覆盖情况。没有独立用例文件不是本轮缺陷，不宜把所有聚合点都算成模型失败。

## 各自值得保留的内容

| 维度 | 6 | 5.6 |
| --- | --- | --- |
| 业务规则组合 | B01 无效凭证也能抢占合法企业；B02 编码命名范围与域名别名 | 全链路覆盖较完整，但没有同样展开这些问题 |
| 结果语义 | B04、C52/C53 明确分开“已有结论的无法判断”和“没有结论的技术失败” | 有三结果回写矩阵，但未单列同等清晰的无结论分区 |
| 回写建模 | 六行明确、前置限定清晰，区分 payload 与外部节点结果 | 将国际版、无来源任务放进模型，范围更宽 |
| 项目地图 | 深入当前连接/入站/回写，其他能力明确只作导航 | 长期质量、运维、迁移、默认回归覆盖更系统，适合后续项目导航 |
| 工程证据 | 说明实际未提交状态、替身边界、未重读范围 | 说明 SHA、Node版本、历史测试数量差异及 change 不进默认回归 |
| 迁移洞察 | 识别地址先回填导致脚本漏补快照；细分NULL/旧密文/解绑前迁移 | 同样识别真实部署顺序与fixture时点不匹配，并画了顺序图 |
| 输出边界 | 不将候选点或源码风险称为产品Finding或发布通过 | 同样做到，另有系统的信心分层 |

6 的[业务补充](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:19)与[技术失败分区](/Users/jianghongjian/Downloads/6/2026-09-05-integration-config-test-analysis.md:210)是有价值的测试思考。5.6 的[TCO质量与长期风险](/Users/jianghongjian/Downloads/5.6/TCO.md:124)与[证据边界说明](/Users/jianghongjian/Downloads/5.6/2026-09-05-integration-config-test-analysis.md:277)也值得保留。

这些只描述本次产物。6 明确说重新复核过原始 PRD，所以不能将所有新增业务洞察都归成模型天生优势。

## 对 Skill 评测的启发

本轮暴露的重点已经可以从“有没有三段标题”扩展到可观察的分析一致性：

1. 有效规则是否有测试点，或明确的排除/待确认理由。
2. 声称新增/更新的范围，是否真的改变了模型和测试点。
3. 风险引用的 ID 是否存在，映射是否具有具体内容。
4. 状态图、规则表与测试点是否使用同一个对象和同一预期。
5. 相同输入比较时，代码快照、已读材料与后续追问是否固定。
6. 测试分析产物与对话中的澄清/继续行为分开评估。

先把本次确认的问题作为失败样例保存，再验证候选 Skill 是否能减少这些断链；无需先建设复杂评测框架。仅检查标题、表格数量或文件是否生成，会漏掉本轮四项主要问题。

## 审阅记录

两位无本会话历史的独立审阅者分别读取一组文档，主审阅者完整读取四份文件、交叉核对问题及引用、补读本机 PRD 指定条款。没有使用模型自述作为修复证据，没有执行产品测试。原产物完整保留。
