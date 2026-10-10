# 自动化方法与接入评测

## 第二阶段：独立编写入口

当前方法入口为 designing-test-automation；明确的接口和旅程任务分别进入 writing-api-tests、writing-e2e-tests。第二阶段输入、判据及评测边界见 [revision-2.md](revision-2.md)。下文 A01—A11、安装过程和示例保留第一阶段来源，不自动视为新入口的行为证据。

本轮新增非便签接口／旅程两组同输入对照，并从新入口生成 API、已有 Playwright、官方 e2e 测试。沿用第一阶段锁定的本地依赖，无重复安装。API 与两种浏览器路径分别验证正常、真实丢写故障及恢复；AI 另做禁操作回放的模型冷运行。

复跑新入口时，读取当前专项及必要参考，让执行者从 fixtures/web-app 的合同生成测试；不要把下方现成代码作为生成结果。版本和环境可沿用下方已核实配置。原始生成代码与执行记录放本地忽略目录，不作为新的发布资产。

## 第一阶段运行方式

输入见 cases.md。每个编号使用新会话，只读取该段输入、被测 designing-test-automation/SKILL.md 及实际路由的参考。A08 同时提供其引用的 A07 项目背景；执行范围仅按 A08 的“只设计”请求判断，与本次实际输入一致。
共同提示：完成该输入请求。仅做只读快照评测，不修改或执行产品；不要读取评测判据、change 或其他版本。输出正常交付及读取文件清单。不自报评分。
固定基线 f4ace9c；基线 A02/A04/A07/A10，候选 A01—A11。同模型、推理配置、权限及提示；候选仅替换 Skill 根路径。
记录宿主、模型配置、输入与加载文件 SHA256、调用轨迹、完整输出及完成状态。原始记录放 .local/validation/test-automation/，不提交。
通过表示无实质偏离；失败说明原话和影响；环境受阻不计内容通过。两版均通过只说明本样本保持，不宣称提升。
评分不靠关键词。只读快照不能证明实际安装、跨阶段触发或运行有效。

## 判据与契约映射

| 输入 | 判据 | delta 场景 |
| --- | --- | --- |
| A01 | 符号、阈值、异常与独立预期准确；不编 RED | A narrow rule |
| A02 | 响应与重读、对象权限及拒绝副作用；未知幂等保留；无浏览器强制 | An API test; lacks an idempotency rule; valid response; authenticated actor; API-only |
| A03 | 保留真实 DB 缺口及高层接线；按互补证据选组合 | Several levels; database behavior |
| A04 | 消费者不等于提供者，契约不等于业务完成 | Only the consumer side |
| A05 | 组件模拟边界准确，不强迫全链路 | UI behavior |
| A06 | 沿用现有框架、目录、命令；源码不足不编完成 | Existing API or browser |
| A07 | 能按官方版本资料推进接入，不仅以本包能力为由拒绝；如实保留只读限制 | A suitable project; Deterministic tests |
| A08 | 只设计，无安装或执行动作 | design only |
| A09 | 版本核对、阻塞与下一动作；不全局升级，不编兼容事实 | incompatible environment |
| A10 | 本轮身份、跳过、首次失败、重试和历史来源明确 | fails before report; retry passes |
| A11 | 可靠模型可用性质/序列测试；未知业务不造性质 | known invariant |

其余场景在真实试跑验证：重新读取保存状态、共享后端隔离、判错能力。来源可达和按需链接由静态契约检查；人工评阅方法选择和真实报告的可读性。
既有回归：test-surface-language 功能/单元/混合；test-communication 的 task-plan。

## 真实试跑

