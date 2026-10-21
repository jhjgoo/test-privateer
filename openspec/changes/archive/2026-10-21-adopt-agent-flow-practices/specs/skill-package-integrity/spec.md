# Spec Delta

## Purpose

规定仓库发布源和目标平台 Skill 包在交付前的确定性完整性检查，防止 frontmatter、引用、路由、计数和平台结构问题进入人工试错。

## ADDED Requirements

### Requirement: Validate source skills before release

仓库 SHALL 提供一个可运行检查，验证每个 `skills/*/SKILL.md` 的 frontmatter 能被 YAML 解析、必填字段存在且非空、正文存在、文件引用路径存在，并核对主入口路由表提到的 Skill 均实际存在；检查 SHALL 输出明确失败位置。

#### Scenario: Frontmatter contains a colon in description

- **WHEN** 一个 Skill 的 description 包含未加引号的冒号并导致 YAML 解析失败
- **THEN** 检查 SHALL 以非零状态失败，并指出该文件和解析错误行

#### Scenario: Router references a missing skill

- **WHEN** 主入口路由表引用不存在的 Skill 名称
- **THEN** 检查 SHALL 以非零状态失败，并列出缺失名称

### Requirement: Validate target platform packages structurally

目标平台包检查 SHALL 支持至少一种显式配置，声明压缩包根入口、允许目录深度、文件数量与大小上限；检查 SHALL 在压缩包内容上执行，而不是仅检查构建目录。

#### Scenario: Workbuddy package has nested directories

- **WHEN** 目标平台限制为两级目录，而压缩包存在 `references/skills/foo/SKILL.md`
- **THEN** 检查 SHALL 失败并列出超限路径

#### Scenario: Valid flat aggregate package

- **WHEN** 压缩包根目录含 `SKILL.md`，所有文件路径不超过二级，大小和数量在限制内
- **THEN** 检查 SHALL 通过，并报告文件数、路径深度和包大小
