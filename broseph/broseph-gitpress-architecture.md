# Broseph + GitPress Architecture Map

This document is the Phase 2 master map for the Broseph multi-site workflow.

Use it to understand where workflow rules live, where secrets live, where site-specific notes live, and what should change next without breaking working flows.

## Goal

Preserve all working Broseph + GitPress workflows while making the system easier to understand, safer to operate, and easier to scale to more WordPress sites.

This is a docs-and-structure layer only. It does not change runtime behavior.

## Current architecture in plain terms

The system already has five working layers:

1. Skill layer
2. Runtime env layer
3. Helper/client code layer
4. Repo documentation layer
5. Memory/history layer

### 1. Skill layer

Primary skill:
- `skills/wp-gitpress-landing-pages/SKILL.md`

Purpose:
- global workflow rules
- default page creation behavior
- permission refresh rules
- draft/publish rules
- SEO/update/form/mail safety rules

### 2. Runtime env layer

Per-site runtime env files should exist outside version control.

Typical keys:
- `BROSEPH_SITE_URL`
- `BROSEPH_REST_BASE`
- `BROSEPH_SITE_ID`
- `BROSEPH_SHARED_SECRET`

### 3. Helper/client code layer

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