先运行 fixtures/web-app/app.test.mjs，证明受控夹具正常、拒绝、重置和丢写模式正确。独立副本执行：
1. 无框架：通过候选入口取得官方 Skill，建立确定性用例，正常与新输出目录复跑。
2. 同一用例：成功但丢写时因业务断言失败，恢复后通过。
3. AI：获准模型执行目标操作＋精确断言，禁用回放缓存；缺凭证保留受阻。
4. 已有 Playwright：保留既有用例，追加业务保护，不安装 e2e。
5. 纯接口：Node 内置工具生成并运行，响应/重读/权限副作用，不安装浏览器。

每项记录版本、实际命令、输出位置与清理方式。实测后在此补可复跑步骤；原始日志不进入 README。有限夹具不证明跨项目或跨宿主稳定。

## 复跑步骤（2026-10-10 实测）

本节保留可复用配置与用例，不保存原始报告。实测为 macOS arm64、Node 26.10.0、npm 11.19.1、Chrome 154.0.8037.99。
e2e 0.18.0 配 @e2e-dev/web 0.13.0；已有框架路径使用 Playwright 1.64.0。
这些是复跑版本，不是长期最低版本或跨平台支持承诺。

### 准备独立副本

在仓库根目录运行夹具自检：

```sh
node --test evals/test-automation/fixtures/web-app/app.test.mjs
```

分别新建无框架、已有框架、纯接口三个临时目录，把 fixtures/web-app/app.mjs 复制到各目录。以下命令在对应副本内执行。
只在空目录初始化；已有用户项目应先检查配置影响。不要把本节的演示初始化当成覆盖现有项目的指令。

### 无框架 Web：确定性业务用例

在空副本建立 private=true、type=module 的 package.json，再安装：

```sh
npm install --save-dev --save-exact e2e@0.18.0 @e2e-dev/web@0.13.0
E2E_TELEMETRY_DISABLED=1 npx --no-install e2e init --yes
```

初始化会取得项目内官方 .agents/skills/e2e 及宿主配置。实施前完整读取其 SKILL.md 与 setup、writing-tests、running 参考；AI 路径再读 agent。检查生成文件，不覆盖已有自定义设置。锁定依赖后保留 lockfile。

本轮默认浏览器缺失，下载较慢；并发安装又遇到缓存锁。未删除共享锁。改用已安装 Chrome 的独立临时实例，验证的是此连接方式，不是默认下载路径。

macOS 可在单独终端启动本次拥有的浏览器（路径按实际安装核对）：

```sh
TEST_CHROME_PROFILE=$(mktemp -d /tmp/automation-skill-chrome.XXXXXX)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --remote-debugging-address=127.0.0.1 --remote-debugging-port=0 \
  --user-data-dir="$TEST_CHROME_PROFILE" --no-first-run --no-default-browser-check about:blank
```

从启动输出读取本次端口。测试终端将 TEST_CDP_ENDPOINT 设为 http://127.0.0.1:该端口，不连接用户日常浏览器。
保存以下 e2e.config.ts：

```ts
import type { E2EConfig } from 'e2e';
import { web } from '@e2e-dev/web';

export default {
  targets: [{
    engine: web({
      connect: { cdpEndpoint: async () => process.env.TEST_CDP_ENDPOINT! },
    }),
    app: {
      url: 'http://127.0.0.1:0',
      command: {
        executable: 'node',
        args: ['app.mjs'],
        env: { PORT: '{port}', DROP_WRITES: process.env.DROP_WRITES ?? '0' },
        log: '.e2e/logs/app.log',
      },
    },
  }],
  workers: 1,
  retries: 0,
  assertionTimeout: 3000,
  cache: 'off',
} satisfies E2EConfig;
```

保存 tests/notes.e2e.ts：

```ts
import { randomUUID } from 'node:crypto';
import { test } from '@e2e-dev/web';
import { expect } from 'e2e';

test('新增便签后重开页面仍可读取', async ({ app, screen }) => {
  const title = '便签-' + randomUUID();
  await app.open('/?user=alice');
  await screen.getByLabel('标题').fill(title);
  await screen.getByRole('button', '保存').click();
  await expect(screen.getByRole('status')).toHaveText('保存成功');
  await app.restart();
  await expect(screen.getByRole('list', '已保存便签').getByRole('listitem')).toContainText([title]);
});
```

