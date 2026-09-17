# Prompt Eval 与 Agent Eval Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 增加 Prompt 与 Agent 两项独立质检 Skill，并接入 Test Privateer 路由与用户文档。

**Architecture:** 两个 model-invoked Skill 分别承载 Prompt 当前适配和 Agent 系统质检。核心步骤留在入口，条件性检查通过 references 渐进披露；不引入评测平台、脚本或新的运行时框架。

**Tech Stack:** Markdown Agent Skills、Python 标准库契约检查、Codex CLI 行为探针。

**Spec:** `docs/superpowers/specs/2026-09-17-prompt-agent-eval-skills-design.md`

## Global Constraints

- 两个 Skill 均为辅助、纠偏和质检能力。
- Prompt 模型适配内化在 `prompt-eval`，不外调 `skill-eval`。
- 不新增评测平台、依赖或自动化执行脚本。
- 结论强度不超过实际执行证据。
- 保留现有独立／项目路径、执行授权和产物路由。

---

### Task 1: 契约测试与 Skill 骨架

**Files:**
- Create: `tests/test_eval_skills_contract.py`
- Create: `skills/prompt-eval/SKILL.md`
- Create: `skills/prompt-eval/references/prompt-review-patterns.md`
- Create: `skills/agent-eval/SKILL.md`
- Create: `skills/agent-eval/references/agent-quality-model.md`
- Create: `skills/agent-eval/references/evaluator-checks.md`

**Interfaces:**
- Consumes: Agent Skills frontmatter 与仓库目录规范。
- Produces: `prompt-eval`、`agent-eval` 两个可发现入口。

- [ ] 编写失败的目录、frontmatter、引用和核心边界契约检查。
- [ ] 运行 `python3 -m unittest tests/test_eval_skills_contract.py -v`，确认因文件缺失失败。
- [ ] 写入两个最小 Skill 与按需 references。
- [ ] 重跑契约检查并通过。

### Task 2: 主入口和用户文档接入

**Files:**
- Modify: `skills/test-privateer/SKILL.md`
- Modify: `README.md`
- Modify: `docs/developer-guide.md`
- Modify: `tests/test_eval_skills_contract.py`

**Interfaces:**
- Consumes: 两个新 Skill 名称和触发边界。
- Produces: 主入口路由、22项能力清单和研发调用示例。

- [ ] 先增加路由／文档失败断言并确认失败。
- [ ] 更新主入口、README 和研发教程。
- [ ] 重跑契约检查并执行 `git diff --check`。

### Task 3: 行为验证与 Skill Eval 审计

**Files:**
- Create: `evals/prompt-agent-eval/README.md`
- Create: `evals/prompt-agent-eval/inputs/*.md`
- Create: `docs/research/2026-09-17-prompt-agent-eval-skill-validation.md`

**Interfaces:**
- Consumes: 新 Skill 与真实边界样例。
- Produces: 实际回复、判定结果、目标模型适配审计和限制。

- [ ] 为 Prompt 失败、Prompt 信息不足、Agent 方案审查、普通测试不误路由准备样例和判据。
- [ ] 在隔离临时目录运行 Codex CLI，保留原始回复和事件。
- [ ] 检查实际结果；只根据复现问题修改 Skill。
- [ ] 执行 skill-eval 的提示面盘点、来源检查、模式扫描和候选 diff；记录空 diff 也属于有效结果。
- [ ] 运行完整契约检查、引用检查与 `git diff --check`。
