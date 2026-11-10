## MODIFIED Requirements

### Requirement: Validate source skills before release

仓库 SHALL 提供一个可运行检查，验证每个 `skills/*/SKILL.md` 的 frontmatter 能被 YAML 解析、必填字段存在且非空、正文存在、文件引用路径存在，并核对主入口路由表提到的 Skill 均实际存在；检查 SHALL 输出明确失败位置。路由解析 SHALL 与主入口实际结构一致，未找到预期结构、未提取有效路由或解析失败时 MUST 非零退出；MUST NOT 将空目标集合视为全部目标存在。路由表 SHALL 保持唯一来源，不新增需要手工同步的检查清单。

#### Scenario: Frontmatter contains a colon in description

- **WHEN** 一个 Skill 的 description 包含未加引号的冒号并导致 YAML 解析失败
- **THEN** 检查 SHALL 以非零状态失败，并指出该文件和解析错误行

#### Scenario: Router references a missing skill

- **WHEN** 主入口路由表引用不存在的 Skill 名称
- **THEN** 检查 SHALL 以非零状态失败，并列出缺失名称

#### Scenario: Router extraction silently becomes empty

- **WHEN** 主入口标题或结构变化导致检查器无法提取有效路由，或路由区确实为空
- **THEN** 检查 SHALL 非零退出并定位主入口的结构或空路由问题，不报告包完整性通过

#### Scenario: Missing skill is injected into the current route table

- **WHEN** 在当前真实路由表中将一个目标替换为不存在的 Skill
- **THEN** 检查 SHALL 观察该改动并列出缺失名称；仍通过即为检查器失败，不以其他静态测试成功掩盖


## ADDED Requirements

### Requirement: Resolve runtime resources from the installed skill

随包脚本、必需参考和运行说明 SHALL 从实际加载的 Skill 安装目录解析，兼容仓库、全局安装和项目安装场景，不依赖调用方当前工作目录、维护者绝对路径或未分发的仓库文档。可选研究材料 SHALL 标明可选，不得成为安装后完成任务的隐含前置；执行所需规则 SHALL 在包内可达。

#### Scenario: XMind runs from an unrelated working directory

- **WHEN** 用户从普通项目调用全局或项目级安装的 XMind 导出 Skill，当前目录不是 Skill 仓库
- **THEN** Agent SHALL 定位该次实际加载目录内的脚本并完成获准转换，不调用当前目录下不存在的 skills 路径

#### Scenario: Packaged review lacks the repository research directory

- **WHEN** 方案质检 Skill 安装包不包含仓库 docs/research 目录
- **THEN** 必需方法 SHALL 仍由包内可达参考支持，可选来源缺失不阻塞质检，不声称读取了不存在的研究文件
