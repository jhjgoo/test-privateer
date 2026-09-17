# Prompt Eval 与 Agent Eval Skill 验证

日期：2026-09-17。目标请求模型：`gpt-6-astra`，reasoning high。源码分支：`codex/prompt-agent-eval-skills`。

## 范围

新增 `prompt-eval`、`agent-eval` 及三份按需参考；修改 `test-privateer` 路由、README 和研发教程。没有新增评测平台、依赖、自动化运行脚本或产品执行能力。

## 静态验证

- `tests/test_eval_skills_contract.py` 先在文件缺失和路由缺失时失败，再在实现后4项通过；覆盖 frontmatter、引用、模型适配归属、Agent质检边界和文档路由。
- `git diff --check` 通过。
- Skill Creator 的 `quick_validate.py` 两次尝试均因运行环境缺少 `PyYAML` 在导入阶段失败；没有把该环境错误记作 Skill 失败，也没有为验证临时增加项目依赖。契约测试检查了本仓库采用的单行 frontmatter 子集：起止分隔符、`name`、非空 `description`、字段行和引用存在性；它不替代通用 YAML 解析器。

## 行为验证

五个合成场景均使用新目录、新会话、本地 Skill 快照、read-only sandbox；评审标准未提供给受测 Agent。原始最终回复、事件、stderr 文本和退出状态保存在 `evals/prompt-agent-eval/runs/2026-09-17/`。

| 场景 | 结果 | 观察 |
| --- | --- | --- |
| Prompt误调用与虚假成功 | PASS | 定位“积极调用”和缺失成功证据条件；给最小替换、正常查询、政策问答、混合请求和失败边界；未声称已优化 |
| Prompt配置不足 | PASS | 补业务目标与来源追溯；目标模型、宿主和工具未知时不编适配结论，不强制格式 |
| Agent评估方案质检 | PASS | 识别字符串Oracle、全是应退款、单次运行、503归因错误和未校准同模型Judge；给工具无关补测设计，未搭平台 |
| 普通订单测试分析 | PASS | 进入常规测试重点，未路由到Prompt／Agent评估，也未展开评测方法论 |
| Agent失败交接Prompt | PASS | 根据完整trace定位错误System Prompt；输出失败场景、目标／实际、直接证据、Prompt位置、邻近场景和验证方式 |

五次进程退出均为0。CLI报告目标模型元数据缺失并使用回退元数据、技能描述预算压缩及插件缓存警告，因此模型名只表示请求配置，不证明服务端实际型号。本轮每个场景仅运行一次，是边界冒烟检查，不支持稳定成功率。

## Skill Eval

提示面包括两个新入口、三份参考、主路由和文档。目标是当前模型／宿主下的行为质量，不把迁移当独立流程。

- **Group 1：** 未加入“必须全面”“永远”“固定轮次”等压力语言；精确步骤只用于证据、权限和完成判断。Prompt审查模式是按需参考，不是强制检查表。
- **Group 2：** 两个 Skill 有独立触发词与任务边界；共享测试原则没有复制成第三个总框架。条件性细节按 branch 放入 references，入口保留检查标准和完成条件。
- **Group 3：** 本轮没有工具 schema；描述分别限定 Prompt 表面与完整 Agent 系统，普通产品分析由主入口现有路径处理。
- **Group 4：** 没有 API、缓存、模型参数或 Agent 执行架构改动。

模型证据来自本地 `skill-eval` 的用户提供 Astra 快照，只支持保留明确的目标、自治边界和适度验证，不足以证明每句话均最优。行为样例支持当前边界和基本决策；未发现需要额外修改的模型年代模式。建议 diff 与实际实现一致，没有追加适配层。

## 限制

没有测试隐式触发、多宿主、长上下文、真实 Langfuse／Evals trace、Judge校准或实际多次统计。没有执行 Prompt 前后候选对照，因为样例任务只要求审查与设计。后续真实使用失败应先复现，再做最小修正；不能以本轮五个样例宣称整体稳定。
