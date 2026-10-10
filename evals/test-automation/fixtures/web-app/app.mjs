import { createServer } from 'node:http';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';

// Intentionally local-only fixture, not an authentication or persistence example.
export function createApp({ dropWrites = false } = {}) {
  const notes = new Map();
  return createServer(async (request, response) => {
    const url = new URL(request.url, 'http://127.0.0.1');
    const send = (status, data) => {
      response.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
      response.end(data === undefined ? undefined : JSON.stringify(data));
    };
    if (request.method === 'GET' && url.pathname === '/') {
      response.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      response.end(page);
      return;
    }
    const user = request.headers['x-test-user'];
    if (!['alice', 'bob'].includes(user)) return send(401, { error: 'unauthorized' });
    if (request.method === 'POST' && url.pathname === '/_test/reset') {
      notes.clear();
      return send(204);
    }
    if (request.method === 'GET' && url.pathname === '/notes') {
      return send(200, [...notes.values()].filter(note => note.owner === user)
        .map(({ id, title }) => ({ id, title })));
    }
    if (request.method === 'GET' && url.pathname.startsWith('/notes/')) {
      const note = notes.get(url.pathname.slice('/notes/'.length));
      if (!note) return send(404, { error: 'not_found' });
      if (note.owner !== user) return send(403, { error: 'forbidden' });
      return send(200, { id: note.id, title: note.title });
    }
    if (request.method === 'POST' && url.pathname === '/notes') {
      try {
        let body = '';
        for await (const chunk of request) {
          body += chunk;
          if (body.length > 8192) return send(413, { error: 'too_large' });
        }
        const { title } = JSON.parse(body);
        if (typeof title !== 'string' || !title.trim()) return send(400, { error: 'invalid_title' });
        const note = { id: randomUUID(), title, owner: user };
        if (!dropWrites) notes.set(note.id, note);
        return send(201, { id: note.id, title });
      } catch {
        return send(400, { error: 'invalid_json' });
      }
    }
    send(404, { error: 'not_found' });
  });
}

const page = `<!doctype html>
<html lang="zh"><meta charset="utf-8"><title>便签测试夹具</title>
<h1>便签</h1>
<form><label>标题<input name="title" required></label><button>保存</button></form>
<p role="status"></p><ul aria-label="已保存便签"></ul>
<script>
const user = new URLSearchParams(location.search).get('user') || 'alice';
const headers = {'x-test-user': user, 'content-type': 'application/json'};
const list = document.querySelector('ul');
const status = document.querySelector('[role=status]');
async function load() {
  const response = await fetch('/notes', {headers});
  if (!response.ok) throw new Error('读取失败');
  const notes = await response.json();
  list.replaceChildren(...notes.map(note => {
    const li = document.createElement('li');
    li.textContent = note.title;
    return li;
  }));
}
document.querySelector('form').addEventListener('submit', async event => {
  event.preventDefault();
  const title = document.querySelector('input').value;
  try {
    const response = await fetch('/notes', {method: 'POST', headers, body: JSON.stringify({title})});
    if (!response.ok) throw new Error('保存失败');
    status.textContent = '保存成功';
    await load();
  } catch (error) { status.textContent = error.message; }
});
load().catch(error => { status.textContent = error.message; });
</script></html>`;

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const server = createApp({ dropWrites: process.env.DROP_WRITES === '1' });
  server.listen(Number(process.env.PORT || 4200), '127.0.0.1', () => {
    console.log('fixture ready http://127.0.0.1:' + server.address().port);
  });
  const stop = () => { server.close(); server.closeAllConnections(); };
  process.on('SIGTERM', stop);
  process.on('SIGINT', stop);
}
