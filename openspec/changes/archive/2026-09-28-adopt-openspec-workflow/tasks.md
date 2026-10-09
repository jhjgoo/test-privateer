# Tasks

## 1. Repository workflow

- [x] 1.1 初始化 OpenSpec 配置，建立项目背景、来源映射与宿主入口。
- [x] 1.2 建立四组已合并能力的历史回填 change，明确迁移及证据边界。

## 2. Validation asset policy

- [x] 2.1 先运行忽略边界检查得到预期失败，再加入 `.gitignore` 规则使检查通过。
- [x] 2.2 停止跟踪纯记录，核对本地文件保留；整理混合评测说明，保持可复用资产和引用。

## 3. Acceptance and archive

- [x] 3.1 复核来源、语义与保留边界，通过现有测试和 OpenSpec 严格校验。
- [x] 3.2 将四组历史 delta 合入当前规格并归档；确认引用与任务状态，满足本 change 的归档条件。

## Acceptance

2026-09-28：14 项 unittest、XMind 自测、OpenSpec 当前及历史包严格校验、共享本地链接检查及 Git diff 检查通过。独立复核未发现迁移阻断问题；顺手澄清评测说明中工具违规与环境失败的分类，未重判历史结果。20 份旧记录只移出索引，本地 SHA-256 与迁移前一致；混合 README 原文已留本地备份。`skills/` 未修改，无新增模型行为评测，未提交或推送。
