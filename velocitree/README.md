# Velocitree Solutions

A two-page website for GitPress Managed, based on the supplied capability card, business-card/website mockup and brand artwork.

## Files

| File | Purpose |
| --- | --- |
| `header.html` | Shared navigation and brand lockup; loads packaged Manrope fonts |
| `home.html` | Home body partial, including the hero, six capabilities, five audiences and company perspective |
| `contact.html` | Contact body partial with Ed Martinez’s email, phone and native FAQs |
| `hero.html` | Reusable hero source, copied into `home.html` by the preview builder |
| `footer.html` | Shared footer |
| `preview/velocitree-home-preview.html` | Full-doctype home preview |
| `preview/velocitree-contact-preview.html` | Full-doctype contact preview |
| `assets/js/shared.js` | Optional navigation, active-link and copyright enhancements |
| `reference-notes.md` | Transcription and factual source notes |

Open either preview HTML file directly in a browser. Both include the complete shell and work from disk; navigation links are rewritten to the local preview files. Preview images, fonts and scripts are local. No build system or JavaScript framework is required.

After editing any fragment, regenerate both previews and synchronize the hero:

```powershell
python velocitree/tools/build_preview.py
python velocitree/tools/check_site.py
```

Edit `hero.html` for hero changes; the copy between `VTS:HERO` markers in `home.html` is generated. All other content in `home.html` remains editable. The preview build does not fetch or inject fragments at runtime.

## GitPress setup

Use these settings for both pages:

```json
{
  "render_mode": "gitpress_managed",
  "render_position": "replace",
  "full_width_content": false,
  "full_page_canvas": true
}
```

Set the WordPress home page to `/` and the contact page to `/contact/`. The other menu destinations are sections of the home page, not additional pages.

Home body:

```text
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="velocitree/home.html" format="html"]
```

Contact body:

```text
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="velocitree/contact.html" format="html"]
```

Global managed header and footer:

```text
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="velocitree/header.html" format="html"]
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="velocitree/footer.html" format="html"]
```

Do not configure `hero.html` as the global header or render it separately alongside `home.html`; it is already inside the home body. Do not use preview documents as GitPress sources.

Production images/fonts/capability-card links point at this repository’s raw `main` URLs. These URLs will become available after the files are committed and pushed. They can instead be replaced with permanent WordPress Media Library/CDN URLs. Fonts and icons are packaged with their OFL/MIT licenses.

For optional enhancements, enqueue `assets/js/shared.js` once through an approved WordPress shared asset mechanism after the managed shell renders. If loaded after DOM ready, it initializes immediately; dynamically replaced shells can call `VelocitreeSite.init()`. The header/footer contain no inline scripts, and all FAQs still open with JavaScript disabled. No page body initializes global navigation. The header contains no menu or toggle, so the script touches only active-link marking, expertise anchors and the footer year.

At 850px and below the header switches from `position: sticky` to `position: fixed`, with a `.vts-header-spacer` sibling holding its 74px of space in the flow. Sticky is silently cancelled by any ancestor with `overflow` or `transform` set, which mobile theme wrappers commonly apply, so fixed is the reliable choice there. There is no mobile menu: the bar is the brand plus the “Let's connect” button, which sits where a hamburger toggle would normally go, and mobile header navigation is therefore the call to action only — the footer carries the full link list on every page.

An earlier `details`/`summary` mobile menu was removed after live WordPress CSS repeatedly overrode its type scale and restored the native disclosure triangle beside the hamburger; with no `details` element left in the header there is nothing for the theme to reach. To keep the label on one line in the narrow bar, the mobile button drops the `↗` glyph and tightens to `9px 14px` padding at 14px, with `white-space: nowrap` and `!important` on the metrics theme rules target, since ID-scoped and `!important` theme selectors outrank plain class selectors. At 320px it measures 120px wide and still clears the wordmark. A green glow sits behind it. `qa_browser.py` counts the button's rendered line boxes at 320, 360, 390 and 430px with representative theme CSS injected, so a regression to two lines fails the suite.

The contact page includes the supplied raw `[fluentform id="1"]` shortcode in its inquiry section, with scoped styling for Fluent Forms fields, labels, validation and buttons. Fluent Forms controls the configured fields and submissions on WordPress. The standalone preview replaces the shortcode with a clearly labeled form area; it does not simulate fields or submission. The “Email Ed” call to action scrolls to that form (`#inquiry`) rather than opening a `mailto:`, so it works for visitors with no desktop mail client configured; the phone number and the plain `mailto:ed@velocitreegroup.com` address links remain available for visitors who do have one. Verify form 1 renders and delivers an actual test inquiry on the target WordPress site after deployment.

Set the following SEO metadata in WordPress/Yoast (previews carry the same titles/descriptions solely for review):

| Page | Title | Description |
| --- | --- | --- |
| Home | Velocitree Solutions \| Strategic Advisory for the UVM Industry | Practical experience and strategic insight for growth in Utility Vegetation Management. From the Jobsite to the Boardroom. |
| Contact | Contact Ed Martinez \| Velocitree Solutions | Start with your business challenge. Connect with Ed Martinez at Velocitree Solutions for strategic advisory in the UVM industry. |

## Visual and content decisions

The charcoal, green and copper palette, light audience section, tree-and-gear emblem and sunset arborist composition follow the supplied artwork. CSS is scoped and the native HTML approach follows `GITPRESS_WEBSITE_STRUCTURE.md`. Manrope supplies the bold geometric typography. Phosphor Regular SVGs provide a consistent icon family. The header’s compact horizontal lockup uses a CSS viewport onto the existing emblem plus typeset lettering.

