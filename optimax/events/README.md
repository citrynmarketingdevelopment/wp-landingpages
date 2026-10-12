# Optimax Events

An Events index and reusable event landing pages, styled to match the existing Optimax pages. Production files are GitPress body partials; the existing WordPress/Divi header and footer remain responsible for the live navigation.

## View the pages

Open these standalone files in a browser, or serve the repository with `python -m http.server 8765`:

- `../preview/optimax-events-preview.html` — Events page.
- `../preview/optimax-event-mgma-2026-preview.html` — MGMA landing page.
- `../preview/optimax-event-namiwalks-kern-county-2026-preview.html` — NAMIWalks landing page.
- `../preview/optimax-home-preview.html` — existing home content with the Events menu entry.

The previews include desktop navigation, a native mobile Menu dropdown, and working links between the Events index, event pages, and home preview. Their header/footer are preview-only mockups; other navigation and contact links point to the actual Optimax site. Preview files are marked `noindex`.

## Add the next event

1. Place the event photo or graphic in this folder. Keep the original file.
2. Duplicate an object in `events.json`. Use MGMA for a conference with optional service links/gallery, or NAMIWalks for a simpler community event.
3. Set a unique `slug` beginning with `event-`, preferably including the year. Update the name, category, ISO start/end dates, human-readable date label, location, organizer link, copy, image filename and image alt text. The date label and ISO dates must agree.
4. Update the `past_*` copy for the new event. This avoids an invitation remaining on a finished event's landing page after the next rebuild. Optional fields are `note`, `topics`, and all `gallery_*` fields; remove the gallery fields together when unused.
5. Run from the repository root:

   ```powershell
   python -m pip install -r optimax/events/requirements.txt
   python optimax/events/build.py
   ```

6. Review the generated previews, then deploy the new body partial and create its WordPress page using the generated setup manifest.

`templates/event.html` is the reusable landing-page template, `templates/index.html` controls the Events index, and `templates/events.css` contains the shared styles. Change these sources rather than the generated files. CSS is embedded in every production partial so GitPress does not need an extra stylesheet or JavaScript bundle. The small single-family font imports follow the existing Optimax/GitPress convention.

Images are compressed into `assets/*.webp` without changing the supplied artwork. Production images use absolute raw GitHub URLs; preview images use local copies. Commit the assets alongside the pages so the production URLs resolve. The originals are preserved.

## Dates and content

As of October 12, 2026, NAMIWalks is upcoming and MGMA is recent:

- [MGMA Annual Conference](https://www.mgma.com/annual-conference): September 27–30, 2026, San Antonio, TX. Booth #433 comes from the supplied `MGMA2.jpg` graphic.
- [NAMIWalks Kern County](https://www.namiwalks.org/kerncounty): October 17, 2026. The page uses the requested “Come See Us at NAMIWalks Kern County” message and the supplied sponsor graphic. No Optimax meeting time, booth number, or other unconfirmed attendance details are added.

The builder sorts upcoming events by start date and recent events by end date, and uses past-event copy when the end date has passed. Multi-day events stay in the upcoming list through their last day and show “Happening now” on their landing page. If there are no upcoming events, the index shows a contact invitation instead of an empty list.

**These are static pages. Rebuild when dates pass and deploy the updated partials to refresh the event status.** Nothing automatically changes on the live site at midnight. The builder uses the America/Los_Angeles calendar date by default. For a repeatable preview:

```powershell
python optimax/events/build.py --today 2026-10-12
```

## WordPress and the live menu

`wordpress-setup.json` lists the page titles, slugs, descriptions, GitPress shortcodes, theme-wrapped settings, and the intended Events menu entry. It is a setup reference, not an automatic WordPress importer.

| Page | Body source | WordPress URL |
| --- | --- | --- |
| Events | `optimax/events.html` | `/events/` |
| MGMA Annual Conference | `optimax/event-mgma-2026.html` | `/event-mgma-2026/` |
| NAMIWalks Kern County | `optimax/event-namiwalks-kern-county-2026.html` | `/event-namiwalks-kern-county-2026/` |

For each WordPress page, use the corresponding shortcode from the manifest with `theme_wrapped`, `replace`, `full_width_content: true`, and `full_page_canvas: false`. Set the title and meta description in WordPress/Yoast rather than inserting a second document head into the body partial.

Add **Events** → `/events/` after **Resources** in the existing primary WordPress menu and ensure the Divi mobile menu uses that menu too. The two event pages are linked from the Events page; they do not need top-level menu entries. The repository has no Optimax production header source to modify; adding Events in a preview does not change the native live menu.

The builder generates source and previews; deployment uses the shared Broseph client described in `../../broseph/CONNECTIONS.md`. Create the three WordPress pages with the generated shortcodes and publish only when requested. Native Divi menu changes remain separate because the current Broseph API has no menu endpoint. After deployment, verify the build marker, images, event links, contact links, and mobile layout in WordPress, using the site's actual GitPress cache controls when needed.
