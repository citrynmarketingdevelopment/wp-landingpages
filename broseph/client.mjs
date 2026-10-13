import { createHash, createHmac, randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, writeFileSync } from 'node:fs';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const NAMESPACE = '/broseph/v1';
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const MODES = ['theme_wrapped', 'full_canvas', 'gitpress_managed'];

export class ConnectionError extends Error {}
export const hash = value => createHash('sha256').update(value).digest('hex');
// Git normalizes Windows CRLF in text files; keep HTTP body signing byte-exact.
export const sourceHash = value => hash(value.toString('utf8').replace(/\r\n/g, '\n'));

export function readJson(file) {
  try { return JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, '')); }
  catch { throw new ConnectionError(`Cannot read valid JSON: ${file}`); }
}

export function contained(root, path) {
  const rel = relative(root, path);
  return rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel);
}

export function parseEnv(contents) {
  // Parse data only; never source/evaluate env files or expand shell expressions.
  const result = {};
  for (const raw of contents.replace(/^\uFEFF/, '').split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const match = line.match(/^(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*(.*)$/);
    if (!match) throw new ConnectionError('Invalid env syntax. Use KEY=value, one key per line.');
    if (Object.hasOwn(result, match[1])) throw new ConnectionError(`Duplicate env key: ${match[1]}`);
    let value = match[2].trim();
    if (/^['"]/.test(value)) {
      const quote = value[0];
      const end = value.lastIndexOf(quote);
      if (end === 0 || !/^\s*(?:#.*)?$/.test(value.slice(end + 1))) throw new ConnectionError('Invalid quoted env value.');
      value = value.slice(1, end);
    } else value = value.replace(/\s+#.*$/, '').trim();
    result[match[1]] = value;
  }
  return result;
}

export function discover(root = ROOT) {
  const sites = [];
  for (const folder of readdirSync(root, { withFileTypes: true })) {
    if (!folder.isDirectory() || folder.name.startsWith('.')) continue;
    const configPath = resolve(root, folder.name, 'broseph.json');
    if (existsSync(configPath)) sites.push(loadConfig(configPath, root));
  }
  const names = new Set();
  for (const config of sites) {
    if (names.has(config.site)) throw new ConnectionError(`Duplicate site alias: ${config.site}`);
    names.add(config.site);
  }
  return sites.sort((a, b) => a.site.localeCompare(b.site));
}

export function loadConfig(configPath, root = ROOT) {
  const config = readJson(configPath);
  if (config.schema_version !== 1 || !SLUG.test(config.site)) throw new ConnectionError(`Invalid site config: ${configPath}`);
  const siteUrl = new URL(config.site_url);
  const base = new URL(config.rest_base);
  if (siteUrl.protocol !== 'https:' || base.protocol !== 'https:' || siteUrl.origin !== base.origin ||
      [siteUrl, base].some(u => u.username || u.password || u.search || u.hash) ||
      !base.pathname.endsWith('/wp-json/broseph/v1')) {
    throw new ConnectionError('Site URL and REST base must be HTTPS on the same host, with no embedded credentials/query/fragment.');
  }
  if (!MODES.includes(config.defaults?.render_mode)) throw new ConnectionError('Invalid default render_mode.');
  const dir = realpathSync(dirname(configPath));
  if (!contained(realpathSync(root), dir)) throw new ConnectionError('Client folder resolves outside this project.');
  if (config.env_file !== '.env.broseph') throw new ConnectionError('Use .env.broseph in the client folder for credentials.');
  const github = config.github;
  if (!github || !/^[\w.-]+$/.test(github.owner) || !/^[\w.-]+$/.test(github.repo) ||
      !/^[\w./-]+$/.test(github.branch) || github.branch.includes('..') ||
      github.base_path !== relative(root, dir).split(sep).join('/') + '/') {
    throw new ConnectionError('GitHub base_path must match the client folder, and repository/branch names must be valid.');
  }
  return { ...config, dir, configPath, root: realpathSync(root) };
}

export function selectSite(name, root = ROOT) {
  if (!name) throw new ConnectionError('Select a site explicitly. Run: node broseph/cli.mjs sites');
  const config = discover(root).find(site => site.site === name);
  if (!config) throw new ConnectionError(`Unknown site '${name}'. Run sites or init first.`);
  return config;
}

export function credentials(config) {
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(config.site_id || '')) {
    throw new ConnectionError(`Add ${config.site}'s Site ID to ${config.configPath}.`);
  }
  const path = resolve(config.dir, config.env_file);
  if (!existsSync(path)) throw new ConnectionError(`Create the local credentials file: ${path}`);
  const env = parseEnv(readFileSync(path, 'utf8'));
  for (const [key, value] of [['BROSEPH_SITE_ID', config.site_id], ['BROSEPH_SITE_URL', config.site_url], ['BROSEPH_REST_BASE', config.rest_base]]) {
    if (env[key] && env[key].replace(/\/$/, '') !== value.replace(/\/$/, '')) {
      throw new ConnectionError(`${key} in the local env does not match ${config.site}'s public config.`);
    }
  }
  if (env.BROSEPH_SECRET && env.BROSEPH_SHARED_SECRET && env.BROSEPH_SECRET !== env.BROSEPH_SHARED_SECRET) {
    throw new ConnectionError('BROSEPH_SECRET and BROSEPH_SHARED_SECRET disagree. Keep one secret key.');
  }
  const secret = env.BROSEPH_SHARED_SECRET || env.BROSEPH_SECRET || '';
  if (!/^[0-9a-f]{64}$/i.test(secret)) throw new ConnectionError(`Save the full 64-character Shared Secret in ${path}. It is missing or incomplete.`);
  // Global process.env secrets are intentionally not a fallback: avoid cross-site auth.
  return { siteId: config.site_id, secret };
}

export function redact(value, secret = '') {
  const walk = current => {
    if (Array.isArray(current)) return current.map(walk);
    if (current && typeof current === 'object') return Object.fromEntries(Object.entries(current).map(([key, val]) =>
      [key, /secret|password|token|authorization|signature/i.test(key) ? '[redacted]' : walk(val)]));
    return typeof current === 'string' && secret ? current.split(secret).join('[redacted]') : current;
  };
  return walk(value);
}

export function sign({ method, route, body = '', siteId, secret, timestamp = String(Math.floor(Date.now() / 1000)), nonce = randomBytes(16).toString('hex') }) {
  if (!new RegExp(`^${NAMESPACE}/[a-z0-9/_-]+$`, 'i').test(route)) throw new ConnectionError('Sign a Broseph REST route without /wp-json or query parameters.');
  const payload = [method.toUpperCase(), route, timestamp, nonce, hash(body)].join('\n');
  return {
    'X-Broseph-Site-Id': siteId,
    'X-Broseph-Timestamp': timestamp,
    'X-Broseph-Nonce': nonce,
    'X-Broseph-Signature': createHmac('sha256', secret).update(payload).digest('hex'),
  };
}

export class Client {
  constructor(config, auth = credentials(config), transport = fetch) {
    this.config = config;
    this.auth = auth;
    this.transport = transport;
  }

  async request(method, route, input = {}) {
    const url = new URL(this.config.rest_base + route.slice(NAMESPACE.length));
    const body = method === 'GET' ? '' : JSON.stringify(input);
    if (method === 'GET') for (const [key, value] of Object.entries(input)) url.searchParams.set(key, String(value));
    const headers = { ...sign({ method, route, body, ...this.auth }), Accept: 'application/json', 'User-Agent': 'Broseph-Multi-Site-Client/1.0' };
    if (method !== 'GET') headers['Content-Type'] = 'application/json';
    let response;
    try {
      response = await this.transport(url, { method, headers, body: body || undefined, redirect: 'manual', signal: AbortSignal.timeout(20000) });
    } catch {
      throw new ConnectionError(`${this.config.site}: network/TLS failure or timeout. No automatic retry was made.`);
    }
    if (response.status >= 300 && response.status < 400) throw new ConnectionError(`${this.config.site}: redirect blocked. Set the canonical HTTPS URL in broseph.json.`);
    let data;
    try { data = await response.json(); }
    catch { throw new ConnectionError(`${this.config.site}: HTTP ${response.status} returned non-JSON content; check WordPress REST access or the hosting firewall.`); }
    if (!response.ok) {
      const clean = redact(data, this.auth.secret);
      throw new ConnectionError(`${this.config.site}: HTTP ${response.status} ${clean.code || 'API error'}: ${clean.message || 'Request failed.'}`);
    }
    return redact(data, this.auth.secret);
  }

  async status() {
    const status = await this.request('GET', NAMESPACE + '/status');
    const expectedUrl = new URL(this.config.site_url).href.replace(/\/$/, '');
    let actualUrl;
    try { actualUrl = new URL(status.site_url).href.replace(/\/$/, ''); } catch { actualUrl = ''; }
    if (status.auth_status !== 'accepted' || status.site_id !== this.auth.siteId || actualUrl !== expectedUrl) {
      throw new ConnectionError(`${this.config.site}: returned site identity does not match the selected connection.`);
    }
    return status;
  }

  async tools() {
    await this.status();
    const manifest = await this.request('GET', NAMESPACE + '/tools');
    if (manifest.namespace !== 'broseph/v1' || !Array.isArray(manifest.tools)) throw new ConnectionError('Unexpected Broseph tools response.');
    return manifest;
  }

  async call(name, input = {}, { write = false } = {}) {
    // Always refresh live permissions; never execute from a cached manifest.
    const manifest = await this.tools();
    const tool = manifest.tools.find(item => item.name === name);
    if (!tool) throw new ConnectionError(`The live plugin does not advertise '${name}'. Inspect tools or update the plugin; do not invent a route.`);
    if (tool.available !== true) throw new ConnectionError(`'${name}' is unavailable. Check its Broseph permission toggle or required plugin.`);
    if (tool.risk_level !== 'read_only' && !write) throw new ConnectionError(`'${name}' changes the site. Run the explicitly intended action with --write.`);
    if (!['GET', 'POST'].includes(tool.method)) throw new ConnectionError('Unsupported advertised HTTP method.');
    if (!input || typeof input !== 'object' || Array.isArray(input)) throw new ConnectionError('Tool input must be a JSON object.');
    if (name === 'create_gitpress_page' || name === 'convert_page_to_gitpress') validateShortcode(this.config, input.shortcode);
    const params = { ...input };
    const route = tool.endpoint.replace(/\{([a-z_]+)\}/g, (_, key) => {
      const value = params[key];
      if (!Number.isSafeInteger(Number(value)) || Number(value) < 1) throw new ConnectionError(`Provide a positive integer '${key}'.`);
      delete params[key];
      return String(Number(value));
    });
    const result = await this.request(tool.method, route, params);
    saveLocal(this.config, 'last-action.json', {
      site: this.config.site, site_id: this.config.site_id, timestamp: new Date().toISOString(),
      tool: name, method: tool.method, route, page_id: result.page_id || result.new_page_id || null,
    });
    return result;
  }

  async doctor() {
    const status = await this.status();
    const tools = await this.request('GET', NAMESPACE + '/tools');
    if (!Array.isArray(tools.tools) || tools.namespace !== 'broseph/v1') throw new ConnectionError('Unexpected Broseph tools response.');
    const summary = {
      site: this.config.site, connected: true, site_url: status.site_url, site_id: status.site_id,
      plugin_version: status.plugin_version, checked_at: new Date().toISOString(),
      gitpress_available: tools.context?.gitpress_available === true,
      available_tools: tools.tools.filter(t => t.available).map(t => t.name),
      permissions: tools.context?.permissions || {},
      menu_api_available: tools.tools.some(t => /menu/.test(t.name) && t.available),
    };
    saveLocal(this.config, 'connection.json', summary);
    saveLocal(this.config, 'tools.json', tools);
    return summary;
  }
}

export function saveLocal(config, filename, data) {
  const path = resolve(config.dir, '.broseph', filename);
  if (!contained(resolve(config.dir, '.broseph'), path)) throw new ConnectionError('Invalid local state path.');
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n', { mode: 0o600 });
  return path;
}

export function initSite({ site, folder = site, url, siteId = '', mode = 'theme_wrapped' }, root = ROOT) {
  if (!SLUG.test(site || '') || !SLUG.test(folder || '') || !MODES.includes(mode)) throw new ConnectionError('Use a simple lowercase site/folder alias and a supported render mode.');
  const siteUrl = new URL(url);
  if (siteUrl.protocol !== 'https:' || siteUrl.username || siteUrl.password || siteUrl.search || siteUrl.hash) throw new ConnectionError('Provide the actual HTTPS site URL.');
  if (discover(root).some(config => config.site === site)) throw new ConnectionError(`Site '${site}' already exists. Edit its config; init does not overwrite it.`);
  const dir = resolve(root, folder);
  if (existsSync(dir) && !contained(realpathSync(root), realpathSync(dir))) throw new ConnectionError('Client folder resolves outside this project.');
  if (existsSync(resolve(dir, 'broseph.json'))) throw new ConnectionError('The client folder already has a Broseph config.');
  const canonical = siteUrl.href.replace(/\/$/, '');
  const config = {
    schema_version: 1, site, site_url: canonical, rest_base: canonical + '/wp-json/broseph/v1',
    site_id: siteId, env_file: '.env.broseph',
    github: { owner: 'citrynmarketingdevelopment', repo: 'wp-landingpages', branch: 'main', base_path: folder + '/' },
    defaults: { render_mode: mode, render_position: 'replace', full_width_content: mode === 'theme_wrapped', full_page_canvas: mode !== 'theme_wrapped', seo_plugin: 'auto' },
  };
  mkdirSync(dir, { recursive: true });
  writeFileSync(resolve(dir, 'broseph.json'), JSON.stringify(config, null, 2) + '\n', { flag: 'wx' });
  const example = '# Keep this file local; paste the full secret from Broseph Connection.\nBROSEPH_SHARED_SECRET=\n';
  for (const filename of ['.env.broseph', '.env.broseph.example']) {
    if (!existsSync(resolve(dir, filename))) writeFileSync(resolve(dir, filename), example, { flag: 'wx', mode: 0o600 });
  }
  return { site, config: resolve(dir, 'broseph.json'), credentials_file: resolve(dir, '.env.broseph'), connected: false };
}

export function validateShortcode(config, shortcode) {
  if (typeof shortcode !== 'string' || !/^\[divi_github_content\s[^\]]+\]$/.test(shortcode)) throw new ConnectionError('Use one divi_github_content shortcode for the selected client.');
  const attributes = Object.fromEntries([...shortcode.matchAll(/([a-z_]+)="([^"]*)"/g)].map(m => [m[1], m[2]]));
  const gh = config.github;
  if (attributes.owner !== gh.owner || attributes.repo !== gh.repo || attributes.branch !== gh.branch ||
      attributes.format !== 'html' || !attributes.path?.startsWith(gh.base_path) ||
      !/^[a-z0-9_./ -]+\.html$/i.test(attributes.path) || attributes.path.includes('..')) {
    throw new ConnectionError('Shortcode must use the selected client folder and its configured GitHub repository/branch.');
  }
}

export function buildDraftPlan(config, { source, title, slug, description = '' }) {
  if (!SLUG.test(slug || '') || !title?.trim()) throw new ConnectionError('Provide a title and a lowercase page slug.');
  const file = resolve(config.root, source);
  if (!existsSync(file) || !contained(config.dir, realpathSync(file)) || !file.endsWith('.html')) throw new ConnectionError('The HTML source must exist inside the selected client folder.');
  const path = relative(config.root, realpathSync(file)).split(sep).join('/');
  const gh = config.github;
  const shortcode = `[divi_github_content owner="${gh.owner}" repo="${gh.repo}" branch="${gh.branch}" path="${path}" format="html"]`;
  validateShortcode(config, shortcode);
  const { seo_plugin, ...settings } = config.defaults;
  return {
    site: config.site, site_id: config.site_id, source: path, source_sha256: sourceHash(readFileSync(file)),
    source_url: `https://raw.githubusercontent.com/${gh.owner}/${gh.repo}/${gh.branch}/${path}`,
    payload: { title, slug, excerpt: description, shortcode, ...settings },
    seo: { seo_plugin, title, description },
  };
}

export function planDraft(config, options) {
  const plan = buildDraftPlan(config, options);
  return { path: saveLocal(config, `plans/${options.slug}.json`, plan), plan };
}

export async function createDraft(client, plan, { write = false, transport = fetch } = {}) {
  const config = client.config;
  if (!write) throw new ConnectionError('Creating a draft requires --write. Review the plan first.');
  if (plan.site !== config.site || plan.site_id !== config.site_id) throw new ConnectionError('The plan belongs to a different site or credentials have rotated. Regenerate the plan.');
  const current = buildDraftPlan(config, { source: plan.source, title: plan.payload.title, slug: plan.payload.slug, description: plan.seo.description });
  if (current.source_sha256 !== plan.source_sha256 || current.source_url !== plan.source_url || JSON.stringify(current.payload) !== JSON.stringify(plan.payload)) throw new ConnectionError('Source/config changed after the plan was made. Review and regenerate the plan.');
  const response = await transport(current.source_url, { redirect: 'manual', signal: AbortSignal.timeout(20000) });
  if (!response.ok || sourceHash(Buffer.from(await response.arrayBuffer())) !== plan.source_sha256) throw new ConnectionError('GitHub source is absent or differs from the reviewed local file. Push the intended source/assets and make a new plan before creating a draft.');
  // Avoid duplicate WordPress pages. Check all returned search pages for an exact slug.
  let page = 1, total = 1;
  do {
    // WordPress text search does not reliably search post_name (the slug).
    const existing = await client.call('list_pages', { per_page: 100, page, status: 'publish,draft,pending,private,future' });
    if (!Array.isArray(existing.pages)) throw new ConnectionError('Unexpected pages response; cannot verify duplicate slugs.');
    if (existing.pages.some(item => item.slug === plan.payload.slug)) throw new ConnectionError('That slug already exists in WordPress. Inspect and update/convert the existing page instead.');
    total = Number(existing.total_pages || 1);
  } while (++page <= total);
  const result = await client.call('create_gitpress_page', plan.payload, { write: true });
  // Record the created ID before SEO, so a later metadata failure cannot hide a draft.
  saveLocal(config, `drafts/${plan.payload.slug}.json`, { plan, result });
  try {
    const manifest = await client.tools();
    if (manifest.tools.some(t => t.name === 'update_seo_meta' && t.available)) {
      const seo = { ...plan.seo };
      if (seo.seo_plugin === 'auto') delete seo.seo_plugin;
      result.seo = await client.call('update_seo_meta', { id: result.page_id, ...seo }, { write: true });
    } else result.seo_warning = 'Draft exists; SEO update is not available in the live plugin.';
  } catch (error) { result.seo_warning = `Draft exists; SEO update failed: ${error.message}`; }
  saveLocal(config, `drafts/${plan.payload.slug}.json`, { plan, result });
  return result;
}
