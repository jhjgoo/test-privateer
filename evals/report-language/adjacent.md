# 固定任务：未执行的接口与单元测试设计

只需要以下两项测试设计，不需要执行报告，也没有执行环境。请直接给出用例和单元测试代码草案。

1. 公开 API：POST /v1/invoices/check，Bearer test-token；请求必须区分 {"taxExempt":false}、{"taxExempt":null}、{}。协议规定 false 返回 HTTP 200 且 body.decision="REJECTED"（规则正常拒绝，不是接口失败）；null 返回 HTTP 422 且 error.code="VALUE_NULL"；缺失返回 HTTP 422 且 error.code="FIELD_MISSING"。目标环境地址未知，不能声明可执行或已通过。
2. TDD：TypeScript 模块 src/invoice.ts 导出 checkTaxExempt(input: {taxExempt?: boolean | null}): "REJECTED" | "APPROVED"。false 返回 REJECTED，true 返回 APPROVED；null 抛 Error("VALUE_NULL")，缺失抛 Error("FIELD_MISSING")。Vitest，测试文件 tests/invoice.test.ts，已确认命令 pnpm vitest run tests/invoice.test.ts。当前实现错误地把 false 和 null 当缺失；要求设计能区分它们的断言。未提供可运行源码，不应声称已经观测到 RED。
