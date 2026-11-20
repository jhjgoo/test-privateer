# Proposal: Integrate SkillEvaluator

## Why

本仓库需要使用 SkillEvaluator 验证后续 Skill 开发、优化及效果，避免将静态评分误作行为改进证据。用户已明确本阶段先建立项目验证体系，暂停向发布包新增 Skill 或消费方评测框架。

## What Changes

- 官方 `skillevaluator` Skill 作为维护者宿主能力，CLI 固定为 `0.9.0`。
- 在 AGENTS.md 与项目背景中接入 `evals/skillevaluator/README.md`，定义静态门禁、行为回归、旧新版本比较及无 Skill 贡献评测。
- 保留可复跑命令、证据要求与受阻状态，实际探查静态门禁和 Tier 3 就绪情况。
- 撤回本 change 的发布包入口、文档和路由改动，Skill 数量保持 30。
- 使用官方 Tier 3 与用户提供的 OpenAI-compatible 网关；可信仓库 Skill 可用官方 local 后端，需更强隔离时使用 Docker。先验证推理和工具调用，再执行双组冒烟及代表案例。

## Non-goals

不新增发布 Skill，不修改现有产品 Skill 方法或安装副本，不持久化密钥或发布 CI，不开发子代理后端。静态检查和独立审阅不替代实际 Tier 3 执行。
