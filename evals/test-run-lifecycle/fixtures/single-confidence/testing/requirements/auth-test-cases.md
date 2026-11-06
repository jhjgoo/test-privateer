# 登录 — 测试用例

## 执行批次

- Run ID：无 Run ID（单项短任务）
- 目标版本或快照：auth@71a4b21
- 环境：local
- 执行时间：2026-11-05T08:20:00Z
- 执行人／来源：local probe

| 用例 | 实际观察 | 测试判定及依据 | 证据 | 未决问题／后续 |
| --- | --- | --- | --- | --- |
| C-001 错误密码被拒绝 | HTTP 401，业务码 AUTH_INVALID_CREDENTIALS | 通过；符合已确认的登录拒绝契约 | `../../evidence/C-001-response.json` | 无 |
