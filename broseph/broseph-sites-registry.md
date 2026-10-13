# Broseph Site Registry

This is the human-readable control center for Broseph-managed WordPress sites.

The shared CLI discovers each client's `broseph.json`; see [CONNECTIONS.md](CONNECTIONS.md) for runtime setup. Secret files and local verification state are Git-ignored.

## citryn
- site URL: `https://citryn.com`
- Broseph REST base: `https://citryn.com/wp-json/broseph/v1`
- public connection: `test-web/broseph.json`
- env file target: `test-web/.env.broseph` (local only)
- repo: `citrynmarketingdevelopment/wp-landingpages`
- base path: `test-web/` for the prepared profile; register a separate profile for another folder
- default creation mode: `gitpress_page`
- default render mode: `full_canvas` unless task calls for something else
- notes:
  - profile prepared; Site ID and secret still needed before live verification
  - primary feature-validation site for Broseph
  - strong examples for GitPress page creation, Divi template cloning, forms, mail tests, and updates

## optimax
- site URL: `https://optimaxcs.net`
- Broseph REST base: `https://optimaxcs.net/wp-json/broseph/v1`
- public connection: `optimax/broseph.json`
- env file target: `optimax/.env.broseph` (local only)
- repo: `citrynmarketingdevelopment/wp-landingpages`
- base path: `optimax/`
- default creation mode: `gitpress_page`
- default render mode: `theme_wrapped`
- notes:
  - signed status/tools checks passed October 12, 2026; Broseph 0.1.1 and GitPress confirmed
  - live manifest has no native WordPress menu endpoint or GitPress cache-purge support
  - most mature documented rollout history
  - existing Divi → GitPress migration notes
  - caching can make raw GitHub and live output appear out of sync

## pwc
- site URL: `https://psychwellnesscenter.com`
- Broseph REST base: `https://psychwellnesscenter.com/wp-json/broseph/v1`
- public connection: `pwc/broseph.json`
- env file target: `pwc/.env.broseph` (local only)
- repo: `citrynmarketingdevelopment/wp-landingpages` (verify live workflow assumptions before first major rollout)
- base path: `pwc/`
- default creation mode: `gitpress_page`
- default render mode: `theme_wrapped`
- notes:
  - profile prepared; Site ID and secret still needed before live verification
  - partially documented
  - requires more live verification for repo mapping and SEO behavior

## Future site onboarding
For every new site:
1. run `node broseph/cli.mjs init CLIENT --url https://actual-site.example --site-id UUID`
2. populate the Git-ignored client-local `.env.broseph`, then add site-specific workflow notes when needed
3. confirm repo/folder mapping
4. run `node broseph/cli.mjs doctor CLIENT` to confirm Broseph auth, identity, tools, and permissions live
5. confirm GitPress render defaults
6. confirm SEO plugin behavior
7. save important verification notes
