# 项目产品验证器最小行为评测

验证 `designing-test-automation` 是否能在不默认引入框架的前提下，从项目证据生成可实测的验证器契约，并保留未验证草案边界。

| 输入 | 必须观察到 |
| --- | --- |
| `existing-harness.md` | 优先复用现有 Playwright/API/CLI harness，只补缺口，不另建平行框架 |
| `draft-only.md` | 未实测时交付草案，明确启动、驱动、采证和清理的未验证项 |
| `shared-session.md` | 识别共享会话或数据风险，说明隔离或拒绝双实例驱动 |

真实运行时每个输入使用新临时项目；候选只看到自然任务和项目材料。判据放评审侧。若授权实测，至少驱动一条用户路径、确认清理后证据仍存在。原始记录放 `.local/validation/test-automation/`。
