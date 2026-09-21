# 混合请求 Skill 行为 RED/GREEN 对照

- Run ID：`test-surface-language-mixed-20260921-1050-gpt56sol`
- 日期：2026-09-21（Asia/Shanghai）
- 运行方式：Codex CLI 0.147.0，两个独立 `--ephemeral` 新上下文，只读沙箱，`gpt-5.6-sol`，reasoning effort `medium`
- 模型限制：先尝试 `gpt-6-astra`，CLI 明确返回“requires a newer version of Codex”，未产生模型输出；因此本次有效 RED/GREEN 均改用同一个可用模型 `gpt-5.6-sol`。这不是 README 所述 Astra 方向的服务端型号核验。
- Baseline 来源：Git `HEAD`，commit `b99564dadfbf7b55d218e54aecb1d12323e042d7`
  - `git show HEAD:skills/test-privateer/SKILL.md`，sha256 `2061ce47279788736ad6694b9e91dabb7bce48d59856223e018ca934d303d2fc`
  - `git show HEAD:skills/designing-test-experiments/SKILL.md`，sha256 `0c0b6dc5e938103efe5f784260ef0f9374362366a96f85a7331a61769607d187`
  - `git show HEAD:skills/writing-unit-tests/SKILL.md`，sha256 `8d9572f900597ada66649a65deba9d794c7e39b1144962ea4964e97be6377b2a`
- Candidate 来源：工作区当前文件
  - `skills/test-privateer/SKILL.md`，sha256 `e80a8a465b3ea3134a2e893961db500a12de2bd619cb23838171ca02603737e0`
  - `skills/designing-test-experiments/SKILL.md`，sha256 `de82b3b1822b71f8203ff438e18b07e746501a887021c19953f488f06f5c55fa`
  - `skills/writing-unit-tests/SKILL.md`，sha256 `292ab42c543efef7b88b83533b8721020ad3901c2996bd5c05ed813dc16f384b`
- 固定输入：`evals/test-surface-language/input.md`
- 固定输入 sha256：`cfeb26a4f4af6c92d8d847d608bd161621c5fd5caa7324ca50f6596f7dd296e7`
- 隔离说明：两次运行均被要求不读取 `evals/test-surface-language/README.md` 或既有运行记录；除 Skill 来源不同外，probe、模型、reasoning effort、工作目录和只读约束相同。

## 精确 probe

> 基于固定输入，同时交付 1 条公开 API 功能 Case 和 1 个 TDD 单元测试切片。分别说明术语保留边界和执行/RED 状态。

## RED 原始输出

### 公开 API 功能 Case：已解绑外部企业编码不可查询场景

| ID | 关联依据 | 要检查什么 | 场景／前置条件 | 怎么操作 | 预期结果 | 最小证据 | 当前条件 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-PUBLIC-001 | 已解绑编码不可用；找不到可用目标企业时返回规定错误 | 已解绑编码不会继续访问原关联企业 | 准备企业 A；外部企业编码 `EXT-001` 曾关联企业 A，现已解绑；企业 A 处于启用状态且有可返回场景 | 请求 `GET /public/scenarios/EXT-001` | HTTP 404；`messageCode=ADT_SERVICE_TENANT_NOT_FOUND`；响应不包含企业 A 的场景 | 请求、响应状态码及响应体 | **待核实／待补环境**：缺少绑定、解绑和场景配置入口，也未指定目标版本与环境 |

- 术语保留边界：面向功能测试只使用“外部企业编码、关联企业、解绑、启用”等可观察业务术语；不把 `TenantExternalCode.code`、`releasedAt != null` 或 Prisma 操作写成测试步骤。
- 执行状态：仅完成 Case 设计，未执行，不能判定通过或失败。

### TDD 单元测试切片：同一企业的重复关联记录不构成多企业归属

- 来源规则：外部编码唯一归属应按去重后的 `tenantId` 判断。
- 分支：目标行为的 TDD 切片；由于缺少真实代码、测试框架、符号和命令，只交付待实现切片。
- seam：外部编码解析组件对调用者公开的“按外部编码解析企业”方法；实际方法名以项目代码为准。
- Given：外部编码 `EXT-001` 存在两条未解绑关联记录，两条记录的 `tenantId` 均为企业 A；企业 A 已启用。
- When：调用解析方法解析 `EXT-001`。
- Then：返回企业 A，不因存在两条记录而判定编码归属不唯一。
- oracle：固定输入明确规定“唯一归属按去重后的 `tenantId` 判断”。
- 最小区分力：错误实现若按记录条数判断，会拒绝该输入；正确实现按 `tenantId` 去重后只得到企业 A。

伪代码：

```text
test "同一 tenantId 的重复有效关联 → 解析为唯一企业" {
  given active links:
    { code: "EXT-001", tenantId: "tenant-a", releasedAt: null }
    { code: "EXT-001", tenantId: "tenant-a", releasedAt: null }
  and tenant-a is enabled

  result = resolveTenantByExternalCode("EXT-001")

  expect(result.tenantId).toEqual("tenant-a")
}
```

- 术语保留边界：`tenantId`、`releasedAt` 仅保留在单元测试数据和规则 oracle 中，用于区分去重与解绑逻辑；Prisma 查询结构、私有函数和内部调用次数不作为断言。
- RED 状态：**未编写、未运行、尚未形成有效 RED**。真实测试文件、符号、fixture 和运行命令缺失；只有目标测试实际以断言差异失败，并明确指向“未按 `tenantId` 去重”时，才能认定为有效 RED。

