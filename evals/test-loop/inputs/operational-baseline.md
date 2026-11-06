# 使用项目现有测试能力运行完整闭环

这个项目的日常测试依赖根目录 `AGENTS.md`、`.test-privateer/project.md`、已安装的 Test Privateer Skills，以及 `rg`、Python 和项目已有测试命令。

请对当前版本运行完整 Test Loop。盲测子代理需要从质量和测试角度独立判断，不得继承开发聊天、实现理由、diff、开发自测结论或既有 Finding 结果；同时不要因为它使用上述项目规则、Skills 或本地 CLI 就把本轮判成上下文污染。
