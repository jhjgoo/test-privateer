# Proposal

## Why

已合并的测试工作流缺少统一可追溯的当前规格。按用户授权于 2026-09-28 回填历史，不重新开发，不声明原提交采用过 OpenSpec。

## What Changes

- 从基线 `351985269815995ee69dcf5cbeb4842c1fb59010` 抽取现有契约，建立当前规格并归档本次回填。
- 来源：`133e621` 至 `99d51c6`（连续 13 个提交，含 `964aa0e`、`2e5f78e`、`a581d25`）。这是能力分组，不是一条历史提交的复刻。
- 非目标：修改运行时 Skill、重跑全部行为评测、将未交付方案计为完成。

## Capabilities

### New Capabilities

- `testing-workflow`：首次登记测试工作流的当前契约；能力本身已在源码实现。

### Modified Capabilities

无；迁移前没有 OpenSpec 当前规格。

## Impact

源码核对范围：`skills/test-privateer/`、`skills/clarifying-test-basis/`、`skills/investigating-findings/`、`skills/analyzing-change-for-testing/`、`skills/selecting-regression-tests/` 和 `docs/guide.md`。本次仅新增管理资产；档案只证明回填，不证明普遍行为稳定。
