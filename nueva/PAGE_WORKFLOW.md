# Neuva CoolPeel and Face GitPress pages

Prepared October 28, 2026 from the supplied CoolPeel development brief and the existing Neuva service pages. The original brief's October 26 target is already past; no scheduled publish was created.

## Review links

| Page | WordPress ID | Review URL | Current state |
| --- | --- | --- | --- |
| CoolPeel | 274296 | https://neuvaaesthetics.com/coolpeel/ | Published GitPress page |
| Face review | 274297 | https://neuvaaesthetics.com/?page_id=274297&preview=true | Draft; temporary slug `face-gitpress-preview` |
| Existing Face | 273470 | https://neuvaaesthetics.com/face/ | Published; converted to GitPress in place |

WordPress preview links require an authorized admin login. Static review copies are in `previews/`; they have a simplified local review shell. Only actual WordPress previews can verify the native Divi header/footer and GitPress sanitization.

## Source and rendering

- `service-pages/coolpeel.html` and `service-pages/face.html` are the deployed body partials. They contain no document wrapper, navigation, footer, or page JavaScript.
- Both published pages use `theme_wrapped`, `replace`, full-width content enabled, and full-page canvas disabled. The existing WordPress/Divi shell remains responsible for navigation and the footer.
- `assets/service-pages.css` is the canonical shared styling reference. The same CSS is embedded into each partial for independent GitPress rendering. Keep all three copies synchronized when editing.
- The design follows Neuva's service-page cream/lavender palette, Cormorant Garamond headings, Montserrat copy, Face banner, and decorative rose image. The accent is darker for readable links/buttons. No new third-party or device imagery was introduced.
- The Face source preserves the original intro and ten non-CoolPeel treatment sections. The eleventh treatment is the brief's shorter CoolPeel summary, corrected device name, award line, and `/coolpeel/` link. Its accordions use native `details`/`summary` and require no scripts.
- At the user's request, CoolPeel's award, booking, address, and results disclaimer sit inside the white content panel next to the flower. The two equal columns have the same 48px desktop / 28px mobile gap as Face.
- GitPress's full-width reset forces `section:first-child` top padding to zero with `!important`. A higher-specificity rule scoped to `#main-content .neuva-service .nv-hero` restores 64px desktop / 46px mobile padding with targeted `!important`, following `GITPRESS_WEBSITE_STRUCTURE.md`. Use a descendant selector here: live GitPress converts the direct-child `>` character inside CSS into `&gt;`, invalidating that rule. This was caught in actual computed-style QA and corrected in revision 7.
- Actual WordPress browser inspection found the native Divi header spacing intact and identified the hero reset as the cause. Its separate `100vw` content wrapper also introduced a small desktop scrollbar-width overflow. A rule scoped to these two WordPress page IDs now uses the existing full-width container at `width: 100%` with zero breakout margins.
- Both pages end with the requested original Promos layout: the transparent `Promos.webp` image at its native 700×650 aspect ratio, the original -85px image margin inside a column with 20px top padding, a white panel, two desktop columns, Monthly label, 64px Montserrat heading, original 13px Open Sans copy, and gold View Details link. The net image-element overlap is 65px, matching the existing page's geometry. The columns stack on tablet/mobile, with a 44px phone heading. This is a general promotions link, not a CoolPeel special or price.
- The brief's damaged text encoding was normalized where the intended spelling was clear: CoolPeel®, Bakersfield, off, confirm, and punctuation. No new treatment claims, timing, session counts, or prices were added.
- `coolpeel-seo.json` holds the exact supplied SEO title and description. Both are saved and read back in Yoast. They exceed the plugin's generic length suggestions; the supplied wording was retained.

## Connection

Use `node broseph/cli.mjs doctor nueva`. `broseph.json` is the public client mapping. `.env.broseph` holds the existing site-specific secret and must remain ignored. Never use another site's credentials.

Broseph's creation route currently omits the full-width setting even when requested. Both new drafts were corrected through the supported conversion endpoint and read back with `full_width_content: true`. Draft-setting backups are IDs 274298 and 274300. No plugin code was changed.

Local `.broseph/` records include original pages, creation plans, resulting IDs, verified settings/SEO, and launch payloads/results. They are ignored by Git. Do not recreate the pages if a later step fails.

