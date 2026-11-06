# Design

## Context

见 [proposal.md](proposal.md)。Test Privateer 已把 DeepEval 实现交给 Confident AI 官方 Skills，但官方 Skill 缺失时只有错误状态，没有用户可确认的恢复动作。项目配置保存长期项目约定，宿主 Skill 和 Python 环境则可能随机器或会话变化。

## Goals / Non-Goals

**Goals:**

- 在 Setup 和实际 DeepEval 入口检查当前宿主是否具备所需官方 Skill。
- 在安装官方 Skill 前展示最小影响并取得明确确认。
- 安装后重新检查实际可用性，失败时保留可诊断状态。
- 保持项目框架选择、宿主就绪状态和执行授权彼此独立。

**Non-Goals:**

- 不在 Test Privateer 中实现 DeepEval API、模板或安装脚本。
- 不自动安装 Python 包、修改锁文件、登录 Confident AI、上传数据或启用付费 Judge。
- 不把当前机器的安装状态写成长期项目规则。
- 不为其他测试框架建立通用依赖管理器。

## Decisions

### 1. 复用宿主安装能力，不维护本地安装实现

缺少官方 Skill 时，Agent 说明需要的 Skill、官方来源、安装范围和后续复检，再请求用户确认。未决定且尚未运行评测时，顶层使用 `awaiting_install_confirmation`；等待用户选择不是一次评测结果，不进入 `agent-eval` 的四类结果。确认后使用宿主已有的 Skill 安装能力；宿主没有安装能力时仍返回 `missing_official_skill`。

安装位置和作用域由宿主安装能力与用户选择决定；没有宿主安装入口时，不自行把官方 Skill 复制进项目目录。这比在仓库内维护克隆命令或安装脚本更小，也避免官方仓库结构变化后本地教程漂移。

### 2. Setup 与运行入口都检查

Setup 在项目选择 DeepEval 时提前暴露缺口；`evaluating-agents-with-deepeval` 在真正实施前再次检查。后者不能依赖历史 Setup 结论，因为运行可能发生在另一宿主或官方 Skill 已被删除、升级。

### 3. 一次确认只授权官方 Skill 安装

用户确认安装官方 Skill，不等于授权安装 Python 依赖、修改项目文件、登录、上传、调用外部 Judge 或产生费用。这些动作继续由官方 Skill 和项目规则按各自边界确认。

### 4. 就绪结果不进入项目配置的长期事实区

`.test-privateer/project.md` 只记录项目选择 DeepEval 的权威来源和项目入口。当前宿主的官方 Skill、Python 包或入口可运行状态只在 Setup 结果中报告；下一次使用时重新核对。

### 5. 未确认时保持诚实降级

用户拒绝、未回答、宿主不支持安装或安装后仍不可读时，DeepEval 实施保持 `environment_error: missing_official_skill`。框架无关的质量主张、自然场景和确定性 Oracle 可以继续，但不得声称 DeepEval 资产已建立或运行。

## Risks / Trade-offs

- [不同宿主的 Skill 安装机制不同] → 只要求调用当前宿主已有能力，不硬编码命令；不可用时保留恢复来源。
- [模型把宿主 Skill 当成项目资产复制] → 明确禁止自行创建项目内 Skill 目录、克隆或下载，安装目标交给宿主安装器和用户选择。
- [确认问题打断 Setup] → 只在项目已选择 DeepEval 且官方 Skill 确实缺失时询问，不为普通项目或自有框架增加步骤。
- [安装确认被误解为全面执行授权] → 明确列出未授权的 Python 依赖、登录、上传、费用和项目修改。
- [Setup 报告很快失效] → 不持久化宿主就绪状态，实际评测入口必须复检。

## Migration Plan

更新生产 Skill、契约测试和一个自然 Setup 场景。现有选择其他框架、未选择框架或已安装官方 Skill 的路径保持不变。回滚时移除就绪确认段即可恢复原 `missing_official_skill` 行为，不涉及项目数据迁移。
