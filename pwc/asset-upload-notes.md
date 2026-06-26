# Imagery Notes — PWC City Hub Pages

All `<img>` tags use **absolute** PWC media-library URLs, because GitPress fragments render
inside WordPress and repo-relative paths won't resolve.

## Images already live (no action needed)

These are already on the PWC CDN and load on every page today:

| Slot | URL | Used on |
|---|---|---|
| Hero (every page) | `https://psychwellnesscenter.com/wp-content/uploads/2024/10/Psychiatrist-san-diego-CA.webp` | all 8 |
| "Adult Psychiatry" section media | `https://psychwellnesscenter.com/wp-content/uploads/2024/10/Psychiatrist-Encinitas-CA.webp` | all 8 |

So every page already carries real San Diego / North County imagery.

## Two San Diego accent images to add (optional enhancement)

Two more San Diego accents are referenced by their **future** URLs. Until you upload them they
degrade gracefully to a branded blue→green gradient panel **with a caption** (they do not look
broken). Upload images to these exact paths (or change the `src` in the 8 HTML files) and they
appear automatically.

| Filename / target URL | Where it appears | Suggested subject | Recommended size |
|---|---|---|---|
| `san-diego-coast-wellness.webp` → `.../wp-content/uploads/2026/06/san-diego-coast-wellness.webp` | "Anxiety & Panic" section media (all 8) | Calm North County San Diego coastline / La Jolla cove, soft daylight, no text, no logos | ~1200×900, landscape, <250 KB |
| `san-diego-skyline-wellness.webp` → `.../wp-content/uploads/2026/06/san-diego-skyline-wellness.webp` | "Serving {City} & Nearby Communities" band (all 8) | San Diego skyline / bay with palms, bright and calm | ~1200×900, landscape, <250 KB |

### How to add them
1. Source two licensed San Diego photos (or ask Claude to generate them — note that AI image
   generation uses Higgsfield credits).
2. In WordPress: **Media → Add New**, upload each file. Keep the filenames above, or note the
   real URLs WordPress assigns.
3. If the URLs differ from the table above, update the `src` in all 8 `pwc/psychiatrist-*-ca.html`
   files (search for `san-diego-coast-wellness` and `san-diego-skyline-wellness`).
4. Re-fire the GitPress webhook / purge GitPress cache so the updated fragments are served.

> Optional: working copies of these two images can also be committed to `pwc/assets/images/`
> as the source of truth, but the **live** pages must reference the WordPress media URL.
