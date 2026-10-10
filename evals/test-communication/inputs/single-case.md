请依据已选测试点 T-041 写一条可交接的公开 API 测试用例，不执行，不扩展到其他测试点。独立材料任务，在对话交付。

规则 DOC-9：有效 Bearer Token 下调用 POST /v1/reservations，readerId 与 bookId 为公开请求字段。readerId 对应的借阅证已失效时返回 HTTP 403，errorCode=CARD_EXPIRED，不生成预约；本次书籍可借库存为 2。测试点 T-041 是失效证读者不能新建预约。

已确认的沙箱准备入口 POST /test-support/readers，请求 {"cardStatus":"expired"}，返回新 readerId；POST /test-support/books，请求 {"availableCopies":2}，返回新 bookId。凭证由沙箱凭证服务提供，当前材料没有真实 Token。GET /test-support/reservations?readerId=<readerId>&bookId=<bookId> 可观察本轮预约记录，预期 items=[]。准备入口仅可用于沙箱。尚未核实沙箱部署版本与凭证是否可用，不得写成已执行。当前没有既有用例编号，沿用 T-041 关联。
