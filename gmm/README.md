# GMM website recreation

Local, reviewable homepage and organizations-page GitPress source for Genesis Medical Management. Nothing has been committed, pushed, converted in WordPress, or published by this task.

## Review

Open `preview/index.html` for the homepage or `preview/clients.html` for Our Organizations. Alternatively, serve the repository and visit `/gmm/preview/` or `/gmm/preview/clients.html`:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Rebuild the local preview after changing a partial:

```powershell
python gmm/scripts/build_preview.py
```

The builder assembles the actual header, homepage, and footer at build time. It replaces GitHub asset URLs with local paths for review and points existing WordPress routes to the real site. No runtime header/footer fetches or frameworks are needed. Preview screenshots and browser verification results are in the ignored `preview/qa/` directory.

## Direction applied

The original homepage HTML, screenshot, and updated `reference/meeting.md` are the reference material. This is a preservation-focused recreation, rather than a new brand design.

- Retained the GMM logo, orange and charcoal palette, Hind/Khand typography, stacked Create / Build / Grow hero, four operational areas, location tiles, about section, organizations section, and closing contact invitation.
- Rewrote the homepage for behavioral health **ownership**, with no consulting pitch, fabricated results, or lead-generation form.
- Restored the original desktop hero artwork and its proportions, spacing, skewed Khand headline, double orange divider, and overlaid navigation. The updated ownership copy remains. The about section uses existing behavioral health facility photography.
- Kept the original separate mobile composition: a compact, single-line Create.Build.Grow. headline, centered copy, and four stacked capability rows rather than the desktop hero artwork. Native disclosures let visitors tap a row to read more. A compact sticky header and large touch targets give the mobile layout an app-like feel.
- Mobile locations use four photo galleries grouped by organization. Large cards show each facility photo with the city and service/location name underneath. The next card peeks into view so visitors can swipe through each organization; galleries also support native keyboard scrolling without JavaScript. All 16 locations remain available. Desktop retains the full photo grid. Captions use the supplied city/service text and source-photo identifiers (Brimhall, Schirra Court, Jason's Retreat, Capistrano, IOP, and Perinatal).
- The mobile photo galleries replace the small thumbnail accordions rejected by the client. At a 390px viewport, standard card photos measure approximately 302 x 227px, with 21px city names and 16px captions. Other mobile sections retain compact spacing.
- Replaced the four old raster illustrations with consistent Tabler outline icons for revenue, growth, operations, and facilities. Their MIT license is retained in `assets/icons/LICENSE`.
- Used the supplied original `church-01.jpg` background in the closing Let's Grow Together section.
- Kept all 16 supplied location tiles. The user confirmed that VRS/DRS in the transcript means **Bakersfield Recovery Services**.
- Central Valley Surgical Specialists is absent. The supplied homepage already omitted it.
- Changed the old clients section to **Our Organizations**, removed the TPMG logo, and included Bakersfield Recovery Services and Inspire Me. No Premier Pain facility tiles were added.
- Replaced the old article feeds and resources promotion with **News coming soon**. Header/footer News links point to this homepage section, rather than sending visitors to the old articles.
- Removed Healthcare Solutions and Resources links from the prepared footer. Existing WordPress URLs for About Us, Locations, Contact Us, and legal pages are preserved.
- Used native `details`/`summary` for mobile navigation, so it remains usable when GitPress strips inline scripts. The page contains no JavaScript and never hides content pending script execution.

Design settings: `DESIGN_VARIANCE: 4`, `MOTION_INTENSITY: 2`, `VISUAL_DENSITY: 4`. Native HTML/CSS follow the existing brand rather than introducing a component framework. The light palette, three-line desktop hero, and one-line mobile hero intentionally preserve the supplied design. Buttons use dark text on brand orange for readable contrast. Buttons use a 5-7px radius, mobile disclosure groups use 8px, mobile thumbnails use 6px, and desktop photo tiles are square.

## Asset notes

Images and self-hosted fonts were downloaded from the public URLs in the supplied HTML. `assets/sources.json` records their origin. `scripts/prepare_assets.py` can retrieve them again; it needs Python, BeautifulSoup, and Pillow. Images were resized for web use while preserving the source files supplied by the user.

- **Inspire Me:** the user supplied and confirmed `https://genesismedicalmanagement.com/wp-content/uploads/2026/01/pwc-san-diego.webp` for this location. It is used in the desktop tile and mobile photo gallery, stored locally as `assets/images/location-16.webp`.
- **BRS:** the user supplied `https://genesismedicalmanagement.com/wp-content/uploads/2026/10/BRS-Final.webp`. Its transparent logo is stored as `assets/images/brs-logo.webp` and used in the organizations sections. Inspire Me's organization entry remains a readable name because no standalone logo was supplied.
- The original hero artwork is served from `assets/images/original-hero.webp`. The closing background is in `assets/images/grow-background.jpg`.

## GitPress files

| File | Purpose |
| --- | --- |
| `home.html` | Page body partial with scoped CSS, one `main`, and one H1 |
| `clients.html` | Our Organizations body partial for the existing `/clients/` route |
| `content/brs.json` | BRS excerpt, paragraph, and four programs derived from user-supplied approved copy |
| `header.html` | Prepared managed header and native mobile menu |
| `footer.html` | Prepared managed footer with updated navigation |
| `gitpress-setup.json` | Shortcodes and intended render settings; no credentials or invented page IDs |
| `preview/index.html` | Full standalone document for local review only |
| `preview/clients.html` | Local organizations-page review, linked to the homepage preview |
| `assets/` | Image/font files referenced by the partials |

Production partials use absolute raw GitHub asset URLs under `citrynmarketingdevelopment/wp-landingpages/main/gmm/`. Those URLs only become available after the reviewed files and assets are pushed. The local preview uses the local assets and does not depend on a push.

The intended render mode is `gitpress_managed`, with the header and footer configured separately in GitPress. Configuring global managed layout can affect other managed pages; inspect the site's settings and review that scope before changing them. The shared header uses `data-nav` hooks and CSS to highlight Home or Locations according to the rendered page; previews also set the current page's accessible marker at build time.

GMM currently has no `broseph.json` or verified local credentials. Follow `../broseph/CONNECTIONS.md` to establish its own connection. Do not borrow another site's connection. This setup file is not a Broseph CLI draft plan.

Once connected, inspect the existing homepage and live tool manifest, prepare a reviewable WordPress draft, and verify that GitHub bytes match the reviewed local source. For an eventual in-place conversion, use the advertised conversion tool with a backup, the inspected expected slug/status, and preserve the original homepage ID, permalink, title, and SEO metadata. Publishing is a separate action. Do not deploy the preview document.

The meeting asks for brochure content rather than an SEO or acquisition project. Existing metadata should be preserved on conversion. No SEO campaign, new page routes, fabricated timeline dates, form submissions, or analytics changes are part of this build.

## Scope still on the existing WordPress site

The homepage, organizations page, and proposed shell are prepared here. The live site has not changed. The existing About Us introduction, the old news archive, and any native WordPress menu changes still need their own reviewed updates. The future behavioral health growth timeline remains deferred as requested in the meeting notes.

## Our Organizations page

`clients.html` recreates `reference/Our Clients _ Genesis Medical Management.html` while following the meeting's ownership and behavioral health direction. It keeps the existing `/clients/` route for eventual conversion.

- Replaces Premier Pain Management with Bakersfield Recovery Services, positioned after Psychiatric Wellness Center.
- Uses the supplied BRS logo and a new excerpt and paragraph summarized from the user's approved website verbiage. `content/brs.json` records this copy separately for reuse; `clients.html` contains the rendered text and should also be updated if that JSON copy changes.
- Includes Jason's Retreat (men's residential), Capistrano (women's residential), Lincoln Street (perinatal residential), and IOP (intensive outpatient).
- Removes Central Valley Surgical Specialists and the old consulting testimonial.
- Retains Aspire and Psychiatric Wellness Center, with concise descriptions based on the supplied reference. Moves TPMG below them into a supporting healthcare-development section; omits the old time-sensitive portfolio statistics.
- Preserves the original clients hero artwork, shared GMM header/footer, and closing background. BRS uses the same white logo-and-text profile layout as Aspire and PWC. Mobile uses uniform white cards on a pale gray background, with native disclosures and short excerpts. Website buttons remain visible outside the collapsed descriptions. No JavaScript is needed.
- BRS's Visit Website button links to the user-confirmed `https://bakersfieldrecoveryservices.com/`. Aspire and PWC use the same button styling and their existing website destinations.
- Both previews link locally between Home and Locations. Organization website links point to their actual sites; TPMG has no invented external destination.

The BRS excerpt is: “Residential and intensive outpatient substance use treatment focused on personal growth, accountability, and long-term recovery.”

The clients-page build marker is `gmm-clients-2026-10-22-r2`. Browser checks covered 320, 375, 390, 430, 768, 980, 1024, and 1440px, visible image decoding, native mobile disclosures with JavaScript disabled, buttons visible while profiles are collapsed, the four BRS programs, and local navigation between pages. Live WordPress verification remains pending connection and deployment.

## Verification

Browser review checks desktop at 1440px and responsive widths of 320, 390, 768, and 1024px. Verify local fonts and images, one H1 and one main region, 16 tiles, valid fragment links, native mobile navigation with JavaScript disabled, reduced-motion behavior, and no horizontal overflow.

After actual WordPress deployment, verify the build marker `gmm-home-2026-10-22-r5`, GitPress sanitization, single header/footer output, mobile navigation, capability disclosures, native location galleries, images/fonts, links, and cache refresh on the real page. Local preview results do not establish live WordPress compatibility. The mobile galleries were checked at 320, 375, 390, 430, 768, and 980px, including keyboard scrolling with JavaScript disabled, all 16 locations, photo decoding, and no horizontal page overflow.
