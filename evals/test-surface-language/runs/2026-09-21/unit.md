# TDD 单元测试表面 RED／GREEN 对照

- Run ID：`test-surface-language-unit-20260921-185046-cst`
- 日期：2026-09-21（Asia/Shanghai）
- 宿主：同一 Codex collaboration agent 在一个上下文中依次生成 RED 与 GREEN；具体模型、reasoning effort 和底层编排标识未由宿主暴露，也没有使用彼此隔离的新上下文。本轮未读取产品源码，未创建或运行产品测试，因此是定性无退化观察，不是可归因的配对实验。
- Baseline：commit `b99564dadfbf7b55d218e54aecb1d12323e042d7` 中 `git show HEAD:skills/writing-unit-tests/SKILL.md` 与 `git show HEAD:skills/test-privateer/SKILL.md`。
- Baseline Skill SHA-256：`writing-unit-tests=8d9572f900597ada66649a65deba9d794c7e39b1144962ea4964e97be6377b2a`；`test-privateer=2061ce47279788736ad6694b9e91dabb7bce48d59856223e018ca934d303d2fc`。
- Candidate：工作区当前 `skills/writing-unit-tests/SKILL.md` 与 `skills/test-privateer/SKILL.md`。
- Candidate Skill SHA-256：`writing-unit-tests=292ab42c543efef7b88b83533b8721020ad3901c2996bd5c05ed813dc16f384b`；`test-privateer=e80a8a465b3ea3134a2e893961db500a12de2bd619cb23838171ca02603737e0`。
- 固定输入：`evals/test-surface-language/input.md`
- 输入 SHA-256：`cfeb26a4f4af6c92d8d847d608bd161621c5fd5caa7324ca50f6596f7dd296e7`
- 对照控制：两次使用相同固定输入和相同 probe；只替换上述两个 Skill 的版本。下方保留生成正文，未用评分摘要替代原始内容。

## 精确 probe

> 为固定输入设计一个 TDD RED 单元测试切片。说明 seam、Given/When/Then、必须保留的真实符号/类型/fixture/替身/运行命令/预期 RED 原因，以及不应进入行为 oracle 的实现细节。没有真实源码和命令时如实标记。

## RED 原始输出

> 来源：baseline Skill。以下为当次生成正文。

### 分支与边界

这是“只有测试设计／没有代码访问权”分支：只能交付可实现的 RED 切片，不能声称已写入测试或取得真实 RED。

### 最小行为切片

**行为：** `/open` 的调用企业已停用时，拒绝场景查询。

**Seam：** 从路由处理器的公开请求边界调用 `GET /open/scenarios/{tenantCode}`，观察 HTTP 响应。输入没有给出处理器的真实导出符号，因此不写成某个臆造的函数名或测试代码。实现前需先在目标项目中确认这个真实 seam。

**Given**

- 一个可通过有效 Bearer Token 识别、但已停用的调用企业。
- 路径中是另一个已启用目标企业的 `tenantCode`，且该目标企业存在可返回的场景，以排除 404 或空列表分支。
- 认证和数据读取使用项目现有 fixture／fake／stub；材料没有提供它们的真实名称或协议，待源码确认。

**When**

- 用该 Token 请求 `GET /open/scenarios/{tenantCode}`。

**Then**

- HTTP 状态为 `403`。
- 响应的 `messageCode` 为 `ADT_SERVICE_TENANT_FORBIDDEN`。

这两个 expected 直接来自固定输入的可观察接口合同，是本切片的 oracle。

### 必须保留的信息

