# 收尾验证

日期：2026-11-21。产品实现来自 `b03fe30`，本轮以 `362015d` 工作区核对交付。补齐验证，并按实测反例修正任务包生成和方案质检边界。

## 原承诺与证据

| 原承诺 | 实现与回归对象 |
| --- | --- |
| 盲测任务包共用契约 | `running-test-loop/SKILL.md` 与 `references/blind-test-worker.md`；核对两份真实 brief、首行共同入口、隔离输出及普通单层请求边界 |
| 教训按未来行动价值筛选 | `maintaining-project-lessons/SKILL.md`；偶发环境不晋升，同时保留已确认高后果单次事件例外 |
| 重复特判先查共同模型 | `checking-solutions/SKILL.md`；共享金额边界与合法地区分支对照 |
| 用例减少执行者脑补 | `designing-test-experiments/SKILL.md`；明确动作与 oracle，缺少状态准备入口不虚构可执行 |
| 终稿质检识别隐式判定 | `challenging-test-designs/SKILL.md`；修正依赖经验的 Case，保留已充分短 Case |

## 静态检查

- `python3 -m unittest discover -s tests -q`：101 项通过，包括任务包生成器的 5 项真实临时目录检查。
- 使用已安装的 SkillEvaluator Python 环境运行 `python -m unittest discover -s evals/skillevaluator -p test_policy.py -q`：5 项通过。
- 五个受影响 Skill 分别执行 `skillevaluator tier1 skills/<name> --no-llm --profile default --policy evals/skillevaluator/policy.yaml -r json,markdown -o <独立输出目录>`：均退出 0，`overall_status=passed`、0 error、无 incomplete scan。告警依次为 Loop 16、教训 17、方案 16、实验设计 17、终稿自校 16。
- 策略 profile 为 `test-privateer`；digest 为 `sha256:ef61893169f6170df5ca09265ed6057a72529fc8911b7b815ce2abe69d78ce0d`。所用策略副本及原始报告保留。
- SkillEvaluator 0.9.0，扫描器 SkillSpector 2.13.3。默认 scanner 启动卡在 uv 解析，已终止；通过官方 `SKILLEVALUATOR_SKILLSPECTOR_PATH` 指向已有同版本缓存后完成扫描，未更改策略或扫描器。可选元数据、英文标题启发式及包外引用未验证提示保留；扫描器通过不证明跨 Skill 引用目标全部扫描完毕。
- 本轮没有运行 Tier 2，不以本轮静态结果申请上游 publication eligibility。
- 修正后对 `checking-solutions` 和 `running-test-loop` 分别重跑完整 Tier 1。最终 Loop 报告在 `tier1-minimal/`：退出 0、`overall_status=passed`、0 error、20 warning，策略 digest 未变；告警包含已保留的元数据、质量启发式和脚本扫描提示，不代表行为通过。
- 独立代码审查未发现可复现缺陷；除生成器和工作流契约测试外，另以临时目录核对父目录符号链接越界和输出符号链接均拒绝，外部原内容保持。该审查不代替 Tier 3。

## 行为回归范围

案例与来源见 `evals/skillevaluator/workflow-lessons/`，独立审阅后冻结。两版数据集均 strict validate 退出 0，两个模型的 local doctor 均退出 0。

使用官方 SkillEvaluator 0.9.0、Codex CLI 0.169.0、local 后端、high reasoning、每例一次、timeout 1x。模型为 `auto/gpt-5.6-sol` 与 `auto/glm-5.3`，Judge 为 `group/j.a.r.v.i.s`。网关路由的底层模型版本未确认。旧版为 `7b21aa226fcc43b47340703e980e1a6296a8066d` 的完整 Skill 包，新版为当前工作区完整包；须检查实际读取范围，不能将其他未行使能力的变化归因于本 change。

五个组合案例 × 两版本 × 两模型，计划 20 次执行及相应评分调用；每组运行 `tier3 evaluate`，使用 `--skip-baseline --max-cases 1 --n-attempts 1 --max-attempts-total 1 --env-mode local --skill-workspace-mode group --harbor-keep-jobs`，同组的完整包通过 `--include-skills` 提供。完整命令和哈希保存在本地 `matrix.json` 与 `snapshot-hashes.json`。

