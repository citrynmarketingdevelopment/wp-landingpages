# Multi-site Broseph connections

The shared client lives in this repository; every site's identity and secret stay in its own client folder. This works with the existing Broseph REST plugin and requires Node.js 20 or newer. No npm install, persistent server, or WordPress plugin changes are required.

```text
wp-landingpages/
  AGENTS.md                     Agent instructions for selecting/using sites
  broseph/
    cli.mjs                     Commands for all registered sites
    client.mjs                  Signing, identity checks, live tool discovery
    CONNECTIONS.md              This guide
  optimax/
    broseph.json                Public URL, site ID, GitHub mapping, render defaults
    .env.broseph.example         Blank, safe to commit
    .env.broseph                 Actual shared secret, ignored by Git
    .broseph/                   Local tools/status/plans/draft IDs, ignored by Git
  pwc/                          Same layout
  test-web/                     Citryn profile, same layout
```

Site aliases are discovered from each client folder's `broseph.json`; no second machine-readable registry is needed. The Markdown registry and workflow references remain human-readable context. Configurations identify their GitHub folder so a draft for Optimax cannot accidentally reference a PWC page.

## Current sites

| Alias | Folder | Site | Initial connection state |
| --- | --- | --- | --- |
| `optimax` | `optimax/` | `https://optimaxcs.net` | Signed status/tools checks passed October 12, 2026; Broseph 0.1.1; GitPress available |
| `pwc` | `pwc/` | `https://psychwellnesscenter.com` | Profile prepared; add Site ID and local secret, then verify |
| `citryn` | `test-web/` | `https://citryn.com` | Profile prepared from existing registry; add Site ID and local secret, then verify |

These last two domains/folder mappings come from the existing registry and have not been verified by this setup. Set any corrected values before using them. `sites` reports credential readiness and the last successful verification time; it does not assume a site is currently reachable. `doctor` performs a fresh check.

## Everyday commands

From this repository's root:

```powershell
node broseph/cli.mjs sites
node broseph/cli.mjs doctor optimax
node broseph/cli.mjs tools optimax
node broseph/cli.mjs call optimax list_pages
node broseph/cli.mjs call optimax scan_gitpress_usages
node broseph/cli.mjs doctor --all
```

`doctor --all` only reads sites, sequentially, and reports each result. It returns a nonzero exit code if any site is missing credentials or fails verification. Every API action also verifies the returned site URL, site ID, and `auth_status` before using its live tools manifest. Local cached manifests are for inspection; they are never a substitute for fresh permissions on a write.

Pass query/body values using a JSON file. For example, a file containing `{"id":123}` can be used with:

```powershell
node broseph/cli.mjs call optimax get_page --input optimax/.broseph/page-input.json
```

Use the live `tools` response for names, inputs, availability, risk levels, and approval metadata. The client executes only advertised tools. Parameters such as `id` replace route placeholders; other GET inputs become query parameters, and POST inputs become a JSON body. Mutations require `--write`; the agent must separately respect the user's authorization. The tool itself still enforces the WordPress Broseph permission settings.

## Onboard another client

1. Activate Broseph in that site's WordPress admin and open its Connection screen.
2. Copy the actual canonical HTTPS site URL and Site ID. Register the site:

   ```powershell
   node broseph/cli.mjs init new-client --url https://actual-client-domain.example --site-id YOUR-SITE-UUID
   ```

3. In `new-client/.env.broseph`, put the full shared secret after `BROSEPH_SHARED_SECRET=`. Save it locally. Copy/paste directly from the plugin's Reveal/Copy Secret controls; do not put it in a command argument or chat message.
4. Confirm `new-client/broseph.json` has the correct GitHub repository, branch, folder, and render defaults. `theme_wrapped` retains the site's native theme/Divi header/footer. Choose `full_canvas` or `gitpress_managed` only when the site workflow calls for it.
5. Run `node broseph/cli.mjs doctor new-client`. This verifies the actual site before any content changes.

`init` creates the public config, a blank example env, and the local env if absent. It never overwrites an existing connection or secret. To use an existing folder under a different alias, add `--folder folder-name`. To rotate credentials, update the Site ID in `broseph.json` and the full secret in `.env.broseph`, then run `doctor` again. Existing draft plans must be regenerated after identity changes.

