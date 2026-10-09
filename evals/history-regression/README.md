# 历史问题行为回归

覆盖三个历史失败及其相邻正常场景。输入位于 inputs/；本文件是评审依据，不传给受测 Agent。输入是脱敏、缩小的合成场景，不是原始项目完整回放。

## 来源与判据

| 输入 | 来源 | 通过标准 |
| --- | --- | --- |
| cause | 2026-09-09 重复动作调查案例 | 区分重复请求产生与循环放大；不能仅凭失败计数分支解释模型为何重复；指出下一轮输入等缺失证据与具体取证动作 |
| observation | 同类调查的边界对照 | 准确报告金额错误及已知范围；不强制完整根因调查或重新建立项目地图 |
| unclear | 2026-09-10 PRD整改验证 | 在依赖规则的完整模型前提出快照时点问题，给推荐及理由；不默认输出实施准入结论 |
| clear | 澄清的相邻正常场景 | 直接分析明确规则；不要求重复确认工作方式和既定业务规则，不默认实施准入 |
| repair | 2026-09-08 自校验证 C/D | 修正摘要、模型、T-001 的确定预期和 T-002 的覆盖声明；保留 T-003、编号及 R-004 后续安排；不能只加免责声明 |
| sound | 自校的相邻正常场景 | 保留正确的范围与预期；只审查不擅改，不虚构矛盾、不强制新增测试项 |

不按标题、术语次数、固定步骤或输出长度评分。检查完整产物和工具轨迹：模型自称通过不作为证据。对于原因假设，区分“值得调查”与“已证实”。

## 运行方法

1. 固定源码提交，复制 skills/ 到独立临时目录；每个样例、每次运行使用新目录和新会话。
2. 仅把该样例放入临时目录的 task.md。提示要求读取本地快照 skills/test-privateer/SKILL.md 与任务需要的下游文件，然后处理 task.md；禁止读取评审判据和其他样例。
3. 使用 `codex exec --skip-git-repo-check --sandbox read-only --json --model <目标模型> -c 'model_reasoning_effort="high"' --output-last-message <输出路径>`，保存标准输出、错误输出、退出状态、耗时和最终回复。
4. 人工按上表判定 PASS／FAIL／环境受阻。修稿样例在回复中交付完整修正稿，避免写权限成为额外变量。
5. 首轮六个样例，条件允许时各重复一次。出现内容失败后定位加载、规则冲突或完成条件，再做单因素候选修改与同条件对照。环境受阻不计为内容失败。

模型名称是请求参数，不独立证明上游服务型号。记录 CLI 版本及是否继承用户配置；本测试仅验证显式加载，不验证隐式触发。真实产品执行、长上下文、多轮交互和 Workbuddy 需另行验证。

评估资料不放入运行时 skills/，不增加用户日常任务的输出负担。当前版本通过的能力保持原样；没有收益证据不发布新的提示词。

## 扩展验证

[跨文件规则变更](crossfile/README.md)检查实际文档修订与原始证据保护。运行结果保存在本目录或 crossfile 下被忽略的 `runs/`，不随可复用材料提交。

## 复跑一个短场景

在仓库根目录执行以下命令；默认重跑 cause，其他场景替换输入文件名。每次建立新目录。命令继承本机CLI配置，运行结果不会自动判为通过，仍需按前述判据审阅。若要重现本次源码，先在独立检出目录使用报告中的完整提交号；直接复制当前工作区只代表当前版本。

```bash
eval_dir=$(rtk proxy mktemp -d /tmp/privateer-replay-XXXXXX)
rtk proxy cp -R skills "$eval_dir/skills"
rtk proxy cp evals/history-regression/inputs/cause.md "$eval_dir/task.md"
rtk proxy codex exec -C "$eval_dir" --skip-git-repo-check \
  -s read-only --json -m gpt-6-astra \
  -c 'model_reasoning_effort="high"' \
  -o "$eval_dir/answer.md" \
  '读取当前目录 skills/test-privateer/SKILL.md 及任务需要的下游文件，然后处理 task.md。只使用当前目录的技能快照和任务材料，不读取其他目录、历史会话、评审答案或网络。不要修改文件，在最终回复中交付结果。' \
  > "$eval_dir/events.jsonl" 2> "$eval_dir/stderr.log"
eval_status=$?
rtk proxy printf '%s\n' "$eval_status" > "$eval_dir/exit-code.txt"
rtk proxy printf '结果目录：%s\n' "$eval_dir"
```

每次运行在本地结果目录保存判读与 SHA-256 清单。校验清单证明文件一致性，不证明内容结论正确；本 README 不作为当前版本的通过记录。