这不是无 Skill 贡献实验，不报告 Skill Lift，也不是完整双盲。Loop 仅验证任务包生成侧的共同契约接入；不证明冷启动子代理消费、完整调度或产品测试通过。其他四项按其实际建议／设计／审查交付判定，不冒充真实项目文件维护或产品执行。

原始证据根目录：`.local/validation/skillevaluator/workflow-close-3ncnxguf/`。以下相对运行路径均位于该目录，缺失评分和运行错误不记为内容零分或通过。

## 已完成的文字交付复核

执行者与匿名复核者分离；锁定逐断言判定后才揭示旧新和模型映射。原始输出、锁分与映射见 `review-text-{a,b}*` 和 `review-solutions-final*`。输出风格、路径及轨迹仍可能泄露身份，不能称完整双盲。

| Skill／采用轮次 | 旧版 GPT／GLM | 新版 GPT／GLM | 可支持的结论 |
| --- | --- | --- | --- |
| maintaining-project-lessons／`runs/` | PASS／PASS | PASS／PASS | 偶发事件不晋升，高后果单次例外保留；未观察到提升 |
| checking-solutions／`solutions-repair/` | PASS／PASS | PASS／PASS | 共享边界识别和合法地区分支保护通过；未观察到相对旧版提升 |
| designing-test-experiments／`runs/` | FAIL／PASS | PASS／PASS | 该样本新版保留可执行缺 Token 检查，且未掩盖停用企业夹具缺口 |
| challenging-test-designs／`runs/` | PASS／PASS | PASS／PASS | 缺准备／oracle 的 Case 被识别，充分短 Case 未被强行扩写 |

四项采用的 16 次尝试均产生官方评分，无执行错误。官方 `behavior_check`（GPT／GLM，旧→新）分别为：教训 `1.0／0.75 → 1.0／1.0`；方案 `1.0／1.0 → 1.0／1.0`；实验设计 `0.5／0.75 → 0.5／0.75`；终稿自校 `1.0／1.0 → 1.0／1.0`。官方评分与逐条复核不完全一致，不能用这个汇总分替代原冻结断言。

方案首轮新版 GLM 曾把已确认地区法规额外解释成必须检查日期选择链，匿名复核 FAIL；官方 `goal_accuracy=0.0`、`accuracy=0.6`，而 `behavior_check=1.0`。补清“未知实现细节只能列未验证”后完整重跑四组，原失败未覆盖。实验设计旧版 GPT 失败原因为额外把题设未要求的 tenantCode 格式来源当作阻塞条件；单次旧新差异仅是该配置的观察，不证明稳定优化。

## Loop 反例与修正

首轮以及 `loop-repair/`、`loop-final/`、`loop-entry/` 保留了重复共同规则、共同引用未读取、相对路径错误、唯一合成者与执行者混淆等反例。以 `reference-read-audit.json` 核对实际读取；文件存在不等于入口生效。

最终使用小型标准库生成器固定首行相对引用和字段结构，只接受本轮差异，不运行测试入口；写入前规范化路径，保留已有不同内容，同内容可重复执行。`loop-cli-contract/` 中 GLM 首次把 `--output` 放在 `--command` 后被 argparse 拒绝，随后按帮助调整参数成功；这属于调用恢复，不隐去首错。其输出仍在业务契约和附加产物重复共同证据／handoff 要求，不能因官方 `behavior_check=1.0` 判通过。删除未被原需求要求的附加产物选项，保留业务契约、专有前置、获准入口和隔离输出。

原 Judge 在旧版长轨迹反复评分超时，扩至 360 秒仍不足；超时保持 NO SCORE。`loop-judge-glm/` 和最终 `loop-minimal/` 分别完整重跑两版本 × 两模型，Judge 固定 `auto/glm-5.3`、Judge budget 360 秒、`--timeout-multiplier 2`，其余沿用冻结案例与单次预算。它们不与原 Judge 或 1x 预算的单臂拼接。

最终 Loop 产物由另一位匿名复核者先锁分再揭盲，结果为旧版 GPT／GLM 均 FAIL，新版 GPT／GLM 均 PASS。旧版两份文件重复隔离、证据和 handoff 规则，且首行未指向共同契约；新版通过实际生成文件及完整工具输出核对，同一共同引用可读，目标版本、Run／wave、业务契约、命令、隔离输出和唯一合成者齐全，没有执行产品入口，也没有将普通接口测试强制转为完整 Loop。

