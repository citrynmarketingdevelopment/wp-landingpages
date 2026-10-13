# Broseph Workflow Bundle

This folder contains the shared Broseph multi-site client and the Broseph + GitPress workflow documentation used for WordPress site operations.

It is intended to preserve the operating model without exposing secrets.

## Included here

- `cli.mjs` and `client.mjs` — signed REST client with explicit site selection
- `CONNECTIONS.md` — setup, onboarding, daily commands, and draft workflow
- `tests/client.test.mjs` — signing, isolation, permission, and draft checks
- `broseph-gitpress-architecture.md`
- `broseph-sites-registry.md`
- `skill/wp-gitpress-landing-pages/SKILL.md`
- `skill/wp-gitpress-landing-pages/references/optimax-workflow.md`
- `skill/wp-gitpress-landing-pages/references/pwc-workflow.md`
- `skill/wp-gitpress-landing-pages/references/citryn-workflow.md`
- `env/.env.example`
- `env/.env.citryn.example`
- `env/.env.optimax.example`
- `env/.env.pwc.example`

## Important rules

- Do not commit real `.env` secrets.
- Keep raw `BROSEPH_SHARED_SECRET` values out of GitHub.
- Real runtime env files stay outside version control.
- Each client uses `broseph.json` for public mapping and `.env.broseph` for its local secret.
- Existing `env/.env.*.example` files remain legacy templates; use the client-local examples for the new CLI.

## Start here

```powershell
node broseph/cli.mjs sites
node broseph/cli.mjs doctor optimax
```

See [CONNECTIONS.md](CONNECTIONS.md) for the complete operating guide.

## Purpose

This bundle makes it easier to reuse the Broseph + GitPress workflow in other tools and environments such as VS Code, Codex, Claude, or future OpenClaw workspaces.
