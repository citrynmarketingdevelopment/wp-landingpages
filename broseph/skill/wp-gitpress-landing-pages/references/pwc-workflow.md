# PWC GitPress Landing Page Workflow Reference

## Site profile
- site: `https://psychwellnesscenter.com`
- Broseph REST base: `https://psychwellnesscenter.com/wp-json/broseph/v1`
- repo mapping: verify before first major rollout
- default render mode: `theme_wrapped`
- default render position: `replace`

## Working assumptions
1. Confirm active target is PWC before mutation.
2. Refresh Broseph tools.
3. Confirm requested repo/folder mapping.
4. Create or update HTML file.
5. Create page with `POST /broseph/v1/gitpress/pages/create`.
6. Confirm page/GitPress settings if needed.
7. Add SEO metadata after creation.
8. Return preview links.
9. Publish only when explicitly requested.

## Important gotchas
- repo mapping still needs verification
- SEO plugin still needs verification
- do not assume page creation `meta` writes SEO fields
- do not assume publish/delete/SEO routes until `/broseph/v1/tools` confirms them