## Prepare and create a GitPress draft

Plan first, using the source path relative to the repository root:

```powershell
node broseph/cli.mjs plan optimax --source optimax/events.html --title Events --slug events --description "Meet Optimax at healthcare conferences and community events."
```

This writes `optimax/.broseph/plans/events.json` with the request payload, SEO fields, selected site ID, source URL, and source checksum. Review the HTML preview and plan. Commit/push the intended source and its images to the configured GitHub branch within the user's authorized scope. The GitPress plugin fetches that branch; an unpushed local file is not a live source.

Then create the draft:

```powershell
node broseph/cli.mjs draft optimax --plan optimax/.broseph/plans/events.json --write
```

The client refuses if the plan belongs to another site, the local source/config changed, GitHub bytes differ, the slug already exists, or the live plugin does not permit creation. It refreshes live permissions, creates the draft, records its ID/preview URL locally, and sets SEO through the separate endpoint if available. It never publishes the draft. If SEO fails, the response explicitly says the draft exists; use the saved ID instead of creating another page.

Source checks normalize Windows CRLF to LF, matching Git's text-file behavior. All other content must match. HMAC authentication still signs the exact HTTP body bytes without normalization.

Draft preview URLs can require WordPress admin login; signed API credentials do not create a browser admin session. Publishing uses the separately advertised `publish_page` or `bulk_publish_pages` tools with explicit IDs and the user's authorization. No credentials grant implicit approval to publish.

## How authentication works

The implementation was inspected at `D:/Projects/broseph-plugin/includes/Auth/RequestSigner.php`. Each call sends:

- `X-Broseph-Site-Id`
- `X-Broseph-Timestamp` (Unix seconds; plugin allows a five-minute difference)
- `X-Broseph-Nonce` (new random value for every request; plugin rejects replay)
- `X-Broseph-Signature` (HMAC-SHA256)

The canonical payload is `METHOD + "\n" + REST_ROUTE + "\n" + TIMESTAMP + "\n" + NONCE + "\n" + SHA256(raw_body)`. Sign `/broseph/v1/status`, while the HTTP URL is `https://site/wp-json/broseph/v1/status`. **Do not sign `/wp-json` or query parameters.** The existing plugin signing docs contain contradictory examples; the PHP verifier is authoritative. Secrets are used as literal strings, not hex-decoded bytes. The client signs exactly the UTF-8 body it sends.

The actual credential file is loaded directly as data, with no shell execution or variable expansion. It supports `BROSEPH_SHARED_SECRET` and the older `BROSEPH_SECRET` alias; conflicting values are rejected. Global environment secrets are deliberately not used as a fallback. Optional legacy URL/Site ID env values must match the public config.

The client requires HTTPS, blocks redirects so signed headers cannot follow another URL, uses a 20-second timeout, and never retries a mutation automatically. It does not disable certificate validation. Secrets, signatures, and token/password fields are redacted from API output; local action records store only site/tool/time/page ID, without request bodies or authentication headers. Cached API metadata and plans are Git-ignored too.

Git ignore prevents accidental commits; it is not encryption. Keep the project directory under your own Windows account. Check with `git check-ignore optimax/.env.broseph`; the `.example` file should remain trackable.

## Current plugin limitations

- Optimax's live Broseph 0.1.1 manifest exposes pages, GitPress, Divi, SEO, forms/mail, reports, and updates. It has **no native WordPress navigation-menu tool**. Add Events through WordPress admin or implement/deploy a dedicated menu API in a separate plugin task. Preview navigation and GitPress-managed headers cannot substitute for editing a native Divi menu.
- The inspected GitPress status endpoint reports `cache_purge_supported: false`. Do not invent a cache-purge route. Use the site's actual GitPress cache controls/webhook behavior and verify rendered source markers.
- Permissions vary by site and can change. A toggle allowing publish or updates is a capability, not an instruction to perform those actions.
- Broseph itself is a WordPress REST integration. This local CLI makes it directly usable from this workspace; it does not install a ChatGPT connector or an MCP server.

## Verify the shared client

```powershell
node --test broseph/tests/client.test.mjs
node broseph/cli.mjs doctor optimax
git diff --check
```

Repository guidance in `AGENTS.md` points future coding sessions to this setup. Its role follows [OpenAI's project-instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
