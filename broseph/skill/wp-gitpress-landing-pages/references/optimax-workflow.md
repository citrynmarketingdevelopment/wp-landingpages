# Optimax GitPress Landing Page Workflow Reference

## Site profile
- site: `https://optimaxcs.net`
- Broseph REST base: `https://optimaxcs.net/wp-json/broseph/v1`
- public connection profile: `optimax/broseph.json`
- local secret file: `optimax/.env.broseph` (Git-ignored)
- connection check: `node broseph/cli.mjs doctor optimax`
- repo: `citrynmarketingdevelopment/wp-landingpages`
- base path: `optimax/`
- default render mode: `theme_wrapped`
- default render position: `replace`
- SEO plugin: `yoast`

## Verified workflow
1. Pull repo changes.
2. Find requested templates under `optimax/`.
3. Read `<title>` if present; otherwise use `<h1>`.
4. Build slug from title if needed.
5. Create page with `POST /broseph/v1/gitpress/pages/create`.
6. Confirm page/GitPress settings if needed.
7. Add SEO metadata via `POST /broseph/v1/seo/page/{id}`.
8. Return preview links.
9. Publish only when explicitly requested.

## Important gotchas
- refresh `/broseph/v1/tools` before assuming routes exist
- do not assume create `meta` writes SEO fields
- GitHub raw content and live output can disagree because of caching
- verify both GitHub source and live HTML when troubleshooting
- signed auth and GitPress were verified October 12, 2026 against Broseph 0.1.1
- native WordPress menu changes and GitPress cache purges are not advertised by that live plugin; do not assume those routes exist
- the live creation endpoint can ignore `full_width_content`; read `get_gitpress_page_settings` after creation. If the requested full-width setting was not saved, use the advertised in-place conversion tool with the same shortcode, expected slug/status, and a backup to persist it. This also performs a normal WordPress page save; verify the canonical public URL rather than only cache-busting URLs.

## Published event pages (October 12, 2026)

| Page | WordPress ID | URL | Source |
| --- | --- | --- | --- |
| Events | 329308 | `/events/` | `optimax/events.html` |
| MGMA Annual Conference | 329309 | `/event-mgma-2026/` | `optimax/event-mgma-2026.html` |
| NAMIWalks Kern County | 329310 | `/event-namiwalks-kern-county-2026/` | `optimax/event-namiwalks-kern-county-2026.html` |

All use theme-wrapped rendering, replace position, full-width content, and the GitPress shortcode pointing to their source on `main`. Reuse these page IDs for updates instead of creating duplicates. The native Events menu entry remains pending admin access or a menu API.