依次运行，后续复跑换用新的输出目录：

```sh
E2E_TELEMETRY_DISABLED=1 npx --no-install e2e run tests/notes.e2e.ts --output .e2e/normal-1 --reporter list,markdown
E2E_TELEMETRY_DISABLED=1 npx --no-install e2e run tests/notes.e2e.ts --output .e2e/normal-2 --reporter list,markdown
DROP_WRITES=1 E2E_TELEMETRY_DISABLED=1 npx --no-install e2e run tests/notes.e2e.ts --output .e2e/fault-1 --reporter list,markdown
E2E_TELEMETRY_DISABLED=1 npx --no-install e2e run tests/notes.e2e.ts --output .e2e/recovered-1 --reporter list,markdown
```

正常两轮和恢复轮各 1 条通过。故障轮应在重新打开后的列表断言失败：预期本轮标题，实际为空。
不能以启动失败代替该反证。每次服务使用独立进程和随机端口，标题使用 UUID。
测试结束由框架停止服务；全部结束后，在浏览器终端停止本次 Chrome。只清理该临时实例的数据。

### 同一项目：AI 冷运行

在上述副本增加依赖：

```sh
npm install --save-dev --save-exact ai@7.0.137 @ai-sdk/openai-compatible@3.0.67
```

通过获准配置提供 OPENAI_BASE_URL 和 OPENAI_API_KEY，不将凭证写入任何文件。
本轮使用兼容服务中可用的 codex/gpt-6.1-sol；换环境先核对模型可用性。
保存 e2e.ai.config.ts：

```ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import type { E2EConfig } from 'e2e';
import base from './e2e.config';

const provider = createOpenAICompatible({
  baseURL: process.env.OPENAI_BASE_URL!,
  apiKey: process.env.OPENAI_API_KEY,
  name: 'approved-local',
});

export default {
  ...base,
  timeout: 120_000,
  agents: {
    default: {
      model: provider.chatModel('codex/gpt-6.1-sol'),
      maxSteps: 6,
      maxModelCalls: 6,
    },
  },
} satisfies E2EConfig;
```

保存 tests/notes-ai.e2e.ts：

```ts
import { randomUUID } from 'node:crypto';
import { test } from '@e2e-dev/web';
import { expect } from 'e2e';

test('AI 新增便签后重开仍可读取', async ({ app, screen, agent }) => {
  const title = 'AI便签-' + randomUUID();
  await app.open('/?user=alice');
  const result = await agent.act('新增一条标题为 {title} 的便签', {
    params: { title },
  });
  await expect(screen.getByRole('status')).toHaveText('保存成功');
  await app.restart();
  await expect(screen.getByRole('list', '已保存便签').getByRole('listitem')).toContainText([title]);
  expect(result.modelCalls).toBeGreaterThan(0);
});
```

```sh
E2E_TELEMETRY_DISABLED=1 npx --no-install e2e run tests/notes-ai.e2e.ts --config e2e.ai.config.ts --no-cache --output .e2e/ai-cold-1 --reporter list,markdown
```

本轮 1 条通过，实际模型调用 3 次。模型 token 缓存与操作回放是两回事。
按所用版本核对 report.json 中 run.id、exitCode、summary、选中用例 attempts 和 agent 步骤；不只读 CLI 退出码。
本轮各选中 1 条并执行，重试后通过与选中后跳过均为 0；初始化示例等未选中项不计入通过数。

### 已有 Playwright：先建立基线，再只追加测试

在另一空副本建立 private=true、type=module 的 package.json 和 scripts.test:ui="playwright test"。
安装 @playwright/test@1.64.0，不安装 e2e。保存 playwright.config.ts：

```ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/ui',
  workers: 1,
  retries: 0,
  use: { baseURL: 'http://127.0.0.1:43127', channel: 'chrome' },
  webServer: {
    command: 'node app.mjs',
    env: { PORT: '43127' },
    url: 'http://127.0.0.1:43127',
    reuseExistingServer: false,
  },
});
```

先保存 tests/ui/existing.spec.ts，运行 npm run test:ui -- --reporter=line，确认基线 1 条通过：

```ts
import { test, expect } from '@playwright/test';
test('已有回归：显示便签入口', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: '便签' })).toBeVisible();
});
```

再只新增 tests/ui/notes.spec.ts：

```ts
import { randomUUID } from 'node:crypto';
import { test, expect } from '@playwright/test';

test('新增便签刷新后仍可读取', async ({ page }) => {
  const title = 'PW便签-' + randomUUID();
  await page.goto('/?user=alice');
  await page.getByLabel('标题').fill(title);
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await expect(page.getByRole('status')).toHaveText('保存成功');
  await page.reload();
  await expect(page.getByRole('list', { name: '已保存便签' }).getByRole('listitem')).toHaveText([title]);
});
```

再运行相同命令，预期 2 条通过。核对配置、原测试与 package.json 的前后哈希一致，依赖未加入 e2e。
本轮先在环境准备阶段选定已安装 Chrome，追加业务用例期间没有改配置。端口占用时先选择新的本次端口，不复用未知服务。

### 纯接口：无 npm 依赖

在第三份副本保存 notes.test.mjs：

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { createApp } from './app.mjs';

test('创建可重读，另一身份拒绝读取且不改变原数据', async t => {
  const server = createApp({ dropWrites: process.env.DROP_WRITES === '1' });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => {
    server.close(resolve);
    server.closeAllConnections();
  }));
  const base = 'http://127.0.0.1:' + server.address().port;
  const title = '接口-' + randomUUID();
  const ownerHeaders = { 'x-test-user': 'alice', 'content-type': 'application/json' };
  const created = await fetch(base + '/notes', {
    method: 'POST', headers: ownerHeaders, body: JSON.stringify({ title }),
  });
  assert.equal(created.status, 201);
  const note = await created.json();
  assert.equal(typeof note.id, 'string');
  assert.equal(note.title, title);
  const read = await fetch(base + '/notes/' + note.id, { headers: ownerHeaders });
  assert.equal(read.status, 200, '刚创建的便签应可重读');
  assert.deepEqual(await read.json(), note);
  const denied = await fetch(base + '/notes/' + note.id, {
    headers: { 'x-test-user': 'bob' },
  });
  assert.equal(denied.status, 403);
  assert.deepEqual(await denied.json(), { error: 'forbidden' });
  const after = await fetch(base + '/notes/' + note.id, { headers: ownerHeaders });
  assert.equal(after.status, 200);
  assert.deepEqual(await after.json(), note);
});
```

```sh
node --test notes.test.mjs
DROP_WRITES=1 node --test notes.test.mjs
node --test notes.test.mjs
```

预期正常与恢复各 1 条通过；故障因重读 404 不等于预期 200 而失败。
使用真实本地 HTTP 与夹具内存存储，非生产数据库。没有安装浏览器框架。
服务由测试自行关闭，三轮使用独立实例，不依赖残留记录。

## 第一阶段证据限制

本次快照各运行一次，不计算稳定率。A01/A02/A04 使用方法阶段版本，其余使用完整实施入口；文件哈希留在本地原答复。
四组 A/B 中 A02/A04/A10 为保持，A07 消除了旧入口只提供设计的限制；真正接入由上述夹具试跑另证。
功能、单元与交接表达回归未见实质偏离；混合请求因意外读到评分规则，作为已知判据回归，不主张盲评。
官方副本、依赖、生成项目和全部原始输出仅放忽略目录。有限本地试跑不证明跨项目、跨宿主或每次均成功。
