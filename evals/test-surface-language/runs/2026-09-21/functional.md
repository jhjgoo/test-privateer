# 功能／公开 API Case Skill 行为对照

## 运行元数据

- 日期：2026-09-21
- RED run id：`functional-red-20260921-01`
- GREEN run id：`functional-green-20260921-01`
- 运行方式：同一 Codex collaboration agent 在一个上下文中依次生成 RED 与 GREEN；具体模型、reasoning effort 和底层编排标识未由宿主暴露，也没有使用彼此隔离的新上下文。因此本记录是定性前后观察，不是可归因的配对实验。
- Baseline 来源：提交 `b99564dadfbf7b55d218e54aecb1d12323e042d7`（`git show HEAD:skills/designing-test-experiments/SKILL.md`、`git show HEAD:skills/test-privateer/SKILL.md`）
- Baseline Skill SHA-256：`designing-test-experiments=0c0b6dc5e938103efe5f784260ef0f9374362366a96f85a7331a61769607d187`；`test-privateer=2061ce47279788736ad6694b9e91dabb7bce48d59856223e018ca934d303d2fc`。
- Candidate 来源：工作区当前 `skills/designing-test-experiments/SKILL.md`、`skills/test-privateer/SKILL.md`
- Candidate Skill SHA-256：`designing-test-experiments=de82b3b1822b71f8203ff438e18b07e746501a887021c19953f488f06f5c55fa`；`test-privateer=e80a8a465b3ea3134a2e893961db500a12de2bd619cb23838171ca02603737e0`。
- 固定输入：`evals/test-surface-language/input.md`
- 固定输入 SHA-256：`cfeb26a4f4af6c92d8d847d608bd161621c5fd5caa7324ca50f6596f7dd296e7`
- 结论边界：只比较上述两个 Skill 版本对同一功能／公开 API Case 任务的输出行为；没有执行产品测试。

## 精确 probe

> 面向手工/公开 API 功能测试人员，为固定输入生成 4 条代表 Case，覆盖 /open 跨企业查询、调用企业停用、/public 编码解绑、数据读取失败。使用 Case 表格，并标明当前条件。

## RED 原始输出

以下为 `functional-red-20260921-01` 的完整原始生成内容，未做摘要或改写。

```markdown
| ID | 关联风险／依据 | 本轮安排 | 要检查什么 | 场景／前置条件 | 怎么操作 | 预期结果 | 需要保留什么 | 当前条件 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | `/open` 应按路径中的目标企业编码查询，而不是按调用方企业查询 | P0 | 跨企业查询返回目标企业的场景 | 创建启用的调用企业 A 和目标企业 B，保证两者 `tenantId` 不同；为 B 配置启用且有当前策略版本的场景；取得 A 的有效 Bearer Token | 使用 A 的 Token 调用 `GET /open/scenarios/{tenantCode}`，其中 `tenantCode` 为 B 的 `Tenant.code` | HTTP 200；返回 B 的启用场景，不返回 A 的场景；结果按名称升序 | 请求、状态码、响应体，以及 A/B 的 `tenantId` 对照 | 待准备企业、Token、场景及数据库数据 |
| C-002 | 停用调用企业不得继续通过 `/open` 查询 | P0 | 调用企业停用时鉴权后的租户状态检查 | 将调用企业对应 `Tenant` 记录设为停用，保留有效 Token；目标企业保持启用 | 调用 `GET /open/scenarios/{tenantCode}` | HTTP 403，`messageCode=ADT_SERVICE_TENANT_FORBIDDEN` | 请求、状态码、响应体、调用企业停用记录 | 待提供企业停用和 Token 准备能力 |
| C-003 | 已解绑的外部编码不得解析到原企业 | P0 | `/public` 不使用已解绑编码 | 创建外部编码记录并关联启用企业，再将 `TenantExternalCode.releasedAt` 设为非空 | 调用 `GET /public/scenarios/{entCode}` | HTTP 404，`messageCode=ADT_SERVICE_TENANT_NOT_FOUND` | 请求、状态码、响应体、外部编码记录 | 待准备外部编码及解绑数据 |
| C-004 | 数据读取异常不得泄漏内部信息 | P1 | Prisma 读取失败时的统一错误响应 | 准备可命中查询的企业与场景，使 Prisma 查询抛出异常 | 调用对应的 `/open` 或 `/public` 查询接口 | HTTP 500，`messageCode=ADT_SERVICE_DATA_READ_FAILED`；响应不包含 SQL、堆栈或连接串 | 请求、状态码、完整响应体和服务端错误日志 | 待提供 Prisma 故障注入或替身能力 |
```

## GREEN 原始输出

以下为 `functional-green-20260921-01` 的完整原始生成内容，未做摘要或改写。

