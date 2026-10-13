import assert from 'node:assert/strict';
import { createHmac, createHash } from 'node:crypto';
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import test from 'node:test';
import { buildDraftPlan, Client, contained, credentials, createDraft, discover, hash, initSite, parseEnv, planDraft, redact, selectSite, sign, sourceHash, validateShortcode } from '../client.mjs';

const SITE_ID = '3387d0b6-839a-4db3-98b9-accf7948d4aa';
const SECRET = 'a'.repeat(64);
const response = (value, status = 200) => new Response(JSON.stringify(value), { status, headers: { 'Content-Type': 'application/json' } });

test('Git source checks accept CRLF/LF equivalence but reject actual content changes', () => {
  assert.equal(sourceHash(Buffer.from('<main>\r\nCafé\r\n</main>\r\n')), sourceHash(Buffer.from('<main>\nCafé\n</main>\n')));
  assert.notEqual(sourceHash(Buffer.from('<main>\r\nCafé\r\n</main>\r\n')), sourceHash(Buffer.from('<main>\nChanged\n</main>\n')));
  assert.notEqual(hash('<main>\r\n'), hash('<main>\n'));
});

function fixture() {
  const root = mkdtempSync(resolve(tmpdir(), 'broseph-tests-'));
  initSite({ site: 'alpha', url: 'https://alpha.example', siteId: SITE_ID }, root);
  initSite({ site: 'beta', url: 'https://beta.example', siteId: '11111111-2222-3333-4444-555555555555' }, root);
  writeFileSync(resolve(root, 'alpha/.env.broseph'), `BROSEPH_SHARED_SECRET=${SECRET}\n`);
  writeFileSync(resolve(root, 'alpha/page.html'), '<main><h1>A & B</h1></main>');
  return { root, config: selectSite('alpha', root), clean: () => {
    assert.ok(contained(resolve(tmpdir()), root) && root !== resolve(tmpdir()), 'Cleanup must stay inside its unique temporary fixture directory.');
    rmSync(root, { recursive: true, force: true });
  } };
}

function transportFor(config, tools, calls, handler = () => response({ ok: true })) {
  return async (url, options) => {
    calls.push({ url: String(url), ...options });
    const pathname = new URL(url).pathname;
    if (pathname.endsWith('/status')) return response({ site_url: config.site_url, site_id: config.site_id, auth_status: 'accepted', plugin_version: '0.1.1' });
    if (pathname.endsWith('/tools')) return response({ namespace: 'broseph/v1', tools });
    return handler(url, options);
  };
}

test('signature matches the PHP canonical payload using raw UTF-8 body and literal secret', () => {
  const body = '{"title":"Café & care"}';
  const parameters = { method: 'POST', route: '/broseph/v1/gitpress/pages/create', body, siteId: SITE_ID, secret: SECRET, timestamp: '1791830000', nonce: '0123456789abcdef0123456789abcdef' };
  const bodyHash = createHash('sha256').update(Buffer.from(body, 'utf8')).digest('hex');
  const expected = createHmac('sha256', SECRET).update(['POST', parameters.route, parameters.timestamp, parameters.nonce, bodyHash].join('\n')).digest('hex');
  assert.equal(sign(parameters)['X-Broseph-Signature'], expected);
  assert.throws(() => sign({ ...parameters, route: '/wp-json/broseph/v1/status' }));
  assert.throws(() => sign({ ...parameters, route: '/broseph/v1/pages?page=2' }));
  assert.notEqual(sign({ ...parameters, nonce: undefined })['X-Broseph-Nonce'], sign({ ...parameters, nonce: undefined })['X-Broseph-Nonce']);
});

test('env parsing handles BOM/quotes/comments but does not evaluate shell expressions', () => {
  assert.deepEqual(parseEnv('\uFEFFBROSEPH_SHARED_SECRET="abc" # note\r\nIGNORED=$(unsafe)\r\n'), { BROSEPH_SHARED_SECRET: 'abc', IGNORED: '$(unsafe)' });
  assert.throws(() => parseEnv('KEY=a\nKEY=b'), /Duplicate/);
  assert.throws(() => parseEnv('not env syntax'), /Invalid/);
});

