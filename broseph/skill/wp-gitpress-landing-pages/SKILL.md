---
name: wp-gitpress-landing-pages
description: Create, update, SEO-optimize, preview, publish, and clean up WordPress pages sourced from GitHub-hosted HTML files using Broseph, GitPress or Divi GitHub Sync, Yoast SEO or Rank Math, and OpenClaw. Use when managing any WordPress site connected through the Broseph plugin where repo files must become draft pages, SEO metadata must be set through Broseph endpoints, preview links must be returned for review, permissions/routes must be refreshed from `/broseph/v1/tools`, or explicitly listed pages must be published or trashed.
---

# WP GitPress Landing Pages

## Overview
Use this skill for any managed WordPress site where Broseph is connected to the site and GitPress or Divi GitHub Sync is used to render GitHub-hosted HTML into WordPress pages.

Core rules:
- refresh Broseph tools before mutating actions
- create draft pages first
- set SEO metadata after creation
- return preview URLs for review
- publish only when explicitly asked
- never commit raw secrets to GitHub

## Multi-site env model
Use site-specific env files outside version control.
Typical keys:
- `BROSEPH_SITE_URL`
- `BROSEPH_REST_BASE`
- `BROSEPH_SITE_ID`
- `BROSEPH_SHARED_SECRET`

## Default page creation rule
Use GitPress page-level creation for new AI-generated pages unless the operator explicitly asks for Divi template mode.

## Divi exception rule
Use Divi template cloning only when explicitly requested or when a `template_page_id` is provided.

## Existing-page rule
Use Divi code-module insertion only for existing Divi pages when explicitly requested.

## Site references
Read the matching site reference before rollout work:
- `references/optimax-workflow.md`
- `references/pwc-workflow.md`
- `references/citryn-workflow.md`