```markdown
| ID | 关联风险／依据 | 本轮安排 | 要检查什么 | 场景／前置条件 | 怎么操作 | 预期结果 | 需要保留什么 | 当前条件 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | `/open` 的路径编码选择目标企业；有效 Token 只证明调用方身份 | P0：证明跨企业解析的核心证据链 | 跨企业查询使用目标企业数据且结果过滤、排序正确 | 准备两个不同的启用企业 A、B；A 可取得有效 Bearer Token；B 有独立的平台企业编码，并配置至少两个名称顺序相反、已启用且有当前策略版本的场景；A 另有可区分场景 | 携带 A 的 Bearer Token，请求 `GET /open/scenarios/{tenantCode}`，路径使用 B 的平台企业编码 | HTTP 200；只返回 B 中已启用且有当前策略版本的场景，不返回 A 的场景，并按名称升序排列 | 请求路径和认证信息、HTTP 状态、完整响应体、用于区分 A/B 的业务测试数据清单 | **当前不可执行**：材料未提供企业创建、场景配置和 Token 获取入口，需补齐可由功能测试人员使用的页面、接口或 fixture |
| C-002 | `/open` 合同规定调用企业停用时返回禁止访问 | 先补条件，再执行 | 停用的调用企业不能使用仍持有的 Token 查询目标企业 | 准备启用的调用企业 A、启用的目标企业 B 和 A 的有效 Bearer Token；通过企业管理能力停用 A，B 保持启用 | 携带 A 的 Token 请求 `GET /open/scenarios/{tenantCode}`，路径使用 B 的平台企业编码 | HTTP 403，`messageCode=ADT_SERVICE_TENANT_FORBIDDEN` | 停用动作的可观察结果、请求、HTTP 状态和响应体 | **当前不可执行**：没有提供企业停用入口，也未说明停用后既有 Token 是否可继续用于验证；待补入口并核实 Token 条件 |
| C-003 | `/public` 已解绑的外部企业编码不可用 | 先补条件，再执行 | 编码解绑后不再解析到原关联企业 | 准备启用企业 B；通过编码管理能力将外部企业编码 E 绑定到 B，确认绑定生效后再解绑 E | 请求 `GET /public/scenarios/{entCode}`，路径使用已解绑的 E | HTTP 404，`messageCode=ADT_SERVICE_TENANT_NOT_FOUND`；响应不返回 B 的任何场景 | 绑定与解绑的可观察结果、请求、HTTP 状态和响应体 | **当前不可执行**：材料未提供外部编码绑定／解绑入口；待补可由功能测试人员操作或核验的入口 |
| C-004 | 数据读取失败应转为稳定错误合同，且不得泄漏内部敏感信息 | 先补条件，再执行 | 两个公开查询入口遇到可恢复的数据读取故障时的响应 | 准备可正常查询的企业和场景；通过测试环境支持的故障控制能力启用一次可恢复的数据读取失败 | 分别请求 `GET /open/scenarios/{tenantCode}`（携带有效 Bearer Token）和 `GET /public/scenarios/{entCode}`；记录故障开启、请求和恢复过程 | 每次请求均为 HTTP 500，`messageCode=ADT_SERVICE_DATA_READ_FAILED`；响应不包含 SQL、堆栈或连接串；故障关闭后接口可恢复 | 故障控制记录、请求、HTTP 状态、完整响应体和恢复验证结果 | **当前不可执行**：没有提供读取故障模拟入口；不能把 Prisma、数据库字段或私有实现替代成功能测试操作，需补环境级故障控制手段 |
```

## 按 README 标准逐项评分

评分依据：`evals/test-surface-language/README.md` 中“功能／公开 API Case”的通过条件。

| 评分项 | RED | GREEN | 判定依据 |
| --- | --- | --- | --- |
| 执行正文只保留功能测试人员可准备、操作、观察的信息 | **FAIL** | **PASS** | RED 把 `tenantId`、`Tenant`、`TenantExternalCode.releasedAt` 和 Prisma 异常直接写入前置或操作；GREEN 将其改写为两个不同企业、企业停用、编码绑定后解绑、环境级故障控制等测试表面动作。 |
| 公开路径与认证保持精确 | **PASS** | **PASS** | 两者均保留 `/open`、`/public`、Bearer Token 及对应路径参数；GREEN 还明确 Token 证明调用方身份、路径编码选择目标企业。 |
| 响应状态、字段和错误码保持精确 | **PASS** | **PASS** | 两者均保留 HTTP 403/404/500、`messageCode` 及各错误码，并检查 500 响应不泄漏 SQL、堆栈或连接串。 |
| 缺少准备或故障入口时诚实标记条件缺口 | **FAIL** | **PASS** | RED 虽写“待提供”，仍把不可用的数据库字段和 Prisma 替身当作准备办法，Case 本身不可由目标执行者操作；GREEN 明确标记“当前不可执行”，指出所缺页面、接口、fixture 或环境级故障控制手段，不虚构入口。 |
| 四个指定代表场景均覆盖且使用 Case 表格、标明当前条件 | **PASS** | **PASS** | 两者均各有 4 条 Case，覆盖 `/open` 跨企业查询、调用企业停用、`/public` 编码解绑和数据读取失败，并含“当前条件”列。 |

### 总结判定

- RED：**FAIL**。覆盖和公开合同信息完整，但测试表面泄漏使前置与故障准备无法由手工／公开 API 功能测试人员执行。
- GREEN：**PASS**。公开 API 合同保持精确，内部实现名未进入执行动作；所有缺失入口均以当前条件缺口呈现。由于模型和隔离元数据未留存，该变化只记为定性观察，不单独证明 Skill 修改造成了改善。
