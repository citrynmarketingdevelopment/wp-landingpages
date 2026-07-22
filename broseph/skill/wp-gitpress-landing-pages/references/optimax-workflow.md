# Optimax GitPress Landing Page Workflow Reference

## Site profile
- site: `https://optimaxcs.net`
- Broseph REST base: `https://optimaxcs.net/wp-json/broseph/v1`
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
