# Test Privateer P0–P2 优化验证

日期：2026-09-09。验证对象为本地工作树的 P0–P2 优化；本记录不代表产品测试执行。

## 静态验证

- 18 个 Skill 通过 `quick_validate.py`。
- 26 个 Skill/reference 文件已同步到 `/Users/jianghongjian/.agents/skills`，字节一致。
- README、教程、Skill 和内部文档的相对 Markdown 链接无断链。
- `git diff --check` 通过。
- `test-privateer` 主入口新增主航线、路线状态、阶段门槛和真实产物核对。
- `artifact-routing` 新增统一 handoff 字段。
- 实际运行行为由 Skill description 和 Codex `agents/openai.yaml` 配置；宿主差异只保留在研究记录，不放入运行时 Skill 文档。

## GPT-6 Astra 行为探针

测试目录：`/tmp/test-privateer-p2/`。输入是一份 PRD、一份项目 `AGENTS.md` 和两轮提示：

1. 显式调用 `test-privateer`，确认项目／独立范围；
2. 用户选择“结合项目分析”，要求停在“路径准备 → 项目地图”，不生成用例、不执行产品测试。

观察结果：

- 第一轮询问独立分析与项目任务，没有把项目目录仅凭存在当成项目任务。
- 第二轮明确承接“路径准备 → 项目地图”。
- Agent 读取主 Skill、`mapping-project-test-space`、`artifact-routing` 和项目文件。
- Agent 在临时项目目录写入 `testing/TCO.md`，状态标为草案，并明确没有生成用例、没有执行产品测试。
- 最终 handoff 指向补齐代码、Spec、数据模型和测试证据后再进入变化分析。

另一个隐性入口探针曾验证过 `allow_implicit_invocation: true` 在该 Codex 宿主下会自动加载 `test-privateer`；该配置随后按产品使用策略撤回为 `false`。当前策略是主入口在 frontmatter 和 Codex 配置中都显式启动，后续阶段由主入口按 handoff 编排，避免不同宿主对主入口产生不一致的过度触发。

这证明 P0 主链在该 GPT-6 场景中被实际执行，而不是只出现在文档中。

## Skill-eval 结果

本轮按 `skill-eval` 的非 Claude 目标规则复核了 GPT-6 Astra 提示面：

- 没有引入 Claude 专属 API、结构化输出或请求参数建议；
- 保留项目权限、证据边界、执行授权和输出契约；
- 主入口的阶段顺序是业务流程约束，不属于可删除的通用 step-by-step 装饰；
- handoff 和路线状态是为解决实际观测到的跨 Skill 断链，不是重复的“请认真检查”；
- 宿主适配说明把显式调用、隐性首次触发、同会话续接和新会话恢复分开，没有声称各宿主行为完全一致。

## 未完成范围

- 本轮只直接探测了 GPT-6 Astra；GPT-5.6 Sol、Claude Code 和 Pi 的完整四场景矩阵仍待后续宿主验收。
- 没有执行产品测试，也没有把临时 `/tmp` 产物纳入项目 Skill 包。