- 已确认的真实合同符号：`GET`、`/open/scenarios/{tenantCode}`、`tenantCode`、Bearer Token、HTTP `403`、`messageCode`、`ADT_SERVICE_TENANT_FORBIDDEN`。
- 真实代码符号与输入／输出类型：**未提供**。不能把“`GET`处理器”、“`Response`”或任意 DTO 写成已确认项目符号。
- fixture：需要“已停用的调用企业”、“已启用的目标企业”、“目标企业中的可返回场景”；项目内真实 fixture builder 和字段结构 **未提供**。
- 替身：需代表“Token 映射到调用企业”和“读取目标企业／场景”的依赖协议；真实依赖符号和返回类型 **未提供**。实现时优先沿用项目现有 fake，其次 stub；只有外部动作本身是合同时才验证交互。
- 测试文件、框架和精确运行命令：**未提供**；不得假设 Vitest／Jest／pytest，也不得编造文件路径和 `-t` 参数。

### 预期 RED

实现测试后，只有在断言差异准确表明“已停用的调用企业未被拒绝”时才是有效 RED，例如预期 `403` 而实际继续返回了 `200`，或返回了其他 `messageCode`。若是导入、类型、fixture 或替身协议错误，那是 ERROR 或错因失败，不是有效 RED。当前未有真实测试与命令，所以 **未运行，未取得 RED 证据**。

### 不应进入行为 oracle 的实现细节

- Prisma 查询是否被调用、调用次数、查询顺序及完整 `where`／`select`／`include` 形状。
- 调用企业、目标企业在数据库中的内部 ID 或局部变量名。
- 私有 helper，中间 DTO，日志事件，以及“先查调用企业还是先查目标企业”。
- `Tenant.code`、`TenantExternalCode.code`、`releasedAt`、`tenantId` 属于技术依据；本切片的 Then 不以这些内部字段为判定对象。

### 交接

先在目标项目中确认路由处理器的真实导出符号、请求／响应类型、现有 fixture／替身和最窄测试命令，再把上述切片落成代码并取得原始断言差异。

## GREEN 原始输出

> 来源：candidate Skill。以下为当次生成正文。

### 分支与状态

当前只有行为材料，没有目标项目源码、现有测试或命令。因此本轮是“无代码访问权的测试设计”：交付一个可落地的单元层 RED 切片，但不声称已编写、运行或得到 RED。

### 切片：停用的调用企业被拒绝

**Seam**

选取 `/open` 路由处理器的真实导出函数作为最窄稳定 seam，从调用者能使用的请求边界传入 Bearer Token 和 `tenantCode`，通过公开响应类型观察结果。材料只确认公开路径 `GET /open/scenarios/{tenantCode}`，**没有提供导出函数名、模块路径、请求类型或响应类型**。实现时必须使用源码中的真实符号，这里不用 `GET`、`handler`、`Request` 或 `Response` 等占位名冒充真实符号。

**Given**

- 认证依赖返回一个已停用的调用企业 fixture。
- 路径参数 `tenantCode` 指向另一个已启用的目标企业。
- 目标企业有至少一个已启用且存在当前策略版本的场景，避免其他拒绝或空结果遮蔽本行为。
- 使用项目现有的认证替身和数据读取替身，并保留它们的真实参数、返回类型和关键数据结构。输入未提供这些符号和类型，所以当前只能标记为待源码确认。

**When**

- 调用上述真实处理器 seam，发起一次对 `GET /open/scenarios/{tenantCode}` 的查询。

**Then**

- 公开响应状态为 HTTP `403`。
- 公开响应字段 `messageCode` 等于 `ADT_SERVICE_TENANT_FORBIDDEN`。

Oracle 依据是固定输入中的可观察接口合同。两个断言共同证明一个拒绝行为。

### 必须保留的 seam 信息

| 类别 | 实现时必须保留 | 当前状态 |
| --- | --- | --- |
| 真实符号 | 路由处理器的导出名、导入路径，以及真实的 `tenantCode` 参数承载位置 | 未提供；只已确认 HTTP 合同中的 `GET` 和 `tenantCode` |
| 类型 | 处理器输入／输出类型、认证结果类型、数据替身的参数与返回类型 | 未提供 |
| fixture | 已停用调用企业、已启用目标企业、目标场景与当前策略版本；沿用项目 fixture builder 及其真实必填字段 | 业务含义已知；真实 builder／字段未提供 |
| 替身 | 认证依赖与数据读取依赖的项目现有 fake／stub，包含真实协议的关键结构 | 符号与协议未提供；不强行把 Prisma mock 当成必选 seam |
| 运行命令 | 只运行该测试文件／用例的项目真实命令 | 未提供；不编造 Vitest／Jest／pytest 命令 |

