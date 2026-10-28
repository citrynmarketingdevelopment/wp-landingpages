# Neuva CoolPeel and Face GitPress pages

Prepared October 28, 2026 from the supplied CoolPeel development brief and the existing Neuva service pages. The original brief's October 26 target is already past; no scheduled publish was created.

## Review links

| Page | WordPress ID | Review URL | Current state |
| --- | --- | --- | --- |
| CoolPeel | 274296 | https://neuvaaesthetics.com/?page_id=274296&preview=true | Draft; reserved slug `coolpeel` |
| Face review | 274297 | https://neuvaaesthetics.com/?page_id=274297&preview=true | Draft; temporary slug `face-gitpress-preview` |
| Existing Face | 273470 | https://neuvaaesthetics.com/face/ | Published Divi original; unchanged |

WordPress preview links require an authorized admin login. Static review copies are in `previews/`; they have a simplified local review shell. Only actual WordPress previews can verify the native Divi header/footer and GitPress sanitization.

## Source and rendering

- `coolpeel.html` and `face.html` are body partials. They contain no document wrapper, navigation, footer, or page JavaScript.
- Both drafts use `theme_wrapped`, `replace`, full-width content enabled, and full-page canvas disabled. The existing WordPress/Divi shell remains responsible for navigation and the footer.
- `assets/service-pages.css` is the canonical shared styling reference. The same CSS is embedded into each partial for independent GitPress rendering. Keep all three copies synchronized when editing.
- The design follows Neuva's service-page cream/lavender palette, Cormorant Garamond headings, Montserrat copy, Face banner, and decorative rose image. The accent is darker for readable links/buttons. No new third-party or device imagery was introduced.
- The Face source preserves the original intro and ten non-CoolPeel treatment sections. The eleventh treatment is the brief's shorter CoolPeel summary, corrected device name, award line, and `/coolpeel/` link. Its accordions use native `details`/`summary` and require no scripts.
- Both pages end with the requested original Promos layout: the transparent `Promos.webp` image at its native 700×650 aspect ratio, the original -85px image margin inside a column with 20px top padding, a white panel, two desktop columns, Monthly label, 64px Montserrat heading, original 13px Open Sans copy, and gold View Details link. The net image-element overlap is 65px, matching the existing page's geometry. The columns stack on tablet/mobile, with a 44px phone heading. This is a general promotions link, not a CoolPeel special or price.
- The brief's damaged text encoding was normalized where the intended spelling was clear: CoolPeel®, Bakersfield, off, confirm, and punctuation. No new treatment claims, timing, session counts, or prices were added.
- `coolpeel-seo.json` holds the exact supplied SEO title and description. Both are saved and read back in Yoast. They exceed the plugin's generic length suggestions; the supplied wording was retained.

## Connection

Use `node broseph/cli.mjs doctor nueva`. `broseph.json` is the public client mapping. `.env.broseph` holds the existing site-specific secret and must remain ignored. Never use another site's credentials.

Broseph's creation route currently omits the full-width setting even when requested. Both new drafts were corrected through the supported conversion endpoint and read back with `full_width_content: true`. Draft-setting backups are IDs 274298 and 274300. No plugin code was changed.

Local `.broseph/` records include original pages, creation plans, resulting draft IDs, verified settings/SEO, and `inputs/face-convert-after-approval.json`. They are ignored by Git. Do not recreate the drafts if a later step fails.

## Approval and rollout

The supplied brief asks for preview approval before publishing. No page was published, no live content was edited, and no message was sent to Caesar.

After approval:

1. Review both actual WordPress drafts at desktop and mobile widths. Confirm the native header/footer render once, images load, CTA text is readable, and Face accordions open by mouse and keyboard. Confirm the source revision marker matches the GitHub source.
2. Publish existing CoolPeel draft ID 274296, then verify `/coolpeel/` and its rendered SEO.
3. Re-read Face ID 273470 and compare it with the saved original. Convert that original page in place using the prepared payload with `backup_first: true`, `expected_slug: face`, and `expected_status: publish`. Preserve its ID, title, URL, parent/menu identity, and existing SEO. Do not publish the separate Face review draft as a replacement.
4. Verify the actual `/face/` output, the `/coolpeel/` link, all treatment accordions, and native shell. Broseph advertises no GitPress cache-purge tool; verify the source marker rather than assuming the cache refreshed.
5. Apply the reviewed supporting changes in `rollout/README.md`. Native WordPress menus and the native Divi footer need their actual editors; the current Broseph tools do not support those changes. The homepage, gallery, and contact snippets are prepared but not applied.

The existing gallery video URL returned HTTP 206 with `video/mp4` and an MP4 container header. Playback has not been visually verified. Keep it only if it plays; remove the video module if it is blank. Keep “Individual results vary.” with the gallery.

## Validation performed

- Verified signed Neuva identity, GitPress availability, and current tool permissions.
- Verified reviewed page sources matched GitHub bytes before draft creation.
- Read both drafts back and confirmed their status, shortcode, render mode, and full-width setting.
- Read CoolPeel's exact Yoast title and description back successfully.
- Compared all ten non-CoolPeel treatment bodies with the original WordPress content; all matched.
- Checked one main/one H1, unique IDs, no nested document shells or script dependency, correct treatment/award/device spelling, no CoolPeel price, and clean Git whitespace.
- Confirmed the original Face page remains published, unconverted, and unchanged since its original modified date.
- Public static-preview browser QA passed at 1440px, 390px, and 320px: images/text appeared, CTA labels were unclipped, no horizontal overflow was found, and CoolPeel and Dermal Fillers accordions opened. A second check of the updated Promos sections confirmed desktop columns, correct image dimensions/loading, and mobile stacking without clipping or overflow. The preview service injects its own first base element, so the standalone review copies now use absolute Neuva links; deployed WordPress partial links remain root-relative.

Native Chrome inspection stopped because Computer Use could not verify the current browser URL. Unauthenticated requests to both WordPress draft previews returned HTTP 404, as expected without an admin session. Actual WordPress visual QA remains pending review access.