## GREEN 原始输出

## 公开 API 功能 Case

| ID | 要检查什么 | 场景／前置条件 | 怎么操作 | 预期结果 | 需要保留什么 | 当前条件 |
| --- | --- | --- | --- | --- | --- | --- |
| C-PUBLIC-001 | 已解绑的外部企业编码不能用于查询场景 | 准备一个曾关联企业、现已解绑的外部企业编码；原关联企业保持启用 | 发送 `GET /public/scenarios/{entCode}`，将 `{entCode}` 替换为该外部企业编码 | HTTP `404`；响应中 `messageCode=ADT_SERVICE_TENANT_NOT_FOUND`；不得返回原关联企业的场景 | 请求路径、响应状态码、响应体 | **待补环境，未执行**：缺少绑定／解绑数据准备入口及目标环境 |

术语保留边界：Case 保留公开契约中的路径、`entCode`、HTTP 状态码和 `messageCode`。操作步骤只使用“外部企业编码、关联企业、已解绑”等可准备和观察的业务术语；`TenantExternalCode.code`、`releasedAt`、`tenantId` 和 Prisma 属于实现层，不写成 API 测试人员的操作步骤。

## TDD 单元测试切片

**目标行为：** 同一个外部编码存在多条未解绑记录，但去重后的 `tenantId` 只有一个时，应解析为唯一企业，不能把重复记录误判为多企业归属。

```ts
it("同一外部编码的未解绑记录指向相同 tenantId 时解析为唯一企业", async () => {
  // Arrange
  const externalCodeRecords = [
    { code: "EXT-001", tenantId: "tenant-1", releasedAt: null },
    { code: "EXT-001", tenantId: "tenant-1", releasedAt: null },
  ];
  const enabledTenant = { id: "tenant-1", enabled: true };

  // Act
  const result = await subject.resolveEnabledTenant(
    "EXT-001",
    externalCodeRecords,
    enabledTenant,
  );

  // Assert
  expect(result.id).toBe("tenant-1");
});
```

- seam：外部编码解析为启用企业的最窄业务服务边界；`subject.resolveEnabledTenant` 是待映射占位符，不冒充项目真实符号。
- oracle：固定输入明确规定“外部编码唯一归属按去重后的 `tenantId` 判断”。
- 术语保留边界：单元层 fixture 保留 `TenantExternalCode` 对应的 `code`、`tenantId`、`releasedAt`，因为它们直接表达该规则；Prisma 查询形状和内部调用次数不属于行为 oracle，不锁入测试。
- **RED 状态：未建立、未运行。** 当前没有真实测试文件、被测符号、框架或运行命令，因此这只是可实现的 RED 切片，不能声称已失败或通过。有效 RED 必须表现为断言未得到 `tenant-1`，且失败原因确实是实现按记录条数而非去重后的 `tenantId` 判断。

## 按 README 标准逐项评分

| 场景 | RED | GREEN | 依据 |
| --- | --- | --- | --- |
| 功能／公开 API Case | PASS | PASS | 两侧执行正文均使用可准备、可观察的业务状态，保留公开路径、路径参数、HTTP 404 和 `messageCode`；都没有把 `TenantExternalCode.code`、`releasedAt`、`tenantId` 或 Prisma 写成 API 执行步骤，并诚实标出绑定／解绑入口缺失和未执行状态。GREEN 对公开契约与实现层边界的表述更直接。 |
| TDD 单元测试 | PASS（输入边界内） | PASS（输入边界内） | 两侧都在单元层保留 `tenantId`、`releasedAt`、fixture 数据、seam 与 oracle，并排除 Prisma 查询形状、私有实现和调用次数。固定输入明确没有真实测试文件、符号、框架和命令；RED 使用伪代码并说明实际方法名未知，GREEN 将 `subject.resolveEnabledTenant` 明示为占位符。两侧均未伪造真实命令或有效 RED，并准确说明取得有效 RED 所需的失败原因。 |
| 混合请求 | PARTIAL | PARTIAL | 两侧都分别交付了功能 Case 和单元测试切片，且两项都有结果与诚实状态，没有出现只完成首个专项产物便停止的行为。但两侧原始输出都没有显式说明“TDD 是 RED→GREEN→REFACTOR 的反馈节奏，而不是测试层级”，因此未完全达到 README 的全部通过条件。 |

## 结论

本次单次隔离 probe 中，GREEN 没有形成可计分的整体跃升：RED 与 GREEN 都通过了公开 API Case 和输入边界内的单元测试信息保护，并都完整交付了混合请求的两个产物。GREEN 更清楚地区分了公开 API 契约、实现层名称和单元层 fixture，但这属于表述增强；两侧都因未显式解释 TDD 的反馈节奏而在混合请求项记为 PARTIAL。该结果只代表这一轮生成，不推翻 README 中其他代表运行的既有结论。

## 评分标准修订后的重评

上述原始评分要求每份混合产物都显式解释“TDD 是反馈节奏”，把内部路由判断变成了用户可见措辞要求。README 已于本轮终审中收紧为行为标准：功能 Case 与单元测试分别交付，TDD 不被当作第三个测试层级，两项均有结果或诚实状态。按该标准，RED 与 GREEN 的混合请求均为 **PASS**；本次运行证明 candidate 满足完成规则且没有退化，但没有证明相对 baseline 提升。