The six capability descriptions, five audiences, contact information and positioning come from the reference folder. No years in business, results, certifications, address or response-time promise have been invented. The supplied UAA, TCIA and ISA affiliation marks appear on the home page under the “Proud industry affiliations” heading, following their business-card placement. They are presented as affiliations, not certifications.

The latest September 9 redesign follows the client's hero reference: uppercase two-line headline, the Jobsite-to-Boardroom tagline directly beneath it, the full supplied introduction, What We Do as the first CTA and Let's Connect as the outlined second CTA. Six centered service panels include icons and short descriptions. Below them, the page uses a light background, a prominent brand introduction and photo-led audience cards. All six detailed capabilities start expanded. A forest-green experience section replaces the generic process steps with the capability card's actual advisor specialties and Ed Martinez's title. Navigation labels, routes and anchor IDs remain stable. Mobile layouts reflow without horizontal scrolling, and interaction feedback respects reduced motion.

See `content-audit.md` for a section-by-section comparison against the capability card, including restored content.

Displayed images ship as WebP derivatives generated from the supplied originals, which stay in the repository. The header and footer emblem comes from `vts logo only 9.11.webp`: the pure-black field is flood-filled from the edges to transparency (so dark pixels inside the artwork survive), trimmed to the content box, and written at 52x42, 104x84 and 156x126 for 1x/2x/3x `srcset`. Because the field is transparent and pre-trimmed, the emblem no longer needs the radial mask and negative-offset crop the previous square logo required. The hero comes from `VTS climber with logo in sun.webp` at 640, 960, 1280 and 1672 wide (q86 below 1280, q82 at and above). Phones get art direction instead: at 480px and under, a `<picture>` source serves `vts-hero-mobile.webp`, a 640x941 portrait crop taken at the same 85% horizontal position the mobile `object-position` used, with `object-position` reset to centre for that source. The mobile box is 100vw by ~690px, so `object-fit: cover` scales by height and only ~532 source pixels are ever visible; the crop carries exactly those pixels at 86KB instead of 184KB for the full frame, at identical rendered sharpness. On phones the copy is anchored to the bottom of an 840px hero rather than the top. The climber's head and torso sit at 24-55% of the frame and the source puts the head only 24% down, so no crop or `object-position` can push the subject below a top-aligned copy block; moving the copy is the only way to clear it. The mobile gradient is flipped to match, staying light over the subject and reaching full strength by 66%, which measures 16:1 or better against white text across the whole copy band. Above 480px the width ladder applies with `sizes="(max-width: 767px) 1226px, 100vw"`, the 1226px accounting for that same cover-crop rather than the element width. A local Lighthouse mobile audit of the earlier build scored 68 performance, 100 accessibility and 96 best practices, with 0 ms total blocking time and 0.001 layout shift; simulated LCP was 6.6 seconds, so production hosting, caching and further font optimization still need separate verification. The standalone previews intentionally remain noindex.

Image preparation used the built-in image-generation tool:

- `assets/images/uvm-hero.png`: edited `reference/new teams bkgrd.png` to remove baked-in lettering, logos and the ghosted watermark while retaining the arborist, tree, forest and sunset. Prompt: “Remove ALL logos, all text, the giant ghosted tree-and-gear watermark, and the logo/words on the left. Preserve the realistic arborist on the RIGHT with safety equipment, tree trunk, ropes and chainsaw, the forest valley and warm copper sunset composition. Seamlessly inpaint the removed graphics as natural sunset sky and forest landscape. Keep left half dark and spacious for later HTML text overlay; right image rich warm copper/amber light, realistic and detailed. Output only the clean full-bleed landscape background image, approximately 16:9, no text, no graphics, no borders. Do not add any objects or people.”
- `assets/images/field-planning.png`: generated illustrative image, not a photograph of Velocitree staff or a claimed project. Prompt: “Photorealistic editorial website image for a utility vegetation management business advisory company. Two experienced field professionals seen mostly from behind / side, wearing dark forest-green work shirts, appropriate safety vests and white forestry hard hats, studying a simple paper site map spread over the hood of a white utility work truck. A mature conifer forest and utility poles in the distant background, no overhead electrical conductors close to workers. Candid practical field planning and experienced leadership, not stock corporate posing. Copper-gold late-afternoon natural light, restrained saturation, dark green shadows, believable equipment and anatomy. Wide medium shot from slightly above map height, crop waist up; professionals and paper map are the focal point, good 4:3-ish landscape composition, no logos, no branding, no visible legible text, no graphics.”
- `assets/images/velocitree-logo.png`: exact copy of the supplied `reference/VTS Capability Card.png`; CSS displays its emblem. This preserves the supplied branding while avoiding the 19 MB square logo source.

## Deployment verification

Local validation covers 7 HTML files for GitPress boundaries, IDs, asset references and navigation; 42 Chrome browser checks cover both pages at 320, 390, 768, 1024 and 1440px, with and without JavaScript, plus native disclosures, the pinned mobile bar, the single-line header call to action and its resilience against theme CSS overrides, responsive hero and emblem source selection by viewport and pixel ratio, contact navigation, keyboard skip links, reduced-motion rendering, service deep links and the form preview boundary. Full screenshots and `qa-report.json` are in `preview/`. Browser verification can be rerun with `python velocitree/tools/qa_browser.py` after installing the optional `playwright` Python package; it uses installed Google Chrome.

This package is prepared locally. Live WordPress rendering, GitPress sanitization/caching and form integration require the target WordPress site. After deploying, confirm the fragment version markers, exactly one header/footer, fonts and images, native FAQ behavior, mobile layout and SEO settings. Purge GitPress’s content cache if the deployed marker is stale.
