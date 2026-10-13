# Working on client websites

This repository contains separate client folders. Keep each task within the named client's folder unless shared tooling is part of the request.

## Broseph website connections

For live WordPress/Broseph work, use `node broseph/cli.mjs` and read `broseph/CONNECTIONS.md`. Each connected client's public mapping is in `<client>/broseph.json`; the shared secret is in the Git-ignored `<client>/.env.broseph`. Never print, copy into chat, or commit secret values. Do not use another site's credentials or global env variables as a fallback.

- Select the client explicitly. `node broseph/cli.mjs sites` lists registered sites; `doctor <site>` verifies signed auth, site identity, GitPress, and live permissions.
- For GitPress page structure, follow `GITPRESS_WEBSITE_STRUCTURE.md`. For Broseph page operations, read `broseph/skill/wp-gitpress-landing-pages/SKILL.md` and the matching site reference when one exists.
- Read-only checks and draft preparation are authorized by a request to connect or prepare pages. That request alone does not authorize publishing, changing menus, updates, sending mail, or submitting forms. Use existing session authorization where given; do not ask again for an already authorized action.
- The client refreshes the live `/tools` manifest before actions. Use advertised tool names; never guess routes or bypass a disabled plugin permission. `--write` expresses an intended mutation to the CLI; it does not replace user authorization.
- Create reviewable drafts first for new pages. `plan` records the scoped source/shortcode; `draft` verifies GitHub matches the reviewed file before creating a WordPress draft. Push source/assets only within the user's authorized scope; do not push unrelated projects.
- Inspect an existing page before changing it, preserve IDs/slugs/SEO when appropriate, and use the documented backup/conversion behavior. Publish or trash only explicitly identified pages within the user's request.
- Validate on the actual WordPress page after deployment. Local preview headers/menus do not change native Divi navigation. If the live plugin lacks a needed capability, report that limitation instead of claiming the change is live.

To onboard another site, use `init <site> --url https://actual-site.example --site-id UUID`; then populate its local env file and run `doctor`. Do not infer URLs or credentials from a client folder name.
