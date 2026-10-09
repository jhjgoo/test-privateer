# Proposal

## Why

用户要求本仓库用 OpenSpec 管理变更，并让非发布用途的验证记录默认不进入 Git，避免每次提交重新确认；同时回填已完成能力的背景与历史归档。

## What Changes

- 配置本地 OpenSpec、简短宿主入口与项目背景，建立当前规格及四组历史回填档案。
- 忽略本地日志、运行结果、审计和旧计划；已跟踪纯记录移出索引但保留文件。
- 保留 Skill、测试、可复用评测材料和生产引用的研究资料，拆开混合 README 中的判据与历史结果。
- 增加实际调用 Git 的忽略边界检查。
- 非目标：改变 Skill 行为、安装全局宿主命令、引入新评测平台、替使用方项目接入、提交或推送。

## Capabilities

### New Capabilities

- `repository-workflow`：本仓库变更、历史迁移及验证资产跟踪约定。

### Modified Capabilities

无。四组业务契约由独立的 `backfill-*` change 登记；本 change 只管理仓库流程。

## Impact

影响 `.gitignore`、根目录协作入口、README、OpenSpec、评测说明和索引。历史归档基线为 `3519852`；不修改 `skills/` 内容，不删除本地证据、不重写 Git 历史。
