# Test Privateer 项目背景

## 项目与边界

本仓库发布黑帆测试官的 23 个 Agent Skills：主入口 `test-privateer` 按任务路由到测试分析、设计、执行、调查、回归和信心评估，以及方案、Prompt／Agent、UI/UX 质检。运行时内容在 `skills/`，用户教程在 `docs/`，可运行检查在 `tests/`，可复用行为评测材料在 `evals/`。

产品契约见 [当前规格](specs/)，具体方法和模板仍以对应 Skill 为维护位置。规格约束可观察行为，不复制全部提示词，也不宣称模型每次都能遵循。接口／页面自动化目前提供设计入口，未提供框架接入与脚本实现；单元测试可编写并验证。

OpenSpec 从 2026-09-28 起管理**本仓库**的变更。它不改变安装方式，不为使用方项目创建 Spec 或审批流程。`ask-matt`、`skill-eval`、Superpowers 等是外部协作能力，不属于本仓库交付和验证范围。

## 已完成能力的历史回填

回填基线：`351985269815995ee69dcf5cbeb4842c1fb59010`。以下按能力归组，日期是迁移日期，不是原开发日期；档案中的任务记录本次迁移核对，不伪造历史 OpenSpec 流程。

| 当前能力 | 归档 change | 来源提交 |
| --- | --- | --- |
| [测试工作流](specs/testing-workflow/spec.md) | [backfill-testing-workflow](changes/archive/2026-09-28-backfill-testing-workflow/) | `133e621` 至 `99d51c6` 的连续 13 个提交：路由、澄清、自校、阶段交接、调查及回归 |
| [方案与 Agent 质检](specs/solution-agent-quality/spec.md) | [backfill-solution-agent-quality](changes/archive/2026-09-28-backfill-solution-agent-quality/) | `56403b6`、`6ea4965`、`e321468`、`dc074c7`、`0fbbfa1`；`3519852` 的完成边界 |
| [UI/UX 评审](specs/ui-ux-review/spec.md) | [backfill-ui-ux-review](changes/archive/2026-09-28-backfill-ui-ux-review/) | `b99564d` |
| [用例与报告质量](specs/test-artifact-quality/spec.md) | [backfill-test-artifact-quality](changes/archive/2026-09-28-backfill-test-artifact-quality/) | `3a4d1b5`、`b17cce4`；`3519852` 的表达、语义保真与区分力 |

回填确认上述能力已进入源码；这不是重新运行所有历史行为评测。静态契约检查不能替代生成行为验证，有限样本通过不能证明所有模型、宿主和长会话稳定。阶段质检仍依赖宿主读取规则与实际调用，未建立自动钩子。旧开发生命周期方案中未交付的扩展、使用方真实项目接入，不因本次归档变成已完成；有新授权时另建 change。

## 变更流程

复用已有活动 change；有行为或流程变化时建立一个最小变更包。普通纠错不改变契约时直接修改即可。

```sh
openspec list
openspec new change <name>
openspec status --change <name>
openspec instructions proposal --change <name>
# 按需获取 specs、design、tasks 指令，填写并对齐原请求后实施
openspec validate <name> --strict --no-interactive
# 实际完成并核对验证、剩余范围后，更新当前 specs 并归档
openspec archive <name> --yes
openspec validate --all --strict --no-interactive
openspec validate --archived --strict --no-interactive
```

使用 `spec-driven` schema；本次用 OpenSpec 1.13.2 初始化，未安装宿主专用 slash commands 或修改全局配置。`config.yaml` 提供生成上下文；CLI 是工具入口，`AGENTS.md`／`CLAUDE.md` 是本仓库协作入口。

实施前用需求和反例检查可落地、可观察、可判定；实施中更新偏差、反证和未完成项；交付前对照原承诺核对实际文件与验证，不能由执行者自行缩小范围后关闭原任务。明确获准的分阶段工作只验收本阶段。

## 验证与版本控制

常规本地检查：

```sh
python3 -m unittest discover -s tests -v
python3 skills/exporting-test-cases-to-xmind/scripts/md_to_xmind.py --self-test
git diff --check
```

Skill 行为变化按风险选代表失败、相邻正常和必要的迁移样本；记录目标配置、版本、真实输出与判读，不要求为简单改动重跑全部模型评测。本次框架迁移不改 Skill 行为，只做结构、引用、忽略边界及既有检查。

Git 保留 Skill、模板、用户教程、可复用测试／评测脚本、输入、夹具、判据和 OpenSpec。原始输出、运行日志、审计报告和旧计划留在本地，不作为发布资产；新记录统一放 `.local/validation/` 或 `evals/<suite>/runs/`。历史 `docs/research/`、`docs/superpowers/` 也按本地记录处理，唯一保留的框架研究文档是已被生产 Skill 引用的源资料。新增长期参考优先放对应 Skill 的 `references/`。

已跟踪的纯记录只移出 Git 索引，不删除本地文件、不改写 Git 历史。忽略规则不隐藏夹具中的证据样本。共享 change 只写必要的验收结论、命令、范围和限制，不附原始运行报告；本地记录不可访问时，不能把历史结论冒充当前可核验结果。