GLM 新版的临时工作区在评测结束后被官方清理，首次匿名复核因收集不到正文标为 UNKNOWN；随后补充原轨迹中两次生成及 `cat` 的完整输出、共同契约成功读取响应，独立复核改判 PASS。保留原 UNKNOWN、补证及两次锁分，未重新生成或人工修改受测文件。证据在 `review-loop-minimal*.json`。

官方新版 `behavior_check` 为 GPT `0.75`、GLM `0.5`：Judge 明确表示看到的轨迹被截断，将部分文件字段或第二份文件标为 `not_checked`，不是观察到文件内容错误。独立产物复核补足项目断言；官方分数原样保留，不把缺失观察改算为官方满分。

`loop-minimal` 旧版 GLM 的必需 `behavior_check` 超时，退出 1、0/1 scored、1 judge failure，不能记为内容零分或通过。此前 `loop-judge-glm` 虽有完整旧版双模型结果，且 60 个旧版快照文件逐一一致，官方 `compare-versions` 仍因报告身份字段缺失拒绝比较：持久化 comparison identity 有 publication target，但从原 run config／result 重建时该字段为 null。保留 `loop-comparison/` 中的不可比较结果，不修写官方证据或强行复用。相同配置的 `loop-minimal-retry/` 再次退出 1；该次独立文件复核仍为旧版 FAIL，但不以复核替代缺失官方评分。

### 最终完整矩阵

最终采用 `loop-gpt-judge/` 的独立四组：旧版／新版 × `auto/gpt-5.6-sol`／`auto/glm-5.3`，Judge 统一改为 `auto/gpt-5.6-sol`，Judge budget 360 秒、timeout 2x，案例、快照及其他预算不变。四组分别退出 0，各 1/1 scored、0 execution error、0 judge failure；不与前述 GLM 或原 Judge 的分数拼接。

| 执行模型 | 官方 overall 旧→新 | 官方 behavior_check 旧→新 |
| --- | --- | --- |
| GPT-5.6-SOL | 0.6625 → 0.6875 | 0.25 → 0.5 |
| GLM-5.3 | 0.7775 → 0.8875 | 0.5 → 0.25 |

新版两组 `accuracy`、`goal_accuracy` 都为 1.0。新 Judge 仍因工具轨迹截断，将部分文件断言记为 `not_checked`；GLM 的 behavior_check 下降不能直接解释为产品回归，overall 上升也不能直接解释为效果提升。保留原始官方分数，按冻结判据另核对运行时抓取的全部 8 份文件、引用可达性和完整调用轨迹。`captured-files.json` 在环境清理前留存实际产物；匿名复核记录见 `review-loop-gpt-judge*.json`。

最终四组匿名复核先锁分再揭盲：旧版 GPT／GLM 均 FAIL，新版 GPT／GLM 均 PASS；逐断言依据见 `review-loop-gpt-judge-locked.json` 与 `review-loop-gpt-judge-unblinded.json`。旧版首行缺共享引用且重复共同规则，新版两组保留了完整差异字段和可访问引用，未执行产品测试或启动子代理；独立单条接口测试仍直达专项。

最终采用的五项回归共 20 次已评分尝试，新版 10 次均通过独立逐断言复核，来源清单为 `closeout-evidence.json`；这不是把所有修正轮次合并成一次实验，也不包含原失败尝试。五个当前目标 Skill 的完整文件树均与各自采用的受测新版快照逐文件一致，核对结果见 `closeout-source-hashes.json`。

## 结论边界

没有无 Skill 组，不计算 Skill Lift；未执行 Tier 2、真实产品测试或冷启动 worker 消费任务包后的完整调度。路由模型的底层版本未确认，单次组合案例只支持有限回归观察，不支持稳定提升或发布认证。原始产物未人工修改后冒充模型生成结果。

收尾检查：101 项仓库测试、5 项策略测试和 XMind 脚本 self-test 通过；受影响 Skill 的完整无 LLM Tier 1、活动 change 的 OpenSpec strict 校验和 `git diff --check` 通过。实施与本轮验收完成，任务 1–8 已完成。

用户已于 2026-11-21 明确确认本 change 完成，授权同步当前规格并归档；任务 9 的确认条件已满足。本轮未提交或推送。