### 预期 RED 原因与验收

目标行为缺失时，测试应在公开响应断言上失败：例如期望 HTTP `403`，实际得到 `200`；或状态为 `403` 但 `messageCode` 不是 `ADT_SERVICE_TENANT_FORBIDDEN`。原始断言差异必须指向“已停用的调用企业没有被正确拒绝”。

如果首次运行失败于编译、导入、fixture 或替身配置，这是 ERROR，不是有效 RED；如果测试 PASS，需要调查行为是否已存在或断言是否无效。当前因缺少源码、测试文件和命令，状态是 **“仅完成切片，未运行，未取得真实 RED”**。

### 不进入行为名称或 oracle 的实现细节

- Prisma 方法名、查询次数、调用顺序和完整查询对象。
- `Tenant.code`、`TenantExternalCode.code`、`releasedAt`、`tenantId` 这些 seam 以下的持久化字段。若真实 fixture／替身协议需要其中某些字段，可在 Arrange 中保留协议必需结构，但 Then 不断言它们。
- 私有 helper，局部变量，日志，中间 DTO，以及先查哪张表。
- 除非外部动作本身是合同，不断言内部依赖的交互次数。

## 按 README 标准评分

README 对 TDD 单元测试的通过条件是：“保留所选 seam 上的真实符号、输入输出、异常、fixture、替身、命令和 RED 原因；seam 以下的实现细节不进入行为名称或 oracle。”本输入明确未提供项目源码、测试符号和运行命令，因此“如实标记缺口”是正确行为，不作扣分。每项 0 或 1 分，共 8 分。

| 评分项 | RED baseline | GREEN candidate | 证据 |
| --- | ---: | ---: | --- |
| seam 明确且从调用者边界观察 | 1 | 1 | 两者均选 `/open` 公开请求／响应边界，并标记真实导出符号待查。 |
| Given／When／Then 完整，且只有一个主行为 | 1 | 1 | 均聚焦“停用的调用企业被 403 拒绝”。 |
| 真实符号、输入／输出类型保留，未知项不臆造 | 1 | 1 | 均保留已知 HTTP 合同；对代码符号和类型明确标记未提供。 |
| fixture 有业务含义并保留项目真实结构 | 1 | 1 | 均说明三类必需 fixture，并把未知 builder／字段留待源码确认。 |
| 替身保留真实协议，不滥用交互断言 | 1 | 1 | 均需要认证与数据读取替身，且没有编造符号或强制断言 Prisma 调用。 |
| 运行命令与执行状态诚实 | 1 | 1 | 均明确命令未提供、未运行，没有编造框架或 RED。 |
| 预期 RED 原因指向目标行为缺失 | 1 | 1 | 均要求原始断言差异指向预期 403／禁止码与实际结果的差异，并区分 ERROR。 |
| seam 以下实现细节不进入行为 oracle | 1 | 1 | 均排除 Prisma 交互、查询形状／顺序、私有 helper 以及 `Tenant.code`／`releasedAt`／`tenantId` 等持久化细节。 |
| **合计** | **8/8，PASS** | **8/8，PASS** | 候选 Skill 没有造成单元测试信息丢失；它将“保留 seam 上真实信息／只隐藏 seam 以下细节”表达得更显式。 |

## 结论边界

本例中 baseline 已能通过 TDD 单元测试标准，candidate 保持该行为并更清楚地划出“seam 上真实信息”与“seam 以下实现细节”的边界。这是一组同上下文定性回归，只支持“本次输出未观察到回归”；不代表统计稳定性、因果提升或已对真实项目取得 RED。
