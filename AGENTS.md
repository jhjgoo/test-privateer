# 仓库协作

- 修改本仓库前，读取 [项目背景与变更流程](openspec/project.md)，再读取相关 `openspec/specs/*/spec.md` 和已有活动 change；继续任务时复用原 change。
- 行为、路由、交付契约或仓库流程变更在 `openspec/changes/<name>/` 维护 proposal、spec delta、design、tasks。纯错字、失效链接修正不另建 change。低风险变更保持文档简短。
- 实施前核对原请求、可观察结果和验证方法；实施中若发现范围偏移或失败反证，先更新同一 change 的决定与剩余任务；交付前按原承诺核对实际文件、测试与未完成项。需要方案质检时使用本仓库 `skills/checking-solutions/SKILL.md`，测试产物自校使用 `skills/challenging-test-designs/SKILL.md`。
- 原始评测输出和审计过程放 `.local/validation/` 或 `evals/<suite>/runs/`。可复用输入、夹具、判据、脚本、测试和 OpenSpec 资产正常跟踪；提交前检查暂存区，勿强制添加被忽略的记录。
- 有 codebase-memory-mcp 时优先用图工具发现代码；非代码资料或图结果不足时用文件搜索。RTK 可用时遵循宿主既有 RTK 约定，不为本仓库安装工具或改写全局配置。

这些是本仓库的调用约定，不是自动执行钩子，也不会随 Skill 安装自动接入使用方项目。