At initial publication, image attachments occupied `/coolpeel/` and `/coolpeel-2/`, so WordPress assigned `/coolpeel-3/`. The user initially approved `/coolpeel-laser-resurfacing/`, which was set through Broseph. A subsequent separate WordPress edit freed and assigned `/coolpeel/` to the service page. The user then explicitly confirmed keeping that now-working original URL. The final canonical and Face treatment link use `/coolpeel/`. No media attachment or image file was modified by this task's tools.

The old GitPress cache continued serving revision 3 after the revision 4 padding fix was pushed. The current body partials were moved into the structure guide's `service-pages/` folder and their page-level source bindings updated through the supported conversion tool. Both current shortcodes use `branch="main"` and the plugin-supported `ttl="60"`. The fresh bindings served revision 5 immediately. There is no Broseph cache-purge tool, and no unadvertised purge route was invoked. Existing GitHub credentials did not have webhook-metadata access; no webhook settings or credentials were changed.

There is also a separate full-page Cloudflare/host cache. It kept the canonical URLs on revision 7 after GitPress had revision 8. A review query URL confirmed the origin's latest source; resaving each page's unchanged final slug through the supported `update_seo_meta` tool triggered the site's normal page-cache invalidation. Both canonical URLs then returned revision 8 with `CF-Cache-Status: MISS`, and Face's CoolPeel link resolved correctly. No SEO title or description was changed by that save. For future updates, verify both the GitPress source marker and the canonical URL, rather than relying on a cache-busting preview alone.

## Deployment and remaining rollout

After reviewing the drafts, the user explicitly authorized publishing both pages and pushing the changes on October 28, 2026. No message was sent to Caesar.

Completed:

1. Published CoolPeel ID 274296 and saved the approved final slug.
2. Compared Face ID 273470 with the original source and SEO, then converted it in place, preserving ID, title, URL, and published status. The original Divi backup is ID 274305. The separate Face review draft remains unpublished.
3. Updated both source bindings for the current revision, with further snapshots ID 274307 (CoolPeel) and ID 274308 (Face).
4. Confirmed both published page-level settings, the Face treatment link, and the CoolPeel canonical URL. Both URLs return HTTP 200, with one native header/footer and one Promos section each. Revision 8 uses the user-confirmed final `/coolpeel/` URL.

Supporting changes in `rollout/README.md` are still prepared, not applied. Native WordPress menus and the native Divi footer need their actual editors; the current Broseph tools do not support those changes. Homepage, gallery, and contact snippets now target the approved CoolPeel URL.

The existing gallery video URL returned HTTP 206 with `video/mp4` and an MP4 container header. Playback has not been visually verified. Keep it only if it plays; remove the video module if it is blank. Keep “Individual results vary.” with the gallery.

## Validation performed

- Verified signed Neuva identity, GitPress availability, and current tool permissions.
- Verified reviewed page sources matched GitHub bytes before draft creation.
- Read both drafts back and confirmed their status, shortcode, render mode, and full-width setting.
- Read CoolPeel's exact Yoast title and description back successfully.
- Compared all ten non-CoolPeel treatment bodies with the original WordPress content; all matched.
- Checked one main/one H1, unique IDs, no nested document shells or script dependency, correct treatment/award/device spelling, no CoolPeel price, and clean Git whitespace.
- Verified the original Face source and SEO before conversion; retained its ID/URL/status and created a recoverable Divi backup before changing it.
- Public static-preview browser QA passed at 1440px, 390px, and 320px: images/text appeared, CTA labels were unclipped, no horizontal overflow was found, and CoolPeel and Dermal Fillers accordions opened. A second check of the updated Promos sections confirmed desktop columns, correct image dimensions/loading, and mobile stacking without clipping or overflow. The preview service injects its own first base element, so the standalone review copies now use absolute Neuva links; deployed WordPress partial links remain root-relative.
- Actual public WordPress browser QA confirmed the flower gap is 48px, award/booking copy is inside the white box, Promos renders, and Face's native accordions work. Final computed hero top padding is 64px desktop / 46px at 390px mobile on both pages, with no horizontal overflow. The native Divi header/footer remain intact.
- Final canonical-URL checks confirmed revision 8 on `/face/` and `/coolpeel/`, with the corrected `/coolpeel/` treatment link and preserved CoolPeel SEO copy.

Initial draft previews required admin login. The pages are now public, and final visual checks can use the actual WordPress URLs rather than only static previews.
