# Proposal

## Why

已合并的用例与报告质量缺少统一可追溯的当前规格。按用户授权于 2026-09-28 回填历史，不重新开发，不声明原提交采用过 OpenSpec。

## What Changes

- 从基线 `351985269815995ee69dcf5cbeb4842c1fb59010` 抽取现有契约，建立当前规格并归档本次回填。
- 来源：`3a4d1b5`、`b17cce4`，以及 `3519852` 的表达、语义保真和区分力部分。这是能力分组，不是一条历史提交的复刻。
- 非目标：修改运行时 Skill、重跑全部行为评测、将未交付方案计为完成。

## Capabilities

### New Capabilities

- `test-artifact-quality`：首次登记用例与报告质量的当前契约；能力本身已在源码实现。

### Modified Capabilities

无；迁移前没有 OpenSpec 当前规格。

## Impact

源码核对范围：`skills/test-privateer/references/artifact-routing.md`、`skills/designing-test-experiments/`、`skills/writing-unit-tests/`、`skills/challenging-test-designs/`、`skills/assessing-test-confidence/`、`skills/exporting-test-cases-to-xmind/`。本次仅新增管理资产；档案只证明回填，不证明普遍行为稳定。
