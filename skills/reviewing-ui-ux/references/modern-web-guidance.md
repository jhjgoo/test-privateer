# Modern Web Guidance：现代 Web 依据与候选扫描

Modern Web Guidance（MWG）提供现代 Web 平台用法指南和 `legacy-scan` 静态扫描。它帮助发现旧实现、浏览器兼容性和可访问的现代化机会，但指南命中或扫描发现都不是产品缺陷本身。

## 使用入口

- 指南源：[GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src)
- 已安装 Skill／插件时，优先按宿主能力读取对应指南；未安装时可用 `npx modern-web-guidance@latest`。
- 按意图检索：`npx modern-web-guidance@latest search "responsive table overflow"`
- 读取指南：`npx modern-web-guidance@latest retrieve <guide-id>`
- 扫描候选：`npx modern-web-guidance@latest legacy-scan . --json`

运行工具前沿用当前任务的联网、执行和费用授权；未授权时仍可引用用户提供的指南或扫描报告。

## 在 UI 评审中的证据边界

MWG 指南是现代平台实践依据，不是产品需求、设计批准或 WCAG 等标准的替代。先用任务和适用依据判断问题；需要确认实现方式、兼容性或替代方案时，再检索并引用具体指南。

`legacy-scan` 输出是候选，不是发现清单。每个 finding 必须按指南的验证规则和真实渲染／操作证据复核；源码无命中不能证明体验、无障碍或兼容性没有问题。报告区分：候选、已证实问题、不适用、证据不足和未覆盖。

## 在自动化与现代化审计中的用法

1. 明确用户任务、目标浏览器基线和本次要证明的行为。
2. 用 `search` 找相关指南，读取后确认适用条件、兼容性边界和 fallback。
3. 用 `legacy-scan --json` 获取候选坐标、规则说明和验证规则。
4. 只实现或报告经真实产品证据确认的候选项；产品承诺优先于“更现代”。
5. 修改后复扫受影响范围，并运行对应 UI／E2E 检查。
6. 记录工具版本、检索词、扫描范围、指南 ID、验证结果和未覆盖项。

静态扫描不能作为测试通过证据。浏览器兼容性和无障碍结论仍需按 [无障碍](accessibility.md)、[证据策略](evidence-strategies.md) 或对应测试入口取得适用证据。
