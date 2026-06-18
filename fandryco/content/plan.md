# Fandry & Co. — Glassmorphism Dark-Green Website Build

## Context

`fandryco/` (inside the `wp-landingpages` repo, currently an untracked folder) contains six **empty** HTML stubs — `home.html`, `services.html`, `about.html`, `contact.html`, `header.html`, `footer.html` — plus a `content/` folder with `homepage-content.md` and `about-content.md` providing the real copy. The client (Fandry & Co. / "FCo") is a healthcare + business-development consulting firm serving private-practice medical groups nationwide. They want all four pages fully designed in HTML with internal `<style>` CSS, a shared header/footer, and a **glassmorphism, dark-green + black, glowing, animated, modern "consulting tech"** aesthetic.

The UI/UX Pro Max skill confirmed the direction: **"Liquid Glass" style + Storytelling/Feature-Rich pattern, CTA above fold**. We adapt its palette to the requested dark-green/black brand.

**Deliverables (written to `C:\Users\citry\OneDrive\Desktop\wp-landingpages\fandryco\`):**
1. `design.md` — created **first**, before any page code (explicit client requirement).
2. `header.html`, `footer.html` — shared partials (markup + own `<style>`).
3. `home.html`, `services.html`, `about.html`, `contact.html` — full pages.

> Note: I'm operating from a git worktree, but `fandryco/` lives in the main working tree and is untracked. All page files are written with absolute paths into `fandryco/` (where the stubs + content already are). This is intentional and matches where the client set the project up.

## Decisions (confirmed with user)
- **Header/footer wiring:** JS `fetch()` include — each page has `<div id="site-header">`/`<div id="site-footer">` placeholders and a small inline script that injects the partials and (re)wires nav behavior. Requires serving over http/WordPress (not `file://`).
- **Imagery:** Mix — photo hero backgrounds (Unsplash hotlinks) under a dark-green glass overlay, plus pure CSS/SVG glow orbs, glass panels, and line-art motifs for inner sections/cards.
- **Contact form:** Insert the literal WordPress shortcode `[fluentform id="3"]` inside a styled glass panel, and ship CSS targeting FluentForms classes (`.fluentform`, `.ff-el-input--content`, `.ff-btn`, etc.) so the rendered form matches the theme.
- **Logo:** No asset exists → use a glass "FCo" monogram tile (with glow) + "FANDRY & CO." wordmark; built to be swapped for a real logo later.

## Design System (to be captured in `design.md`)

**Palette (CSS custom properties, defined in `:root` of every file):**
- Backgrounds: `--ink:#050806` (near-black, green-tinted), `--bg-2:#0A1410`, `--bg-3:#08110D`
- Greens: `--green-900:#0B3D2E`, `--green-700:#0F6B43`, `--green-500:#16A86B`, `--green-400:#2BD17E`
- Glow/accent: `--glow:#34E89E`, `--mint:#7CFFD4`; CTA gradient `linear-gradient(135deg,#34E89E,#0F9B6C)`
- Glass: `--glass:rgba(255,255,255,.05)` blended with `rgba(18,80,55,.18)`; border `--glass-bd:rgba(124,255,212,.16)`
- Text: `--fg:#EAF6EF`, `--muted:#9DB5AA`, `--muted-2:#6E867B`
- Effects tokens: `--blur:18px`, `--radius:20px`, glow shadow `0 0 40px rgba(52,232,158,.25)`

**Typography (Google Fonts):** Headings **Space Grotesk** (geometric, techy-premium), body **Inter**. `font-display:swap`. Type scale 13/14/16/18/22/30/44/64. Body line-height 1.6.

**Glass recipe:** `background: var(--glass); backdrop-filter: blur(var(--blur)) saturate(1.2); border:1px solid var(--glass-bd); border-radius:var(--radius);` + soft inner highlight + outer green glow on hover.

**Motion (all gated behind `prefers-reduced-motion`):**
- Hero: floating glow orbs + animated gradient mesh (CSS keyframes), staggered fade-up entrance on load.
- Scroll reveal: one shared `IntersectionObserver` adds `.in-view` → fade/translate-up, staggered 40–60ms.
- Cards/buttons: 200ms lift + brightening border + intensifying glow; button shine-sweep on hover.
- Sticky header: glass blur that darkens/condenses after scroll; active-link highlight by filename.
- Accent touches: industries marquee, optional count-up stats, SVG line-draw medical/data motif.
- Durations 150–300ms micro / ≤500ms hero; ease-out enter, exit faster.

**Icons:** Inline SVG (stroke 1.75), consistent family — no emoji.

## Page Plans (copy sourced/expanded from `content/`)

**header.html** — Sticky glass nav: monogram + wordmark, links (Home/Services/About/Contact), "Book a Consultation" CTA, mobile hamburger → glass sheet. Own `:root` + component `<style>`.

**footer.html** — Glass footer: brand blurb + socials, Services list, Company links, contact (email/phone/"Nationwide"), glowing CTA strip, copyright. Own `<style>`.

**home.html** — (1) Hero: consulting photo + dark-green glass overlay + glow orbs, title "Healthcare & Business Development. Management. Growth.", nationwide subtitle, two CTAs, floating glass stat chips. (2) Stat/trust band. (3) About Us glass panel (expanded paragraph from homepage-content.md + monogram). (4) Core Services — 4 glass cards w/ SVG icons (Operations Consulting, Finance Strategy, Marketing & Media, HR & Compliance), each links to `services.html`. (5) Industries (Healthcare/Law/Startups/Nonprofits) intro + chips/marquee. (6) Why Choose Us — 3 glow pillars (Data-Driven Decisions, Tailored Strategies, Nationwide Experience). (7) Glowing CTA band. (8) Footer include.

**services.html** — (1) Compact hero + CTA. (2) Approach intro. (3) Four detailed alternating glass sections (Operations Consulting, Finance Strategy, Marketing & Media, HR & Compliance), each with summary + "What We Offer" bulleted glass list + SVG icon (all copy from homepage-content.md lines 53–104). (4) "How we work" process steps with motion. (5) CTA band. (6) Footer.

**about.html** — (1) Hero "About FCo". (2) Mission — three expanded paragraphs (about-content.md + homepage-content.md lines 35–39) in glass panels. (3) The Teams — 4 cards (Growth & Development, Programs & Services, Financial Services, Operations & Management) with descriptions. (4) Values pillars + nationwide stats. (5) CTA. (6) Footer.

**contact.html** — (1) Hero "Let's talk". (2) Two columns: left = glass contact-info cards (email/phone/nationwide/hours) + reasons to reach out; right = glass form panel containing `[fluentform id="3"]` + FluentForms theming CSS. (3) CTA/closing. (4) Footer.

## Shared include + behavior script (inline in each page, before `</body>`)
```html
<div id="site-header"></div> <!-- at top of body -->
<div id="site-footer"></div> <!-- at end of body -->
<script>
  async function inject(id,f){try{const r=await fetch(f);if(r.ok)document.getElementById(id).innerHTML=await r.text();}catch(e){}}
  (async()=>{
    await inject('site-header','header.html');
    initHeader();            // wire hamburger, scroll-shrink, active link by location.pathname
    await inject('site-footer','footer.html');
  })();
  // IntersectionObserver scroll-reveal + prefers-reduced-motion guard
</script>
```
Because `innerHTML` won't run `<script>` inside partials, all header/footer interactivity is defined in this page-level script (or via event delegation), not inside the partials.

## Implementation order
1. Write `design.md` (tokens, type, motion, components) — **before any page**.
2. `header.html`, then `footer.html`.
3. `home.html` (establishes the reusable section/card/button/hero CSS patterns).
4. `services.html`, `about.html`, `contact.html` (reuse home's patterns; contact adds FluentForms CSS).

## Verification
- Serve `fandryco/` over http (e.g. `python -m http.server` from that folder) so the `fetch()` includes resolve; open each page.
- Use the Preview MCP / browser to confirm on a desktop and at 375px: header/footer inject correctly, active-link state works, nav is responsive, glass + glow render, scroll-reveal animations fire, and reduced-motion disables them.
- Check contrast of body/muted text on dark glass (≥4.5:1), focus states visible, hover states smooth, no horizontal scroll at 375px.
- Confirm the `[fluentform id="3"]` shortcode is present in `contact.html` inside the themed panel (renders live only in WordPress; static preview shows the styled container + literal shortcode).