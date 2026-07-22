# Broseph Site Registry

This is the human-readable control center for Broseph-managed WordPress sites.

## citryn
- site URL: `https://citryn.com`
- Broseph REST base: `https://citryn.com/wp-json/broseph/v1`
- env file target: `.env.citryn`
- repo: `citrynmarketingdevelopment/wp-landingpages`
- base path: `test-web/` or task-specific path
- default creation mode: `gitpress_page`
- default render mode: `full_canvas` unless task calls for something else
- notes:
  - primary feature-validation site for Broseph
  - strong examples for GitPress page creation, Divi template cloning, forms, mail tests, and updates

## optimax
- site URL: `https://optimaxcs.net`
- Broseph REST base: `https://optimaxcs.net/wp-json/broseph/v1`
- env file target: `.env.optimax`
- repo: `citrynmarketingdevelopment/wp-landingpages`
- base path: `optimax/`
- default creation mode: `gitpress_page`
- default render mode: `theme_wrapped`
- notes:
  - most mature documented rollout history
  - existing Divi → GitPress migration notes
  - caching can make raw GitHub and live output appear out of sync

## pwc
- site URL: `https://psychwellnesscenter.com`
- Broseph REST base: `https://psychwellnesscenter.com/wp-json/broseph/v1`
- env file target: `.env.pwc`
- repo: `citrynmarketingdevelopment/wp-landingpages` (verify live workflow assumptions before first major rollout)
- base path: `pwc/`
- default creation mode: `gitpress_page`
- default render mode: `theme_wrapped`
- notes:
  - partially documented
  - requires more live verification for repo mapping and SEO behavior

## Future site onboarding
For every new site:
1. create a site-specific env file outside version control
2. add a site workflow reference
3. confirm repo/folder mapping
4. confirm Broseph tools/routes live
5. confirm GitPress render defaults
6. confirm SEO plugin behavior
7. save important verification notes
