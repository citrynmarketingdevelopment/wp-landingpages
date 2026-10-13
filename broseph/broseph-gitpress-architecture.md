# Broseph + GitPress Architecture Map

This document is the Phase 2 master map for the Broseph multi-site workflow.

Use it to understand where workflow rules live, where secrets live, where site-specific notes live, and what should change next without breaking working flows.

## Goal

Preserve all working Broseph + GitPress workflows while making the system easier to understand, safer to operate, and easier to scale to more WordPress sites.

The shared runtime client is now `cli.mjs` / `client.mjs`. See [CONNECTIONS.md](CONNECTIONS.md) for the executable setup; this document describes its workflow layers.

## Current architecture in plain terms

The system already has five working layers:

1. Skill layer
2. Runtime env layer
3. Helper/client code layer
4. Repo documentation layer
5. Memory/history layer

### 1. Skill layer

Primary skill:
- `skill/wp-gitpress-landing-pages/SKILL.md`

Repository discovery guidance: `../AGENTS.md`.

Purpose:
- global workflow rules
- default page creation behavior
- permission refresh rules
- draft/publish rules
- SEO/update/form/mail safety rules

### 2. Runtime env layer

Per-site runtime env files exist in each client folder, excluded from version control by the root `.gitignore`.

Public site URL, REST base, Site ID, GitHub mapping and render defaults live in `<client>/broseph.json`. Only `BROSEPH_SHARED_SECRET` is needed in `<client>/.env.broseph`. Legacy URL/ID env keys are supported only when they agree with the public mapping.

### 3. Helper/client code layer

Shared client: `client.mjs`. Entry point: `node broseph/cli.mjs`.

Purpose:
- working request signing/auth
- Broseph REST client functions
- site-loading logic

### 4. Repo documentation layer

Purpose:
- GitPress HTML structure rules
- shortcode usage patterns
- per-site rendering conventions
- repo-specific file layout guidance

### 5. Memory/history layer

Purpose:
- preserve verified lessons
- preserve route/auth quirks
- preserve past troubleshooting results
- preserve historical rollout details

## Source-of-truth ownership

### Skill = global workflow brain
Put here:
- cross-site workflow rules
- mutation safety rules
- GitPress vs Divi rules
- publish/update/form/mail guidance

### Site workflow references = per-site operating notes
Put here:
- site profile
- repo mapping
- shortcode conventions
- render-mode defaults
- SEO plugin notes
- site-specific gotchas

### Env files = secrets and runtime auth
Put here:
- Broseph auth values
- repo tokens
- other sensitive runtime configuration

Never commit real env files to GitHub.

### Repo docs = GitPress content/render architecture
Put here:
- HTML partial rules
- render-mode architecture
- shortcode structure conventions
- repo layout patterns

### Memory = verified historical lessons
Put here:
- what actually happened
- what was verified live
- what failed and why

### Helper/client code = execution layer
Put here:
- signing logic
- endpoint wrappers
- validation helpers

## Operating principle

Preserve working workflows first. Normalize structure second. Never sacrifice working site behavior just to make docs look cleaner.
