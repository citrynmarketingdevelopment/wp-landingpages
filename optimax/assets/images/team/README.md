# About page portraits

The seven 600 × 600 WebP files are used by `optimax/about-us.html`. The supplied originals in `optimax/headshots/` remain unchanged. Jaclyn Jeffries keeps her existing WordPress portrait.

| WebP | Supplied original |
| --- | --- |
| david-mizrahi.webp | David Head Shot.png |
| donald-keisler.webp | Donald_Keisler_Headshot_1254x1254.png |
| marquise-romero.webp | Marquise Headshot.png |
| omied-mizrahi.webp | Omied.png |
| stephanie-padilla.webp | Stephanie Head Sho.jpeg |
| gloria-cisneros.webp | Gloria Headshot.PNG |
| michele-ballard.webp | Michelle Headshot.png |

David's supplied transparent portrait was composited over white. The other six backgrounds were replaced using the built-in image editing tool on November 3, 2026. The results were cropped to squares with approximately 6% space above the head, then resized and exported as WebP at quality 94. This matches the existing site's head-and-upper-torso presentation. David's crop adds 60 source pixels above the head to avoid clipping it.

The same image editing prompt was used separately for each of the six portraits:

> Edit this exact supplied professional portrait for the Optimax website. Change ONLY the background to seamless pure solid white (#ffffff). Preserve the photographed person exactly: identical face, facial features, skin texture, hair, expression, pose, clothing, jewelry and lighting. Do not beautify, redraw, retouch, change age, or alter facial anatomy. Keep the original subject framing and full visible hair and body; do not crop the head or introduce borders or text. Clean natural hair edges against pure white. This is a background replacement, not a new portrait.

The About page conversion preserves WordPress page ID 72331 and `/about-us/`, uses theme-wrapped GitPress rendering, and retains the native header, footer and Gravity Forms form 1. Sonny Diaz's card and link are excluded. His separate published biography, page 72697 at `/sonny-diaz/`, is outside the About partial and must be unpublished in WordPress admin; the current Broseph manifest cannot unpublish a published page.
