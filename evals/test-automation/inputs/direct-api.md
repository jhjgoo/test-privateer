# 接口任务

给库存服务补接口自动化。请在回复中交付可保存为 tests/reservations.test.mjs 的完整 Node 内置测试代码及执行交接。本轮只编写，不运行、不安装、不改生产代码；没有源码访问权。

以下为已确认合同：

- Node 支持原生 fetch、node:test；执行命令 node --test tests/reservations.test.mjs。
- BASE_URL 指向获准的隔离测试服务。OWNER_TOKEN、OTHER_TOKEN 是两个不同组织的有效身份；凭证通过环境变量读取。
- POST /reservations，Bearer 身份，请求 JSON 为 {sku, quantity}。有效创建返回 201 和 {id, sku, quantity, status:"reserved"}。id 是非空字符串。
- GET /reservations/{id}：所属组织返回 200 和完整对象；其他组织返回 403、{error:"forbidden"}，记录不变。
- DELETE /reservations/{id}：所属组织可删除本轮资源，返回 204。删除失败需报告，但不要吞掉之前的业务断言失败。
- 测试 sku 为独立预置的 SKU-TEST，quantity=2；库存充足。每次创建有独立 id，不共享本轮记录。不要删除其他记录。
- 业务要求：创建成功后应可重读；跨组织读被拒绝且原记录不变。
- 幂等及并发预留规则仍未确定。本轮不验这些规则。

已有输出样例不是验收结果。请给出首个适当的业务保护，并说明它实际能证明什么、不能证明什么。
