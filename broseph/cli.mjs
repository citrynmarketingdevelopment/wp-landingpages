#!/usr/bin/env node
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { Client, ConnectionError, credentials, createDraft, discover, initSite, planDraft, readJson, redact, selectSite } from './client.mjs';

const HELP = `Broseph multi-site client (Node.js 20+, no npm dependencies)

  node broseph/cli.mjs sites
  node broseph/cli.mjs init SITE --url https://site.com [--site-id UUID] [--folder FOLDER] [--render-mode theme_wrapped]
  node broseph/cli.mjs doctor SITE
  node broseph/cli.mjs doctor --all
  node broseph/cli.mjs tools SITE
  node broseph/cli.mjs call SITE TOOL [--input path/to/body.json] [--write]
  node broseph/cli.mjs plan SITE --source client/page.html --title "Page title" --slug page-slug [--description "Summary"]
  node broseph/cli.mjs draft SITE --plan client/.broseph/plans/page-slug.json --write

Secret files stay in each client folder as .env.broseph. Never pass secrets as arguments.
All remote actions verify the selected site identity. Writes refresh live tools/permissions.
Planning is local. Draft creation checks the reviewed source exists on GitHub; publishing is separate.
`;

function args(values) {
  const positional = [], options = {};
  for (let i = 0; i < values.length; i++) {
    const value = values[i];
    if (!value.startsWith('--')) positional.push(value);
    else {
      const key = value.slice(2);
      if (['write', 'all', 'help'].includes(key)) options[key] = true;
      else {
        if (!values[i + 1] || values[i + 1].startsWith('--')) throw new ConnectionError(`Missing value for --${key}.`);
        options[key] = values[++i];
      }
    }
  }
  const allowed = new Set(['write', 'all', 'help', 'input', 'url', 'site-id', 'folder', 'render-mode', 'source', 'title', 'slug', 'description', 'plan']);
  for (const key of Object.keys(options)) if (!allowed.has(key)) throw new ConnectionError(`Unknown option --${key}.`);
  return { positional, options };
}

const output = value => process.stdout.write(JSON.stringify(value, null, 2) + '\n');
let secret = '';
try {
  const { positional: [command, site, tool], options } = args(process.argv.slice(2));
  if (!command || command === 'help' || options.help) process.stdout.write(HELP);
  else if (command === 'sites') {
    output(discover().map(config => {
      let readiness = 'credentials_needed';
      try { credentials(config); readiness = 'ready_to_verify'; } catch { /* Missing values are summarized, never printed. */ }
      let last = null;
      const state = resolve(config.dir, '.broseph/connection.json');
      if (existsSync(state)) last = readJson(state);
      return { site: config.site, folder: config.github.base_path, url: config.site_url, readiness, last_verified: last?.checked_at || null };
    }));
  } else if (command === 'init') {
    output(initSite({ site, folder: options.folder || site, url: options.url, siteId: options['site-id'] || '', mode: options['render-mode'] || 'theme_wrapped' }));
  } else if (command === 'doctor' && options.all) {
    const results = [];
    for (const config of discover()) {
      try { results.push(await new Client(config).doctor()); }
      catch (error) { results.push({ site: config.site, connected: false, reason: error.message }); }
    }
    output(results);
    if (results.some(r => !r.connected)) process.exitCode = 1;
  } else {
    const config = selectSite(site);
    if (command === 'plan') output(planDraft(config, options));
    else {
      const client = new Client(config);
      secret = client.auth.secret;
      if (command === 'doctor') output(await client.doctor());
      else if (command === 'tools') output(await client.tools());
      else if (command === 'call') {
        if (!tool) throw new ConnectionError('Provide the advertised tool name.');
        output(await client.call(tool, options.input ? readJson(resolve(options.input)) : {}, { write: options.write === true }));
      } else if (command === 'draft') {
        if (!options.plan) throw new ConnectionError('Provide --plan with the reviewed plan file.');
        output(await createDraft(client, readJson(resolve(options.plan)), { write: options.write === true }));
      } else throw new ConnectionError(`Unknown command '${command}'. Run help.`);
    }
  }
} catch (error) {
  // Avoid raw exception objects, request headers, stack traces and response HTML.
  const message = error instanceof ConnectionError ? error.message : 'Unexpected local/network error. Check configuration and file paths; no request was retried.';
  process.stderr.write(redact(message, secret) + '\n');
  process.exitCode = 1;
}
