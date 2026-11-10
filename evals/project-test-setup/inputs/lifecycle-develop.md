# 调整商品检查

把商品检查脚本从 scripts/check_catalog.py 迁到 tools/check_catalog.py，项目测试入口改用新位置。沿用 unittest，补充未知商品编码必须抛出 KeyError 的检查，并实际运行。产品行为不变。结果记入现有 catalog-check change，完成后交付，暂不归档、不提交。
