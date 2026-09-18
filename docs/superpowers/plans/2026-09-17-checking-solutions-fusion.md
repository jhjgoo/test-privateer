# Checking Solutions 融合实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `challenging-change-specs` 重构为统一的 `checking-solutions` 方案质检 Skill：普通研发方案执行轻量对症检查，SDD 变更包在此基础上加载完整契约链检查，同时保留现有 SDD 能力并消除双入口。

**Architecture:** `checking-solutions/SKILL.md` 只承载所有方案都需要的质检流程；原 `challenging-change-specs` 的阶段、框架、任务、归档等 SDD 专属规则下沉到 `references/sdd-contract-chain.md`，并通过可观察的 SDD 产物条件加载。`test-privateer` 只负责路由，普通方案不会被迫补齐 SDD 产物，SDD 方案也不会退化成单纯的硬编码扫描。

**Tech Stack:** Markdown Agent Skills、Python `unittest` 静态契约测试、Codex CLI 隔离行为回归、Git。

**Spec:** [本计划的设计基线](#设计基线)

## Global Constraints

- 只保留一个最终入口 `checking-solutions`；验证通过后删除 `challenging-change-specs`，不长期保留兼容壳。
- 质检对象是已经形成的方案草稿；Skill 不参与原方案生成，不替负责人审批，也不默认重写完整方案。
- “硬编码”按语义判断：只有绑定样例偶然特征且缺少业务规则、系统约束或失败机制依据时才形成发现；常量、白名单和局部分支本身不是问题。
- 普通方案只执行核心质检；仅在识别到 SDD 框架、产物角色或实施／归档阶段时加载 SDD 参考。
- 保留 `challenging-change-specs` 当前的阶段、框架映射、delta、任务切分、实现证据、归档事实和验收证据矩阵能力。
- 不修改 `investigating-findings`、`prompt-eval`、`agent-eval` 和 `challenging-test-designs` 的职责边界。
- 先取得当前版本的失败基线，再编辑运行时 Skill；基线未复现的问题不增加规则。
- 行为回归的原始事件、回复、日志和临时目录只放 `/tmp`，不得加入 Git。
- 不改写历史研究和历史运行记录中的旧 Skill 名称；只更新当前运行时文件、当前文档和新增回归资产。
- 不生成 Workbuddy 发布包、不提交、不推送，除非后续得到明确授权。

---

## 设计基线

### 统一职责

`checking-solutions` 在 AI 已生成或接收到研发解决方案、修复方案、实施方案或 SDD 变更包后，检查以下证据链：

```text
问题或目标 → 已知依据 → 方案作用点 → 预期行为变化 → 验证证据
```

它只输出可定位的发现、未验证部分和证据边界。没有发现时，只能说明“在当前材料和范围内未发现可证明的问题”，不能升级为实施批准或正确性证明。

### 普通方案分支

检查样例耦合、作用点错位、闭环断点、范围夸大和无法区分样例补丁的验证。原因未知时报告缺口；已明确标注的止损方案可以成立，但不得被描述成根因修复。

### SDD 分支

核心质检完成后，若材料明确使用 SDD／Spec-Driven，出现 proposal、spec、design、tasks、verify、archive 等角色，或用户要求实施前、实施后、归档前质检，则读取 `references/sdd-contract-chain.md`，继续检查阶段、框架、delta、任务、实现证据和归档事实。

### 输出边界

每条发现必须包含具体位置、直接证据、断开的连接、影响和最小补证或修正方向。普通分支不输出“可实施／不可实施”；SDD 分支可以保留现有阶段门禁，但必须声明该结论只针对当前 SDD 产物链和证据。

---

## 文件结构

| 路径 | 动作 | 单一职责 |
| --- | --- | --- |
| `skills/checking-solutions/SKILL.md` | 新建（由旧 Skill 重构） | 通用方案质检、分支识别、输出契约和完成条件 |
| `skills/checking-solutions/references/sdd-contract-chain.md` | 新建 | 原 SDD 专属阶段、产物、任务、证据与归档规则 |
| `skills/checking-solutions/references/framework-map.md` | 移动 | SDD 框架到通用产物角色的映射 |
| `skills/challenging-change-specs/` | 删除 | 避免双入口和规则重复 |
| `skills/test-privateer/SKILL.md` | 修改 | 将普通方案与 SDD 方案统一路由到 `checking-solutions` |
| `tests/test_checking_solutions_contract.py` | 新建 | 验证目录、引用、路由、文档和旧入口清理 |
| `evals/checking-solutions/README.md` | 新建 | 固定行为回归方法、人工判据和不提交原始输出的规则 |
| `evals/checking-solutions/inputs/*.md` | 新建 | 普通方案、合理例外、止损和 SDD 分支的最小输入 |
| `README.md` | 修改 | 更新 Skill 清单和用途 |
| `docs/guide.md` | 修改 | 更新 Skill 数量不变的清单与入口说明 |
| `docs/developer-guide.md` | 修改 | 将“评方案”示例改为统一方案质检，并解释 SDD 加深分支 |

---

### Task 1: 建立当前版本的行为失败基线

**Files:**
- Create: `evals/checking-solutions/README.md`
- Create: `evals/checking-solutions/inputs/repeated-action-patch.md`
- Create: `evals/checking-solutions/inputs/shared-seam-patch.md`
- Create: `evals/checking-solutions/inputs/legitimate-local-rule.md`
- Create: `evals/checking-solutions/inputs/explicit-containment.md`
- Create: `evals/checking-solutions/inputs/sdd-badcase-patch.md`
- Create: `evals/checking-solutions/inputs/sdd-sound-package.md`

**Interfaces:**
- Consumes: 当前 `skills/test-privateer/SKILL.md` 与 `skills/challenging-change-specs/SKILL.md`。
- Produces: 六个固定输入、一套人工判据和当前版本是否存在目标缺口的基线结论；原始运行结果只存在 `/tmp/checking-solutions-baseline-*`。

- [ ] **Step 1: 写回归说明和评分规则**

在 `evals/checking-solutions/README.md` 写明：

```markdown
# 方案质检行为回归

验证 Skill 能否在不替代方案生成和审批的前提下，检测样例耦合、作用点错位、闭环断点、范围夸大和验证缺口，并保留合理局部规则与明确止损方案。

## 通过判据

| 输入 | 必须发现 | 不得误报 |
| --- | --- | --- |
| repeated-action-patch | “禁止连续相同调用”只控制症状；成功状态是否进入下一轮仍无证据；合法重试需要保持 | 不得断言状态回写一定是根因，不得直接重写完整方案 |
| shared-seam-patch | 单个调用方补丁绕过三个入口共享的 normalizeAmount；只复测 API A 不能支持全局修复声明 | 不得把已确认的两位小数规则本身称为硬编码 |
| legitimate-local-rule | 无发现；CN 分支有明确法规依据且影响边界明确 | 不得因存在地区常量而报告硬编码 |
| explicit-containment | 可指出它是止损而非根治，但不能把明确标注的临时限流本身报告为错误 | 不得要求在应急发布前完成完整根因调查 |
| sdd-badcase-patch | 发现设计作用点与失败机制断开、任务和验证只覆盖单个案例；同时执行 SDD 契约链检查 | 不得只做关键词扫描 |
| sdd-sound-package | 无对症性 finding；继续检查阶段、任务、验证证据和归档事实 | 不得要求普通方案字段，不得虚构缺失 |

## 评分

- PASS：满足该输入全部“必须发现”和“不得误报”。
- FAIL：漏掉关键断点、把合理局部规则当硬编码、把止损当根治错误、替用户重写方案，或给出无证据审批结论。
- BLOCKED：环境或工具无法产生有效结果；不得算作内容失败。

每个输入使用新临时目录和新会话。基线至少运行一次；候选版本每个输入运行两次。人工阅读完整回复，不按标题、关键词次数或模型自称评分。原始事件、最终回复和日志只存 `/tmp`，不加入仓库。
```

- [ ] **Step 2: 写六个最小输入**

每个输入都包含“原问题／依据／AI 已生成方案”，不要求受测 Agent 再生成方案。示例 `repeated-action-patch.md` 使用以下事实：

```markdown
请质检下面这份非 SDD 修复方案，只报告有证据的方案问题，不重新设计完整方案。

问题：模型在工具第2次调用成功后，第3至8次继续请求相同添加动作。重复保护拒绝后直接 continue，失败计数没有增长。下一轮模型输入未保留，无法确认成功结果和条目变化是否反馈给模型。

方案：在编排层保存 previous_action；如果本轮 action 与 previous_action 完全一致，直接丢弃。原重复动作案例已通过，因此该问题已根治。
```

其余输入必须分别固定：共享 `normalizeAmount` 却只修 API A；有法规来源的 CN 特例；明确声明“仅止损”的临时限流；包含 design/tasks/verify 的 SDD badcase 补丁；契约链完整且作用点合理的 SDD 正常包。

- [ ] **Step 3: 使用当前版本运行基线**

对普通方案输入显式加载当前主入口；对 SDD 输入显式加载当前 `challenging-change-specs`：

```bash
eval_dir=$(mktemp -d /tmp/checking-solutions-baseline-XXXXXX)
cp -R skills "$eval_dir/skills"
cp evals/checking-solutions/inputs/repeated-action-patch.md "$eval_dir/task.md"
codex exec -C "$eval_dir" --skip-git-repo-check -s read-only --json \
  -m gpt-6-astra -c 'model_reasoning_effort="high"' \
  -o "$eval_dir/answer.md" \
  '读取当前目录 skills/test-privateer/SKILL.md 及任务需要的下游 Skill，然后处理 task.md。只使用当前快照和任务材料；不要读取网络、历史会话或评审答案。不要修改文件。' \
  > "$eval_dir/events.jsonl" 2> "$eval_dir/stderr.log"
printf '%s\n' "$?" > "$eval_dir/exit-code.txt"
printf '结果目录：%s\n' "$eval_dir"
```

- [ ] **Step 4: 人工评分并执行修改门槛**

只有以下条件成立才继续 Task 2：普通方案至少一个关键断点被漏检，或 SDD 分支无法检测 badcase 定向修补。若全部场景已稳定满足判据，停止实现并记录“无需新增 Skill”；不得为了完成计划而强行改写运行时规则。

- [ ] **Step 5: 提交可复现输入，不提交运行输出**

```bash
git add evals/checking-solutions/README.md evals/checking-solutions/inputs
git commit -m "test(测试技能): 增加方案对症性质检场景"
```

---

### Task 2: 用静态契约锁定融合后的目录和边界

**Files:**
- Create: `tests/test_checking_solutions_contract.py`

**Interfaces:**
- Consumes: Task 1 已证明的行为缺口和本计划文件结构。
- Produces: 在运行时 Skill 尚未重构时必然失败、重构完成后通过的静态契约。

- [ ] **Step 1: 写失败测试**

测试必须验证：新入口及两份 reference 存在；旧入口最终不存在；核心 Skill 引用 SDD reference；主入口与当前文档使用新名称；核心 Skill 包含“样例耦合、作用点、未验证”；SDD 专属 delta 术语只在 reference 中出现。

```python
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckingSolutionsContractTest(unittest.TestCase):
    def test_merged_skill_has_one_entrypoint_and_lazy_sdd_reference(self):
        skill_dir = ROOT / "skills/checking-solutions"
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        sdd = skill_dir / "references/sdd-contract-chain.md"
        framework = skill_dir / "references/framework-map.md"

        self.assertIn("name: checking-solutions", text)
        self.assertIn("references/sdd-contract-chain.md", text)
        self.assertTrue(sdd.is_file())
        self.assertTrue(framework.is_file())
        self.assertFalse((ROOT / "skills/challenging-change-specs").exists())
        for term in ("样例耦合", "作用点", "未验证"):
            self.assertIn(term, text)
        self.assertNotIn("ADDED/MODIFIED/REMOVED", text)
        self.assertIn("ADDED/MODIFIED/REMOVED", sdd.read_text(encoding="utf-8"))

    def test_router_and_current_docs_use_the_merged_name(self):
        paths = (
            ROOT / "skills/test-privateer/SKILL.md",
            ROOT / "README.md",
            ROOT / "docs/guide.md",
            ROOT / "docs/developer-guide.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("checking-solutions", text, path)
            self.assertNotIn("challenging-change-specs", text, path)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认 RED 原因正确**

```bash
python3 -m unittest tests/test_checking_solutions_contract.py -v
```

预期：FAIL，原因是 `skills/checking-solutions/SKILL.md` 尚不存在；不能接受导入错误或 Python 环境错误作为有效 RED。

---

### Task 3: 重构为统一的 `checking-solutions` Skill

**Files:**
- Create: `skills/checking-solutions/SKILL.md`
- Create: `skills/checking-solutions/references/sdd-contract-chain.md`
- Move: `skills/challenging-change-specs/references/framework-map.md` → `skills/checking-solutions/references/framework-map.md`
- Delete: `skills/challenging-change-specs/SKILL.md`

**Interfaces:**
- Consumes: 已形成的普通方案或 SDD 变更包及其问题、需求、代码、测试和执行证据。
- Produces: 普通分支的质检发现；或普通发现加 SDD 契约链结果。每条发现均为“位置—直接证据—断点—影响—最小补证／修正方向”。

- [ ] **Step 1: 移动目录和框架映射**

```bash
mkdir -p skills/checking-solutions/references
git mv skills/challenging-change-specs/references/framework-map.md \
  skills/checking-solutions/references/framework-map.md
```

- [ ] **Step 2: 写核心 `SKILL.md`**

核心文件按以下顺序编写，控制为普通方案所需的最小上下文：

```markdown
---
name: checking-solutions
description: 用于 AI 已生成或接收研发解决方案、修复方案、实施方案或 SDD 变更包，需要在交付、实施或归档前质检方案是否对应问题与约束，是否存在样例耦合、作用点错位或证据链断点时。
---

# 质检解决方案

读取已经形成的方案及其问题、需求和证据，查找会让实现对当前案例有效、却无法支持目标行为的断点。只报告可定位发现和未验证范围；不参与原方案生成，不替负责人审批，不默认重写完整方案。

## 固定质检范围

记录原问题或目标、方案版本、方案声称解决的范围、实际读取的需求／代码／测试／运行证据。材料缺失时保留未验证连接，不补写原因或规则。

## 检查对症链

沿“问题或目标 → 已知依据 → 方案作用点 → 预期行为变化 → 验证证据”逐段检查：

1. 样例耦合：常量、字符串、错误码、用户、地区、测试数据、调用路径或措辞是否只来自当前案例，缺少业务规则、系统约束或失败机制依据。
2. 作用点错位：方案是否修改真正控制目标行为的 seam；局部入口补丁是否遗漏共享路径，文案或 Prompt 修改是否掩盖状态、工具、数据或编排问题。
3. 闭环断点：依据能否支持该方案，方案能否推出声称的行为变化，验证能否观察该变化。
4. 范围夸大：止损、防护、单点修复或单次通过是否被描述成根因修复、全局覆盖或稳定提升。
5. 区分性验证：选择能区分“修到共同依据”和“记住当前案例”的最小探查；不固定凑测试类型或数量。

硬编码按依据判断，不按代码外形判断。已确认规则支持的常量和局部分支不是 finding；明确标注范围的止损可以成立，只检查其效果与声明是否一致。

## SDD 加深分支

先依据框架或产物关系确认属于 SDD：材料明确使用 SDD／Spec-Driven，或 proposal、spec、design、tasks、verify、archive 等产物形成需要跨角色追溯的变更链。确认后再按实施前、实施中、实施后或归档前选择阶段并读取 `references/sdd-contract-chain.md`。只有实施时点、没有 SDD 产物链的普通方案仍停在核心检查。

## 交付

每条发现写明位置、直接证据、断开的连接、影响和最小补证或修正方向。另列未验证部分和本轮证据边界。普通方案不输出批准、驳回或实施准入结论；没有发现时只说明当前范围内未发现可证明的问题，不把它写成方案已经正确。

原因尚未查清且会改变方案时，交给 `investigating-findings`；Prompt 或完整 Agent 的专属行为质量分别交给 `prompt-eval`、`agent-eval`，本 Skill 只检查它们已经形成的改进方案是否对症。

**完成条件：** 方案每项关键主张都已连接到可定位依据、作用点、行为变化和验证，或被明确标记为断点／未验证；发现不把合法业务规则误报为硬编码，不把质检结论扩大为实施批准。
```

- [ ] **Step 3: 将现有 SDD 内容迁入专属 reference**

从旧 `challenging-change-specs/SKILL.md` 原样保留并迁移以下内容：

1. “证据边界”的阶段、框架、读取范围和版本记录；
2. “产物角色”表；
3. 契约链中的行为与 oracle、技术与代码库贴合、任务与交付切分、证据与收敛；
4. 评审深度；
5. SDD 输出中的阶段关口、契约链、验收证据矩阵和 P1／P2／P3 定义；
6. `references/framework-map.md` 的条件指针。

删除与新核心重复的意图复述、证据不得夸大和 finding 基本字段，只在 `sdd-contract-chain.md` 开头声明：

```markdown
# SDD 契约链加深检查

仅在 `SKILL.md` 的 SDD 条件成立后读取。核心方案质检已经完成；本文件只增加 SDD 阶段、产物角色、任务、实现证据和归档事实检查，不重复普通方案规则。
```

- [ ] **Step 4: 删除旧入口并检查引用完整性**

```bash
git rm skills/challenging-change-specs/SKILL.md
test ! -e skills/challenging-change-specs
grep -n 'references/sdd-contract-chain.md' skills/checking-solutions/SKILL.md
grep -n 'references/framework-map.md' skills/checking-solutions/references/sdd-contract-chain.md
```

- [ ] **Step 5: 运行静态契约测试，确认只剩文档／路由失败**

```bash
python3 -m unittest tests/test_checking_solutions_contract.py -v
```

预期：新 Skill 结构相关断言通过；当前文档和 `test-privateer` 尚未改名，因此路由文档测试仍失败。

---

### Task 4: 更新路由和当前使用文档

**Files:**
- Modify: `skills/test-privateer/SKILL.md`
- Modify: `README.md`
- Modify: `docs/guide.md`
- Modify: `docs/developer-guide.md`

**Interfaces:**
- Consumes: `checking-solutions` 的统一入口和 SDD 条件。
- Produces: 普通 AI 方案与 SDD 方案都进入同一 Skill，但执行不同深度；Skill 总数仍为 22。

- [ ] **Step 1: 修改主入口路由**

将原路由：

```markdown
| SDD 变更包需要实施前、实施后或归档前的质量关口 | `challenging-change-specs` |
```

替换为：

```markdown
| AI 已形成研发／修复／实施方案，或 SDD 变更包需要交付前、实施后、归档前质检 | `checking-solutions`；SDD 由其加载契约链加深检查 |
```

并在“跨入执行”之前增加一段交付前边界：只有当前任务产出了方案草稿或用户提供了待检方案时才进入 `checking-solutions`；需求分析、原因调查和测试设计本身不因此自动变成方案质检。

- [ ] **Step 2: 更新 README 和通用指南**

将当前文档中的 `challenging-change-specs` 替换为 `checking-solutions`，描述统一为：

```markdown
`checking-solutions`：质检研发、修复和实施方案中的样例耦合、作用点错位与证据链断点；SDD 变更包额外检查规格、任务、实现和归档契约链。
```

由于是一个 Skill 替换一个 Skill，`README.md` 和 `docs/guide.md` 中“22 个 Skill”保持不变。

- [ ] **Step 3: 更新研发教程示例**

将“评方案”示例改为：

```text
使用 checking-solutions，质检这份已经形成的解决方案。
结合原问题、已确认规则和现有证据，检查是否存在只针对当前 badcase 的判断、
作用点错位、影响范围遗漏或无法证明方案有效的验证设计。
只报告具体位置、直接证据和最小补证／修正方向，不重新生成整套方案。
如果这是 SDD 变更包，再加深检查规格、任务、实现证据和归档事实。
```

- [ ] **Step 4: 运行全部静态测试**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

预期：全部 PASS。

- [ ] **Step 5: 检查当前文件不存在旧入口引用**

只检查运行时和当前文档，不修改研究、历史运行和旧压缩包：

```bash
grep -R -n 'challenging-change-specs' \
  skills README.md docs/guide.md docs/developer-guide.md tests \
  && exit 1 || true
```

- [ ] **Step 6: 提交融合实现**

```bash
git add skills/checking-solutions skills/test-privateer/SKILL.md \
  tests/test_checking_solutions_contract.py README.md docs/guide.md docs/developer-guide.md
git add -u skills/challenging-change-specs
git commit -m "feat(测试技能): 融合解决方案与SDD质检"
```

---

### Task 5: 运行候选版本行为回归并做 Skill 审计

**Files:**
- Modify only if a verified failure requires it: `skills/checking-solutions/SKILL.md`
- Modify only if SDD regression requires it: `skills/checking-solutions/references/sdd-contract-chain.md`
- No raw run files added to the repository.

**Interfaces:**
- Consumes: Task 1 的相同输入、模型、推理设置和人工判据。
- Produces: 候选版本相对基线的可复核结论；只有真实失败才允许引入下一条规则。

- [ ] **Step 1: 在新临时目录中重复六个场景**

使用 Task 1 的命令，将提示中的入口改为：

```text
读取当前目录 skills/checking-solutions/SKILL.md 及其按条件需要的 reference，然后处理 task.md。只使用当前快照和任务材料；不要读取网络、历史会话或评审答案。不要修改文件。
```

每个输入运行两次。不得复用会话或目录。

- [ ] **Step 2: 按预设判据人工评分**

发布门槛：

1. 两个 badcase 输入均能定位样例耦合或作用点／证据链断点；
2. `legitimate-local-rule` 两次均不把法规常量误报为硬编码；
3. `explicit-containment` 两次均保留明确止损方案，只纠正超范围声明；
4. 普通方案不要求 SDD 产物，不输出实施审批；
5. 两个 SDD 输入都进入加深分支，且现有阶段、任务、证据和归档检查没有丢失；
6. 任何一次环境失败单独记为 BLOCKED，不用重跑掩盖。

- [ ] **Step 3: 对真实失败做单因素修正**

一次只改一个导致失败的完成条件、条件指针或输出字段；重新运行失败输入及其最近的正常对照。不得因为措辞“不够强”就叠加“必须、绝不允许”等同义禁令。

- [ ] **Step 4: 使用 `skill-eval` 审计最终 Prompt 表面**

审计目标为实际部署模型和宿主，至少检查：描述是否误触发普通分析、普通分支是否被 SDD 内容污染、条件指针能否可靠加载、输出契约是否诱导审批、是否存在模型无依据规则。审计发现必须回到对应行为场景验证，不能凭静态意见直接改稿。

- [ ] **Step 5: 运行最终验证**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git status --short
```

预期：单元测试全部通过，`git diff --check` 无输出；`git status` 只出现本计划内文件和用户原有未跟踪文件。

- [ ] **Step 6: 如有验证后修正，单独提交**

```bash
git add skills/checking-solutions tests/test_checking_solutions_contract.py
git commit -m "fix(测试技能): 收紧方案质检边界"
```

没有验证后修正时跳过该提交，不制造空提交。

---

### Task 6: 同步本地 Skill 并验证迁移结果

**Files:**
- Sync: `skills/checking-solutions/` → `/Users/jianghongjian/.agents/skills/checking-solutions/`
- Sync: `skills/test-privateer/` → `/Users/jianghongjian/.agents/skills/test-privateer/`
- Remove after verified copy: `/Users/jianghongjian/.agents/skills/challenging-change-specs/`

**Interfaces:**
- Consumes: 已通过静态、行为和 Prompt 审计的仓库版本。
- Produces: 本地仅保留新入口，且文件内容与仓库一致；不生成发布包、不推送远端。

- [ ] **Step 1: 先复制新入口和主入口**

```bash
rm -rf /Users/jianghongjian/.agents/skills/checking-solutions
cp -R skills/checking-solutions /Users/jianghongjian/.agents/skills/checking-solutions
rm -rf /Users/jianghongjian/.agents/skills/test-privateer
cp -R skills/test-privateer /Users/jianghongjian/.agents/skills/test-privateer
```

- [ ] **Step 2: 校验新目录一致后删除旧本地入口**

```bash
diff -ru skills/checking-solutions /Users/jianghongjian/.agents/skills/checking-solutions
diff -ru skills/test-privateer /Users/jianghongjian/.agents/skills/test-privateer
rm -rf /Users/jianghongjian/.agents/skills/challenging-change-specs
test ! -e /Users/jianghongjian/.agents/skills/challenging-change-specs
```

- [ ] **Step 3: 做本地发现性检查**

启动一个全新会话，分别输入普通方案和 SDD 方案请求，确认可发现 `checking-solutions`，普通方案不进入 SDD 加深分支，SDD 方案会读取 `sdd-contract-chain.md`。

- [ ] **Step 4: 最终范围审计**

```bash
git show --stat --oneline HEAD~2..HEAD
git status --short
```

确认提交中没有 `docs/research/` 草稿、`evals/**/runs/`、事件流、临时输出、`dist/` 包或用户原有未跟踪文件。

---

## 完成标准

- 仓库和本地只保留 `checking-solutions` 一个方案质检入口。
- 普通方案能够检测样例耦合、作用点错位、闭环断点、范围夸大和验证缺口。
- 合法业务常量、合理局部规则和明确止损不会被机械误报。
- SDD 方案保留原有阶段、框架、delta、任务、证据和归档检查。
- 普通方案不会被要求补齐 SDD 产物，SDD 方案不会只做轻量扫描。
- Skill 只报告发现和未验证范围，不参与原方案生成，不替负责人审批。
- 静态测试、行为回归和 `skill-eval` 均通过，结论不超过实际证据。
- Git 中没有原始运行输出、过程日志、发布包或无关研究文件。
