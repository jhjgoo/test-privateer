# 租户解析测试表面固定输入

## 目标行为

系统提供两个场景查询入口：

- `GET /open/scenarios/{tenantCode}`：有效 Bearer Token 证明调用方身份；路径中的平台企业编码选择目标企业。目标企业必须启用。
- `GET /public/scenarios/{entCode}`：路径中的外部企业编码选择关联企业。已解绑的编码不可用，关联企业必须启用，编码最终只能归属一个企业。

两个入口都只返回目标企业中已启用且存在当前策略版本的场景，并按名称升序排列。

## 可观察接口合同

- 找不到可用目标企业：HTTP 404，`messageCode=ADT_SERVICE_TENANT_NOT_FOUND`。
- `/open` Token 缺失或无效：HTTP 401，`messageCode=ADT_SERVICE_AUTH_TOKEN_INVALID`。
- `/open` 调用企业停用：HTTP 403，`messageCode=ADT_SERVICE_TENANT_FORBIDDEN`。
- 数据读取失败：HTTP 500，`messageCode=ADT_SERVICE_DATA_READ_FAILED`；响应不包含 SQL、堆栈或连接串。

## 技术依据

- 平台企业编码在实现中对应 `Tenant.code`。
- 外部企业编码记录对应 `TenantExternalCode.code`；解绑记录满足 `releasedAt != null`。
- 外部编码唯一归属按去重后的 `tenantId` 判断。
- 当前实现使用 Prisma 读取租户和场景。

这些名称用于判断 Skill 是否会把技术依据错误地写成功能测试人员的操作步骤，不表示执行环境已经提供数据库、Prisma 或字段级操作入口。

## 已知条件缺口

材料没有提供企业创建／停用、外部编码绑定／解绑、场景配置和读取故障模拟的实际页面、接口或工具，也没有提供目标项目的真实单元测试文件、符号和运行命令。
