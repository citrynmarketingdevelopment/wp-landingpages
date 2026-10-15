# Fandry & Co. — Design System

Visual + interaction specification for the FandryCo website. Read this **before** editing any page. Style direction: **Liquid Glass (glassmorphism)** on a **dark-green + black** foundation, with **glow, animation, and motion** — a premium "consulting tech" feel for a healthcare business-development firm.

> Stack: static HTML, internal `<style>` blocks (no external CSS file), inline SVG icons, vanilla JS. Shared `header.html` / `footer.html` are injected at runtime via `fetch()`.

---

## 1. Brand

- **Name:** Fandry & Co. — short form **FCo**.
- **Tagline:** "Healthcare & Business Development. Management. Growth."
- **Positioning sub:** Nationwide consulting solutions for private-practice medical groups of any size and specialty.
- **Logo:** No asset yet. Use a glass **"FCo" monogram tile** (rounded square, emerald gradient edge + glow) beside the **"FANDRY & CO."** wordmark. Built to be swapped for a real logo (replace the `.brand-mark` block).

---

## 2. Color Tokens

Defined in `:root` of **every** file (pages + partials) so styling is consistent and never depends on injection order.

```css
:root{
  /* Backgrounds (near-black, green-tinted) */
  --ink:#050806;          /* page base */
  --bg-2:#0A1410;         /* alt section */
  --bg-3:#08110D;         /* deep panel */

  /* Greens */
  --green-900:#0B3D2E;
  --green-700:#0F6B43;
  --green-500:#16A86B;
  --green-400:#2BD17E;

  /* Glow / accent */
  --glow:#34E89E;
  --mint:#7CFFD4;
  --cta:linear-gradient(135deg,#34E89E 0%,#0F9B6C 100%);

  /* Glass */
  --glass:rgba(255,255,255,.05);
  --glass-2:rgba(18,80,55,.18);
  --glass-bd:rgba(124,255,212,.16);
  --glass-bd-strong:rgba(124,255,212,.32);

  /* Text */
  --fg:#EAF6EF;           /* primary */
  --muted:#9DB5AA;        /* secondary (>=4.5:1 on dark) */
  --muted-2:#6E867B;      /* tertiary / labels */

  /* Effects */
  --blur:18px;
  --radius:20px;
  --radius-sm:12px;
  --glow-shadow:0 0 40px rgba(52,232,158,.25);
  --shadow:0 24px 60px rgba(0,0,0,.45);
  --container:1180px;
  --ease:cubic-bezier(.22,1,.36,1);
}
```

**Contrast rules:** body copy uses `--fg` or `--muted` on dark backgrounds (≥4.5:1). Never put `--muted-2` on glass for paragraph text — labels/eyebrows only. Accent green text (`--glow`) is for large headings/labels, not small body.

---

## 3. Typography

Google Fonts, `display=swap`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

- **Headings:** `Space Grotesk` — geometric, techy-premium. Weights 500–700. Letter-spacing -0.02em on large sizes.
- **Body / UI:** `Inter`. Weights 300–600. Line-height 1.6.
- **Eyebrows/labels:** Inter 600, uppercase, letter-spacing .18em, 12–13px, color `--glow` or `--muted-2`.
- **Type scale (px):** 13 · 14 · 16 · 18 · 22 · 30 · 44 · 64. Use `clamp()` for hero (`clamp(2.6rem,6vw,4.4rem)`).

---

## 4. Glass Recipe

```css
.glass{
  background:linear-gradient(160deg,var(--glass),var(--glass-2));
  backdrop-filter:blur(var(--blur)) saturate(1.25);
  -webkit-backdrop-filter:blur(var(--blur)) saturate(1.25);
  border:1px solid var(--glass-bd);
  border-radius:var(--radius);
  box-shadow:var(--shadow), inset 0 1px 0 rgba(255,255,255,.06);
}
.glass:hover{ border-color:var(--glass-bd-strong); box-shadow:var(--shadow),var(--glow-shadow); }
```

- Always pair `backdrop-filter` with a `-webkit-` prefix.
- Inner top highlight (`inset 0 1px 0 rgba(255,255,255,.06)`) sells the glass.
- Hover intensifies border + adds green glow (no layout shift — only shadow/border/transform).

---

## 5. Components

- **Buttons**
  - `.btn-primary`: `--cta` gradient, dark text (`#04130C`), pill radius, glow shadow; hover = lift `translateY(-2px)` + brighter glow + shine-sweep (animated `::before` highlight). Min height 48px.
  - `.btn-ghost`: transparent, `--glass-bd` border, `--fg` text; hover = glass fill + border brighten.
  - Focus-visible: 2px `--glow` outline, offset 2px. Always `cursor:pointer`.
