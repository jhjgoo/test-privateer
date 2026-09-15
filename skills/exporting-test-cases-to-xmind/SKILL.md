---
name: exporting-test-cases-to-xmind
description: 用于已有测试用例需要导出为 XMind 原生脑图，或测试同学要求用脑图评审、交接 Case 时。
---

# 导出测试用例脑图

把已经成稿的测试用例转换成 `.xmind`，用于评审、交接或团队熟悉的脑图阅读方式。用例文件仍是权威来源；脑图不新增、删除或改写 Case。用户尚未提供用例时，先回到 `designing-test-experiments` 完成设计，不先搭建空脑图。

读取用例文件和 `test-privateer/references/artifact-routing.md` 的编号规则。本包标准产物按 Case 表转换，保留 `C-xxx` 编号、关联依据、前置、操作、预期、当前安排和条件；已确认的执行记录和追溯矩阵不放进脑图。若来源采用 `tc-P0/P1/P2` 的 Markdown 标题层级，直接保留其原有层级和优先级，不强行改成本包编号。

在用例文件所在目录生成同名 `.xmind`，用户指定输出路径时除外。执行本包脚本：

```bash
python skills/exporting-test-cases-to-xmind/scripts/md_to_xmind.py <test-cases.md>
```

脚本只使用 Python 标准库，生成 XMind 2020+ 的 ZIP/JSON 结构。导出后核对：源文件中的每条 Case 在脑图中有对应主题；前置、操作和预期没有互换；空白字段标「待确认」；文件是有效 ZIP 且包含 `content.json`。发现用例文件本身缺前置或 oracle，先报告来源缺口；为让脑图可直接交接，可将缺项主题命名为「待确认」，但不得编造规则或结果。

交付时列出源文件、`.xmind` 路径、导出的 Case 数量和未导出的执行记录、附录或复杂详情，说明脑图只是导出视图。
