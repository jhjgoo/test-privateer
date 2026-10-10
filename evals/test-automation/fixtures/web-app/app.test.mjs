import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createApp } from './app.mjs';

async function fixture(t, options) {
  const server = createApp(options);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise((resolve, reject) => {
    server.close(error => error ? reject(error) : resolve());
    server.closeAllConnections();
  }));
  const base = 'http://127.0.0.1:' + server.address().port;
  const request = (path, user = 'alice', method = 'GET', data) =>
    fetch(base + path, {
      method, headers: { 'x-test-user': user, 'content-type': 'application/json' },
      ...(data === undefined ? {} : { body: JSON.stringify(data) }),
    });
  return { request, base };
}

test('create then reread preserves the title and owner; reset isolates the next run', async t => {
  const { request } = await fixture(t);
  const created = await request('/notes', 'alice', 'POST', { title: '旅程-正常' });
  assert.equal(created.status, 201);
  const note = await created.json();
  assert.equal(typeof note.id, 'string');
  assert.equal(note.title, '旅程-正常');
  assert.deepEqual(await (await request('/notes/' + note.id)).json(), note);
  assert.deepEqual(await (await request('/notes')).json(), [note]);
  assert.equal((await request('/_test/reset', 'alice', 'POST', {})).status, 204);
  assert.deepEqual(await (await request('/notes')).json(), []);
});

test('another identity is rejected without reading or changing the owner record', async t => {
  const { request } = await fixture(t);
  const response = await request('/notes', 'alice', 'POST', { title: '私有便签' });
  assert.equal(response.status, 201);
  const note = await response.json();
  const denied = await request('/notes/' + note.id, 'bob');
  assert.equal(denied.status, 403);
  assert.deepEqual(await denied.json(), { error: 'forbidden' });
  assert.deepEqual(await (await request('/notes', 'bob')).json(), []);
  assert.deepEqual(await (await request('/notes/' + note.id)).json(), note);
});

test('drop-write fault still acknowledges creation but subsequent reads expose the loss', async t => {
  const { request } = await fixture(t, { dropWrites: true });
  const created = await request('/notes', 'alice', 'POST', { title: '故障便签' });
  assert.equal(created.status, 201);
  const { id } = await created.json();
  assert.equal((await request('/notes/' + id)).status, 404);
  assert.deepEqual(await (await request('/notes')).json(), []);
});

test('only the two fixture identities can use the API; invalid title is rejected', async t => {
  const { request } = await fixture(t);
  assert.equal((await request('/notes', 'unknown')).status, 401);
  assert.equal((await request('/notes', 'alice', 'POST', { title: '' })).status, 400);
  assert.deepEqual(await (await request('/notes')).json(), []);
});