- **Cards** `.glass` + padding 28–32px; icon tile (44–56px glass square with emerald glow), title (Space Grotesk 20–22), copy (`--muted`).
- **Icon tile** `.ico`: glass square, inline SVG 24px, stroke `var(--glow)` stroke-width 1.75, subtle glow.
- **Eyebrow** `.eyebrow`: dot + uppercase label.
- **Glow orbs** `.orb`: absolutely-positioned blurred radial gradients (emerald/mint) behind hero & section backgrounds; slow float animation.
- **Section shell** `.section{padding:clamp(72px,10vw,128px) 0}`; `.container{width:min(var(--container),calc(100% - 40px));margin-inline:auto}`.
- **Stat chip / pillar:** glass, big number (Space Grotesk 30–44, `--glow`), label `--muted-2`.
- **Marquee:** horizontally scrolling industry/specialty chips (`@keyframes marquee`), paused on reduced-motion.

---

## 6. Icons

Inline SVG only — **no emoji**. Consistent family: 24×24 viewBox, `fill="none"`, `stroke="currentColor"` (set color to `--glow`), `stroke-width="1.75"`, round caps/joins. Reuse a small inline set per page (operations/gear, finance/chart, marketing/megaphone, HR/people, shield, spark, etc.).

---

## 7. Motion

All motion is wrapped behind `@media (prefers-reduced-motion: no-preference)` (or disabled inside `prefers-reduced-motion: reduce`).

- **Hero entrance:** staggered fade-up (`translateY(18px)`→0, opacity) on load, 60ms stagger, `--ease`, ≤500ms.
- **Glow orbs:** slow float/scale loop (12–20s, ease-in-out, alternate).
- **Scroll reveal:** one shared `IntersectionObserver` toggles `.in-view` on `[data-reveal]`; transition opacity + `translateY(20px)`. Stagger via `transition-delay` (40–60ms increments by index).
- **Hover micro-interactions:** 150–220ms; cards lift + glow; buttons shine-sweep + lift. Use `transform`/`opacity`/`box-shadow`/`border-color` only.
- **Header:** adds `.scrolled` after 24px scroll → stronger blur + darker bg + thinner padding.
- **Easing:** enter `--ease` (ease-out feel); exits faster (~70%). No `linear` for UI.
- **Reduced motion:** orbs static, reveals show immediately (opacity 1, no transform), marquee paused.

---

## 8. Layout & Responsive

- Mobile-first. Breakpoints: 480 / 768 / 1024 / 1280.
- Container max 1180px, 20px gutters; grids collapse to 1 column < 768px.
- Touch targets ≥44px; nav becomes hamburger → glass sheet < 900px.
- No horizontal scroll at 375px. Hero text uses `clamp()`. Images `loading="lazy"` + width/height/aspect-ratio to avoid CLS.
- `min-height:100dvh` on hero (not 100vh).

---

## 9. Imagery

- **Hero backgrounds:** real consulting/medical photos (Unsplash hotlinks) under a dark-green glass overlay (`linear-gradient` from `--ink` → transparent + green tint) so text stays ≥4.5:1. Always set an overlay; never raw photo behind text.
- **Inner sections:** CSS/SVG glow orbs, glass panels, thin line-art motifs (no stock photos required).

---

## 10. Shared Header/Footer Injection

Each page has placeholders + an inline script (partials' own `<script>` won't run through `innerHTML`, so behavior lives in the page script):

```html
<div id="site-header"></div>   <!-- top of body -->
<div id="site-footer"></div>   <!-- end of body -->
```

The page script: `fetch('header.html')`/`fetch('footer.html')` → inject → `initHeader()` (hamburger toggle, scroll `.scrolled`, active-link by `location.pathname` filename) → init scroll-reveal observer. Requires serving over http/WordPress, not `file://`.

---

## 11. Page Map

| Page | Sections |
|------|----------|
| **home** | Hero · stat band · About FCo · Core Services (4 cards→services) · Industries (marquee) · Why Choose Us (3 pillars) · CTA band · footer |
| **services** | Compact hero · approach · 4 detailed alternating service blocks (+ "What We Offer" lists) · How We Work steps · CTA · footer |
| **about** | Hero · Mission (3 panels) · The Teams (4 cards) · Values/stats · CTA · footer |
| **contact** | Hero · info cards + themed `[fluentform id="3"]` panel · closing CTA · footer |

---

## 12. Pre-Delivery Checklist

- [ ] No emoji icons (SVG only); consistent stroke width.
- [ ] `cursor:pointer` + visible `:focus-visible` on all interactive elements.
- [ ] Body/muted text ≥4.5:1 on dark glass.
- [ ] Hover transitions 150–300ms; no layout shift on hover.
- [ ] `prefers-reduced-motion` respected (orbs/reveals/marquee).
- [ ] Responsive at 375 / 768 / 1024 / 1440; no horizontal scroll.
- [ ] Header/footer inject correctly; active nav link highlighted.
- [ ] `[fluentform id="3"]` present in a themed panel on contact.