test('credentials stay per-site, missing secrets fail, and init never overwrites a connection', () => {
  const f = fixture();
  try {
    assert.equal(discover(f.root).length, 2);
    assert.equal(credentials(f.config).secret, SECRET);
    assert.throws(() => credentials(selectSite('beta', f.root)), /missing or incomplete/);
    assert.throws(() => initSite({ site: 'alpha', url: 'https://other.example' }, f.root), /already exists/);
    assert.throws(() => selectSite('', f.root), /explicitly/);
    writeFileSync(resolve(f.root, 'alpha/.env.broseph'), `BROSEPH_SHARED_SECRET=${SECRET}\nBROSEPH_SITE_URL=https://beta.example`);
    assert.throws(() => credentials(f.config), /does not match/);
  } finally { f.clean(); }
});

test('GET query values are encoded outside the signed route, with empty body and no redirects', async () => {
  const f = fixture(), calls = [];
  try {
    const client = new Client(f.config, credentials(f.config), async (url, options) => { calls.push({ url, options }); return response({ ok: true }); });
    await client.request('GET', '/broseph/v1/pages', { search: 'A & B', page: 2 });
    const { url, options } = calls[0];
    assert.equal(url.searchParams.get('search'), 'A & B');
    assert.equal(options.body, undefined);
    assert.equal(options.redirect, 'manual');
    const signature = sign({ method: 'GET', route: '/broseph/v1/pages', siteId: SITE_ID, secret: SECRET, timestamp: options.headers['X-Broseph-Timestamp'], nonce: options.headers['X-Broseph-Nonce'] });
    assert.equal(options.headers['X-Broseph-Signature'], signature['X-Broseph-Signature']);
  } finally { f.clean(); }
});

test('POST signs exactly the JSON bytes it sends', async () => {
  const f = fixture();
  try {
    const client = new Client(f.config, credentials(f.config), async (_, options) => {
      const signature = sign({ method: 'POST', route: '/broseph/v1/scan', body: options.body, siteId: SITE_ID, secret: SECRET, timestamp: options.headers['X-Broseph-Timestamp'], nonce: options.headers['X-Broseph-Nonce'] });
      assert.equal(options.headers['X-Broseph-Signature'], signature['X-Broseph-Signature']);
      assert.deepEqual(JSON.parse(options.body), { title: 'Café & care' });
      return response({ ok: true });
    });
    await client.request('POST', '/broseph/v1/scan', { title: 'Café & care' });
  } finally { f.clean(); }
});

test('redirects, identity mismatch and transport failure stop without retry', async () => {
  const f = fixture();
  try {
    let attempts = 0;
    const redirected = new Client(f.config, credentials(f.config), async () => { attempts++; return new Response(null, { status: 302 }); });
    await assert.rejects(redirected.status(), /redirect blocked/);
    assert.equal(attempts, 1);
    const mismatch = new Client(f.config, credentials(f.config), async () => response({ site_url: 'https://beta.example', site_id: SITE_ID, auth_status: 'accepted' }));
    await assert.rejects(mismatch.tools(), /identity/);
    const failure = new Client(f.config, credentials(f.config), async () => { throw new Error(SECRET); });
    await assert.rejects(failure.status(), error => !error.message.includes(SECRET) && /No automatic retry/.test(error.message));
  } finally { f.clean(); }
});

test('tools are refreshed; unavailable tools and unrequested writes never reach their endpoint', async () => {
  const f = fixture(), calls = [];
  try {
    const tools = [
      { name: 'publish_page', method: 'POST', endpoint: '/broseph/v1/pages/{id}/publish', risk_level: 'publish_mutation', available: true },
      { name: 'update_seo_meta', method: 'POST', endpoint: '/broseph/v1/seo/page/{id}', risk_level: 'metadata_mutation', available: false },
    ];
    const client = new Client(f.config, credentials(f.config), transportFor(f.config, tools, calls));
    await assert.rejects(client.call('publish_page', { id: 1 }), /--write/);
    await assert.rejects(client.call('update_seo_meta', { id: 1 }, { write: true }), /unavailable/);
    await assert.rejects(client.call('invented_route', {}), /does not advertise/);
    assert.ok(calls.every(c => /\/(status|tools)$/.test(c.url)));
    await client.call('publish_page', { id: 7, expected_current_status: 'draft' }, { write: true });
    assert.ok(calls.at(-1).url.endsWith('/pages/7/publish'));
    assert.deepEqual(JSON.parse(calls.at(-1).body), { expected_current_status: 'draft' });
  } finally { f.clean(); }
});

