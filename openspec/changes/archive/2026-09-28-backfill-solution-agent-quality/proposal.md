# Proposal

## Why

已合并的方案与 Agent 质检缺少统一可追溯的当前规格。按用户授权于 2026-09-28 回填历史，不重新开发，不声明原提交采用过 OpenSpec。

## What Changes

- 从基线 `351985269815995ee69dcf5cbeb4842c1fb59010` 抽取现有契约，建立当前规格并归档本次回填。
- 来源：`56403b6`、`6ea4965`、`e321468`、`dc074c7`、`0fbbfa1`，以及 `3519852` 的完成边界部分。这是能力分组，不是一条历史提交的复刻。
- 非目标：修改运行时 Skill、重跑全部行为评测、将未交付方案计为完成。

## Capabilities

### New Capabilities

- `solution-agent-quality`：首次登记方案与 Agent 质检的当前契约；能力本身已在源码实现。

### Modified Capabilities

无；迁移前没有 OpenSpec 当前规格。

## Impact

源码核对范围：`skills/checking-solutions/`、`skills/prompt-eval/`、`skills/agent-eval/`、`docs/developer-guide.md` 和 `docs/prompt-agent-eval-guide.md`。本次仅新增管理资产；档案只证明回填，不证明普遍行为稳定。
