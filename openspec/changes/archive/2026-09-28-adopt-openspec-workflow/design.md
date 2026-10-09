# Design

## Context

仓库已有 Skills、标准库单元检查及少量评测输入，但旧审计与计划混入版本控制。用户已同意保留可复用资产，仅让过程记录退出日常提交。

## Goals / Non-Goals

用已安装 OpenSpec 的 `spec-driven` 流程管理本仓库。保持最小入口，不安装宿主插件或引入第二套任务账本，不用此次结构迁移宣称 Skill 行为提升。

## Decisions

- `openspec init --tools none --language zh-CN --profile core` 初始化；`AGENTS.md` 为简短入口，`CLAUDE.md` 引用同一入口。
- `project.md` 保存背景、来源映射和维护约定，`specs/` 保存当前行为，`changes/` 保存活动 delta 与已完成归档。四个回填 change 按能力组织，不按每次文案提交拆分。
- `.gitignore` 使用明确目录与少量历史文件规则，不全局忽略 Markdown、JSON、图像或 evidence 目录。保留被 Skill 引用的框架研究文档。
- 对已跟踪记录先取得清单与内容哈希，再 `git rm --cached`，核对本地文件未变；混合说明先本地备份，再只保留可复用判据与运行方法。
- 以真实 `git check-ignore --no-index` 检验输出与源码边界，执行已有 unittest、XMind 自测及 OpenSpec 严格校验；不重跑模型行为评测。

## Risks / Trade-offs

忽略目录中新增长期参考容易漏跟踪：约定放回对应 `skills/*/references/`，回归检查保护现有例外与夹具证据。历史归档表示源码契约迁移，不补造过去的验收；宿主是否遵循入口仍不是自动保证。旧验证文件保持本地，Git 删除只代表停止跟踪。