test('known secrets and sensitive fields are redacted from responses/errors', async () => {
  assert.deepEqual(redact({ shared_secret: SECRET, nested: { token: 'other', value: `prefix${SECRET}` } }, SECRET), { shared_secret: '[redacted]', nested: { token: '[redacted]', value: 'prefix[redacted]' } });
  const f = fixture();
  try {
    const client = new Client(f.config, credentials(f.config), async () => response({ code: 'oops', message: SECRET }, 401));
    await assert.rejects(client.status(), error => !error.message.includes(SECRET) && error.message.includes('[redacted]'));
  } finally { f.clean(); }
});

test('draft plans scope sources and shortcodes to the selected client; no secret is in a plan', () => {
  const f = fixture();
  try {
    const result = planDraft(f.config, { source: 'alpha/page.html', title: 'A & B', slug: 'a-b' });
    assert.equal(result.plan.source_sha256, hash(readFileSync(resolve(f.root, 'alpha/page.html'))));
    assert.ok(!JSON.stringify(result).includes(SECRET));
    assert.throws(() => buildDraftPlan(f.config, { source: 'beta/page.html', title: 'B', slug: 'b' }), /inside/);
    validateShortcode(f.config, result.plan.payload.shortcode);
    assert.throws(() => validateShortcode(f.config, result.plan.payload.shortcode.replace('alpha/page.html', 'beta/page.html')), /selected client/);
  } finally { f.clean(); }
});

test('draft refuses unpushed/changed source without creating a page or altering the reviewed plan', async () => {
  const f = fixture();
  try {
    const result = planDraft(f.config, { source: 'alpha/page.html', title: 'Page', slug: 'page' });
    let mutations = 0;
    const client = { config: f.config, call: async () => { mutations++; } };
    await assert.rejects(createDraft(client, result.plan, { write: true, transport: async () => response({}, 404) }), /GitHub source/);
    assert.equal(mutations, 0);
    const reviewed = readFileSync(result.path, 'utf8');
    writeFileSync(resolve(f.root, 'alpha/page.html'), '<main>Changed</main>');
    await assert.rejects(createDraft(client, result.plan, { write: true }), /changed/);
    assert.equal(readFileSync(result.path, 'utf8'), reviewed);
  } finally { f.clean(); }
});

test('draft duplicate-slug check paginates all pages rather than relying on text search', async () => {
  const f = fixture();
  try {
    const { plan } = planDraft(f.config, { source: 'alpha/page.html', title: 'Page', slug: 'page' });
    const inputs = [];
    const client = { config: f.config, call: async (name, input) => {
      assert.equal(name, 'list_pages');
      inputs.push(input);
      return input.page === 1 ? { pages: [{ slug: 'other' }], total_pages: 2 } : { pages: [{ slug: 'page' }], total_pages: 2 };
    } };
    await assert.rejects(createDraft(client, plan, { write: true, transport: async () => new Response(readFileSync(resolve(f.root, 'alpha/page.html'))) }), /already exists/);
    assert.equal(inputs.length, 2);
    assert.equal(inputs[0].search, undefined);
  } finally { f.clean(); }
});

test('created draft ID survives SEO failure and is returned without automatic publishing', async () => {
  const f = fixture();
  try {
    const { plan } = planDraft(f.config, { source: 'alpha/page.html', title: 'Page', slug: 'page' });
    const calls = [];
    const client = { config: f.config, tools: async () => { throw new Error('SEO permission refresh failed'); }, call: async (name) => {
      calls.push(name);
      if (name === 'list_pages') return { pages: [], total_pages: 0 };
      if (name === 'create_gitpress_page') return { page_id: 73, preview_url: 'https://alpha.example/?page_id=73&preview=true' };
      throw new Error('unexpected tool');
    } };
    const result = await createDraft(client, plan, { write: true, transport: async () => new Response(readFileSync(resolve(f.root, 'alpha/page.html'))) });
    assert.equal(result.page_id, 73);
    assert.match(result.seo_warning, /Draft exists/);
    assert.deepEqual(calls, ['list_pages', 'create_gitpress_page']);
    assert.equal(JSON.parse(readFileSync(resolve(f.config.dir, '.broseph/drafts/page.json'))).result.page_id, 73);
  } finally { f.clean(); }
});
