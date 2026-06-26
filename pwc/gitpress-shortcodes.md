# GitPress Shortcodes — PWC City Hub Pages

Each page is a GitPress **body partial** (no `<head>/<body>`; SEO set in WordPress). Wire each
WordPress page to its GitHub file with the shortcode below, then set the render mode at the
GitPress page level (not inside the shortcode — per `GITPRESS_WEBSITE_STRUCTURE.md` §4).

- **Repo:** `citrynmarketingdevelopment/wp-landingpages` · branch `main`
- **Render mode (all 8):** `theme_wrapped` — keeps PWC's existing WordPress/Divi header,
  menu, and footer (the fragments are body content only). Recommended page settings:

```json
{
  "render_mode": "theme_wrapped",
  "render_position": "replace",
  "full_width_content": true,
  "full_page_canvas": false
}
```

## Pages

| Live slug | GitHub file | Shortcode |
|---|---|---|
| `/psychiatrist-carlsbad-ca/` | `pwc/psychiatrist-carlsbad-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-carlsbad-ca.html" format="html"]` |
| `/psychiatrist-la-jolla-ca/` | `pwc/psychiatrist-la-jolla-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-la-jolla-ca.html" format="html"]` |
| `/psychiatrist-del-mar-ca/` | `pwc/psychiatrist-del-mar-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-del-mar-ca.html" format="html"]` |
| `/psychiatrist-carmel-valley-ca/` | `pwc/psychiatrist-carmel-valley-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-carmel-valley-ca.html" format="html"]` |
| `/psychiatrist-solana-beach-ca/` | `pwc/psychiatrist-solana-beach-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-solana-beach-ca.html" format="html"]` |
| `/psychiatrist-san-marcos-ca/` | `pwc/psychiatrist-san-marcos-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-san-marcos-ca.html" format="html"]` |
| `/psychiatrist-oceanside-ca/` | `pwc/psychiatrist-oceanside-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-oceanside-ca.html" format="html"]` |
| `/psychiatrist-escondido-ca/` | `pwc/psychiatrist-escondido-ca.html` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="pwc/psychiatrist-escondido-ca.html" format="html"]` |

## After wiring each page

1. Set Yoast fields from `yoast-new-location-pages.md`.
2. Confirm the GitPress webhook fired (or purge GitPress cache) so the new fragment is served
   — clearing only the WP page cache is not enough (§13). Each fragment carries a
   `<!-- webhook retrigger 2026-06-26 -->` marker; bump it on future edits and grep the live
   page source to confirm the latest version is live before debugging CSS (§8).
3. Verify on staging: managed header/footer appear once, headings stay PWC slate-blue
   (`#39657e`), buttons stay green (`#799d4c`), the FAQ accordion toggles, and the San Diego
   hero image loads. Re-check colors/spacing on the live Divi page, not just standalone.
