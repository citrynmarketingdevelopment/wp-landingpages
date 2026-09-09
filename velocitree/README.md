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

For optional enhancements, enqueue `assets/js/shared.js` once through an approved WordPress shared asset mechanism after the managed shell renders. If loaded after DOM ready, it initializes immediately; dynamically replaced shells can call `VelocitreeSite.init()`. The header/footer contain no inline scripts, and the menu and all FAQs still open with JavaScript disabled. No page body initializes global navigation. The custom native mobile-menu hooks intentionally avoid the legacy GitPress hamburger IDs.

The contact page is functional through `mailto:velocitreesolutions@outlook.com` and `tel:+19095618661`. No inquiry form ID or submission endpoint was supplied, so it has no simulated submission or invented Fluent Forms ID. To add a WordPress form later, embed the actual raw `[fluentform id="..."]` shortcode in the contact body and let Fluent Forms handle submissions.

Set the following SEO metadata in WordPress/Yoast (previews carry the same titles/descriptions solely for review):

| Page | Title | Description |
| --- | --- | --- |
| Home | Velocitree Solutions \| Strategic Advisory for the UVM Industry | Practical experience and strategic insight for growth in Utility Vegetation Management. From the Jobsite to the Boardroom. |
| Contact | Contact Ed Martinez \| Velocitree Solutions | Start with your business challenge. Connect with Ed Martinez at Velocitree Solutions for strategic advisory in the UVM industry. |

## Visual and content decisions

The charcoal, green and copper palette, light audience section, tree-and-gear emblem and sunset arborist composition follow the supplied artwork. CSS is scoped and the native HTML approach follows `GITPRESS_WEBSITE_STRUCTURE.md`. Manrope supplies the bold geometric typography. Phosphor Regular SVGs provide a consistent icon family. The header’s compact horizontal lockup uses a CSS viewport onto the existing emblem plus typeset lettering.

The six capability descriptions, five audiences, contact information and positioning come from the reference folder. No years in business, results, certifications, address or response-time promise have been invented. Industry affiliation marks remain in the linked original capability/business-card materials; they are not presented as certifications.

Image preparation used the built-in image-generation tool:

- `assets/images/uvm-hero.png`: edited `reference/new teams bkgrd.png` to remove baked-in lettering, logos and the ghosted watermark while retaining the arborist, tree, forest and sunset. Prompt: “Remove ALL logos, all text, the giant ghosted tree-and-gear watermark, and the logo/words on the left. Preserve the realistic arborist on the RIGHT with safety equipment, tree trunk, ropes and chainsaw, the forest valley and warm copper sunset composition. Seamlessly inpaint the removed graphics as natural sunset sky and forest landscape. Keep left half dark and spacious for later HTML text overlay; right image rich warm copper/amber light, realistic and detailed. Output only the clean full-bleed landscape background image, approximately 16:9, no text, no graphics, no borders. Do not add any objects or people.”
- `assets/images/field-planning.png`: generated illustrative image, not a photograph of Velocitree staff or a claimed project. Prompt: “Photorealistic editorial website image for a utility vegetation management business advisory company. Two experienced field professionals seen mostly from behind / side, wearing dark forest-green work shirts, appropriate safety vests and white forestry hard hats, studying a simple paper site map spread over the hood of a white utility work truck. A mature conifer forest and utility poles in the distant background, no overhead electrical conductors close to workers. Candid practical field planning and experienced leadership, not stock corporate posing. Copper-gold late-afternoon natural light, restrained saturation, dark green shadows, believable equipment and anatomy. Wide medium shot from slightly above map height, crop waist up; professionals and paper map are the focal point, good 4:3-ish landscape composition, no logos, no branding, no visible legible text, no graphics.”
- `assets/images/velocitree-logo.png`: exact copy of the supplied `reference/VTS Capability Card.png`; CSS displays its emblem. This preserves the supplied branding while avoiding the 19 MB square logo source.

## Deployment verification

Local validation passed: 7 HTML files checked for GitPress boundaries, IDs, asset references and navigation; 28 Chrome browser checks covered both pages at 320, 390, 768, 1024 and 1440px, with and without JavaScript, plus native menus/disclosures, Escape/outside-click closing, contact navigation, keyboard skip links and reduced-motion rendering. Full screenshots and `qa-report.json` are in `preview/`. Browser verification can be rerun with `python velocitree/tools/qa_browser.py` after installing the optional `playwright` Python package; it uses installed Google Chrome.

This package is prepared locally. Live WordPress rendering, GitPress sanitization/caching and form integration require the target WordPress site. After deploying, confirm the fragment version markers, exactly one header/footer, fonts and images, native menu/FAQ behavior, mobile layout and SEO settings. Purge GitPress’s content cache if the deployed marker is stale.
