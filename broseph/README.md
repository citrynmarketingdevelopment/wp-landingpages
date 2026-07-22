# Broseph Workflow Bundle

This folder contains a safe, repo-friendly copy of the Broseph + GitPress workflow documentation used for WordPress site operations.

It is intended to preserve the operating model without exposing secrets.

## Included here

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
- Treat this folder as documentation/templates only.
- Real runtime env files stay outside version control.

## Purpose

This bundle makes it easier to reuse the Broseph + GitPress workflow in other tools and environments such as VS Code, Codex, Claude, or future OpenClaw workspaces.
