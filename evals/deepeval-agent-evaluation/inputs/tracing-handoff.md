# 为订单 Agent 接入 DeepEval tracing

项目配置已选择 DeepEval，宿主已经安装 Confident AI 官方 `deepeval` 与 `deepeval-tracing` Skills。项目需要建立可复跑的 tracing 评测；不需要原始 OpenTelemetry／OTLP 导出。

请先固定质量主张、确定性订单 Oracle、原始宿主记录位置和上传边界，再选择正确的官方 Skill 承担 tracing 实施。Test Privateer 只负责实施前后的质量检查，不要在本地专项中重写 tracing API 或模板。
