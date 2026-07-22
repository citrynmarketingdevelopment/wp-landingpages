# Citryn Broseph Workflow Reference

## Site profile
- site: `https://citryn.com`
- Broseph REST base: `https://citryn.com/wp-json/broseph/v1`
- repo: `citrynmarketingdevelopment/wp-landingpages`
- base path: `test-web/` for early GitPress testing; confirm task-specific path before rollout
- default render mode: `full_canvas` for standalone GitPress canvas tests unless explicitly told otherwise
- default render position: `replace`
- SEO plugin: verify live before SEO writes

## Verified behavior
- feature-validation site for GitPress page creation, Divi template cloning, forms, mail testing, and updates
- default new AI-generated pages should use GitPress page creation
- Divi template mode should be used only when explicitly requested
- existing Divi code-module insertion should be used only for existing Divi pages when explicitly requested
- never auto-publish

## Important gotchas
- refresh `/broseph/v1/tools` before mutating actions
- do not assume form submission is supported just because form discovery works
- do not assume updates are enabled until tools and update checks confirm it
