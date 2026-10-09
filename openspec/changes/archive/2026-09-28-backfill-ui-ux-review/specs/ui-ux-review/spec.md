# Spec Delta

## Purpose

规定界面与使用体验专项如何沿用户任务选择评审方法、适用依据和下一探查。截图、设计约定、操作记录、用户观察和扫描报告各有证据边界，专项不绑定工具品牌，也不接管无关的接口或实现任务。

## ADDED Requirements

### Requirement: Review user tasks using applicable evidence
UI/UX 评审 SHALL 将界面问题连接到用户任务、对象或状态、观察、适用依据及用户后果，并按缺口选择最小补证动作。

#### Scenario: Screenshot-only review
- **WHEN** 只有截图而没有操作轨迹
- **THEN** 完成可见内容评审，动态焦点、点击和恢复保持未知，不把截图当作实际操作成功或失败的证据

#### Scenario: Approved visual change
- **WHEN** 有效设计批准了相应外观变化
- **THEN** 区分预期变化与未测体验，不因与历史截图不同直接判缺陷

### Requirement: Keep methods and conclusions proportional
专项 SHALL 按问题选择视觉、交互、无障碍或可用性方法，区分标准适用范围、同源报告、自动完成与真实用户表现。

#### Scenario: Equivalent reports from one run
- **WHEN** 两份报告来自同一次原始采集
- **THEN** 可以互相定位发现，但不作为两次独立复现；不因报告品牌不同改变实质判定

#### Scenario: Unrelated API request
- **WHEN** 用户只要求公开接口规则测试，未要求界面评审
- **THEN** 保持接口范围，不因材料出现页面名而启动全套 UI/UX 检查
