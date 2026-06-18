# GitPress Website Structure Guide for Agents

Use this guide when building or editing GitHub-hosted HTML/CSS/JS that will be rendered inside WordPress through **GitPress / Divi GitHub Sync** and managed by **Broseph**.

This file is intended to live in each website repo so Codex, Open Claw, Claude, or any other agent knows how to structure GitPress websites correctly.

---

## 1. Core Architecture

GitPress is not a normal static-site deploy. GitHub stores the HTML/CSS/JS source, but WordPress renders that source through GitPress shortcodes.

There are three render modes:

### Theme Wrapped

Use this for normal WordPress pages that should keep the existing WordPress/Divi header, menu, footer, theme wrapper, and site styling.

```txt
render_mode: theme_wrapped
render_position: replace
full_width_content: true
full_page_canvas: false
```

Expected output:

```txt
WordPress/Divi header
GitPress page content
WordPress/Divi footer
```

### Full Canvas

Use this only for standalone landing pages where the page output should become the whole body and the WordPress/Divi header/footer should be bypassed.

```txt
render_mode: full_canvas
render_position: replace
full_page_canvas: true
full_width_content: false
```

Expected output:

```txt
GitPress page content only
```

### GitPress Managed

Use this when GitPress should manage the header and footer from global GitPress settings. This is best when the entire page shell is controlled from GitHub instead of Divi.

```txt
render_mode: gitpress_managed
render_position: replace
full_page_canvas: true
full_width_content: false
```

Expected output:

```txt
GitPress global header shortcode
GitPress page body shortcode
GitPress global footer shortcode
```

---

## 2. Recommended Repo Structure

Use a clean folder per client or site.

```txt
repo-root/
  client-slug/
    header.html
    footer.html
    home.html
    about.html
    services.html
    contact.html
    service-pages/
      payroll-services-denver-co.html
      hr-services-los-angeles-ca.html
    location-pages/
      bakersfield-ca.html
    forms/
      contact-standard.json
    assets/
      css/
        shared.css
      js/
        shared.js
      images/
        hero.webp
```

For smaller sites, inline page-specific CSS in each HTML partial is acceptable. For larger sites, prefer shared CSS/JS files when GitPress is configured to load them safely.

---

## 3. File Types and Responsibilities

### `header.html`

Use only for the GitPress Managed global header.

Allowed:

```txt
<style> header-specific CSS </style>
<header>...</header>
<nav>...</nav>
mobile menu markup
<script> header behavior only </script>
```

Not allowed:

```txt
<!DOCTYPE html>
<html>
<head>
<body>
<main>
<footer>
page-specific sections
```

The header file should own:

```txt
scroll class behavior
hamburger/menu behavior
mobile drawer behavior
active nav link behavior
```

Page body files should not initialize the header.

### `footer.html`

Use only for the GitPress Managed global footer.

Allowed:

```txt
<style> footer-specific CSS </style>
<footer>...</footer>
<script> footer-only behavior, such as year updater </script>
```

Not allowed:

```txt
<!DOCTYPE html>
<html>
<head>
<body>
<header>
<main>
page-specific sections
```

### Page Body Files

Examples:

```txt
home.html
about.html
services.html
contact.html
service-pages/example.html
```

These files should be **GitPress body partials**, not full standalone HTML documents.

Allowed structure:

```html
<style>
  /* page-specific CSS */
</style>

<main>
  <!-- page sections -->
</main>

<script>
  // page-specific safe JS only
</script>
```

Do not include:

```txt
<!DOCTYPE html>
<html>
<head>
<body>
</body>
</html>
<div id="site-header"></div>
<div id="site-footer"></div>
fetch('header.html')
fetch('footer.html')
inject('site-header', 'header.html')
inject('site-footer', 'footer.html')
```

GitPress Managed mode already handles the document shell plus header/footer.

---

## 4. GitPress Shortcode Pattern

Use this shortcode format in WordPress/GitPress/Broseph:

```txt
[divi_github_content owner="OWNER" repo="REPO" branch="main" path="client-slug/home.html" format="html"]
```

Example:

```txt
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="fandryco/home.html" format="html"]
```

Do not add render mode inside the shortcode. Render mode belongs to GitPress page-level settings or Broseph payloads.

Bad:

```txt
[divi_github_content owner="..." repo="..." path="..." render_mode="theme-wrapped"]
```

Good:

```json
{
  "shortcode": "[divi_github_content owner=\"...\" repo=\"...\" branch=\"main\" path=\"fandryco/home.html\" format=\"html\"]",
  "render_mode": "gitpress_managed"
}
```

---

## 5. Page Creation Defaults

For normal service/location/SEO pages using the client’s existing WordPress shell:

```json
{
  "render_mode": "theme_wrapped",
  "render_position": "replace",
  "full_width_content": true,
  "full_page_canvas": false
}
```

For standalone campaign pages:

```json
{
  "render_mode": "full_canvas",
  "render_position": "replace",
  "full_width_content": false,
  "full_page_canvas": true
}
```

For GitHub-controlled shell pages:

```json
{
  "render_mode": "gitpress_managed",
  "render_position": "replace",
  "full_width_content": false,
  "full_page_canvas": true
}
```

---

## 6. Converting Existing WordPress / Divi Pages

When converting an existing live page from Divi Code Module content to GitPress, use Broseph’s in-place conversion route.

Do not create a replacement page when the original URL must stay live.

Required behavior:

```txt
preserve original page ID
preserve slug/permalink
preserve title
preserve status
preserve SEO meta
preserve parent/menu identity
create backup first
clear old Divi content when requested
disable Divi builder safely when requested
attach GitPress page-level shortcode/meta
```

Example payload:

```json
{
  "shortcode": "[divi_github_content owner=\"citrynmarketingdevelopment\" repo=\"wp-landingpages\" branch=\"main\" path=\"client-slug/service-pages/example.html\" format=\"html\"]",
  "render_mode": "theme_wrapped",
  "render_position": "replace",
  "full_width_content": true,
  "full_page_canvas": false,
  "backup_first": true,
  "clear_existing_content": true,
  "disable_divi_builder": true,
  "expected_slug": "example-service-page",
  "expected_status": "publish"
}
```

For GitPress Managed conversion, use:

```json
{
  "render_mode": "gitpress_managed",
  "render_position": "replace",
  "full_width_content": false,
  "full_page_canvas": true
}
```

---

## 7. HTML Rules for GitPress Pages

### Use semantic sections

Preferred:

```html
<main>
  <section class="hero">
    <div class="container">
      <h1>Page headline</h1>
      <p>Page intro.</p>
    </div>
  </section>
</main>
```

### Do not nest full documents

Never place a complete HTML document inside a GitPress page body file.

Bad:

```html
<!DOCTYPE html>
<html>
<head>...</head>
<body>...</body>
</html>
```

Good:

```html
<style>...</style>
<main>...</main>
<script>...</script>
```

### Links should be WordPress-friendly

Prefer root-relative URLs:

```html
<a href="/services">Services</a>
<a href="/contact">Contact</a>
```

Avoid static `.html` links unless intentionally linking to raw files:

```html
<a href="services.html">Services</a>
```

---

## 8. CSS Rules

### Scope styles when possible

Use client or page prefixes to avoid collisions with WordPress/theme/plugin CSS.

Examples:

```css
.fco-hero {}
.fco-card {}
.dgs-managed-main .hero {}
```

Global resets are risky. Avoid broad resets unless required and tested.

Use carefully:

```css
* { box-sizing: border-box; }
```

Avoid aggressive global styling:

```css
body * { margin: 0; padding: 0; }
html, body { overflow: hidden; }
```

### Font loading

If using Google Fonts, prefer loading them in the managed header or a shared global asset so they are not duplicated on every page.

If a page partial includes font links, ensure GitPress sanitizer allows them or move them to the managed header/plugin settings.

### Fixed headers

If `header.html` uses `position: fixed`, page body content needs top spacing or hero padding.

Example:

```css
.hero {
  padding-top: 136px;
}
```

Do not rely on WordPress/Divi header spacing in GitPress Managed mode.

---

## 9. Icons

Use inline SVG icons. GitPress supports a safe SVG allowlist.

Preferred pattern:

```html
<span class="ico" aria-hidden="true">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 3v18h18"/>
    <path d="m7 14 3-3 3 3 5-6"/>
  </svg>
</span>
```

Recommended CSS:

```css
.ico {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  color: var(--glow);
}

.ico svg {
  width: 24px;
  height: 24px;
  display: block;
}
```

Avoid temporary CSS-mask icon workarounds unless the project specifically uses a shared mask icon system.

Do not use unsafe SVG content:

```txt
<script>
foreignObject
onload / onclick / onerror
href / xlink:href
javascript:
data: URLs inside SVG
```

---

## 10. JavaScript Rules

### Keep JS small and local

Page body files may include page-specific JavaScript, but avoid large frameworks unless the project explicitly supports them.

Allowed:

```txt
reveal animations
sliders if lightweight
form enhancement
header/footer behavior in header/footer partials
```

Avoid:

```txt
browser-only static-site fetches for header/footer
hard dependencies on local .html files
scripts that require module bundling unless configured
scripts that break if WordPress moves markup
```

### No header/footer injection in page files

Bad:

```js
await fetch('header.html')
document.getElementById('site-header').innerHTML = ...
```

GitPress Managed already renders header/footer.

### Avoid hiding content when JS fails

Content must be visible by default.

Bad:

```css
.reveal-up { opacity: 0; }
[data-reveal] { opacity: 0; }
```

Good:

```css
.reveal-up,
[data-reveal] {
  opacity: 1;
  transform: none;
}

html.dgs-js .reveal-up,
html.dgs-js [data-reveal] {
  opacity: 0;
  transform: translateY(20px);
}

html.dgs-js.loaded .reveal-up,
html.dgs-js [data-reveal].in-view {
  opacity: 1;
  transform: none;
}
```

Add JS enhancement:

```html
<script>
  document.documentElement.classList.add('dgs-js');

  function initReveal(){
    var els = document.querySelectorAll('[data-reveal]');
    if (!('IntersectionObserver' in window)) {
      els.forEach(function(el){ el.classList.add('in-view'); });
      return;
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: .12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function(el){ io.observe(el); });
  }

  initReveal();
  requestAnimationFrame(function(){
    document.documentElement.classList.add('loaded');
  });
</script>
```

---

## 11. Forms

### Preferred form engine

Use Fluent Forms inside WordPress.

GitHub/GitPress should contain the embed location. WordPress/Fluent Forms handles the actual form submission, validation, notifications, entries, and spam controls.

### Raw shortcode pattern

Use the raw shortcode exactly where the form should appear:

```html
<div class="contact-form-card">
  <h2>Send us a message</h2>
  <p>Share a few details and our team will follow up.</p>

  <div class="fco-form-embed">
    [fluentform id="3"]
  </div>
</div>
```

Do not place form shortcodes inside:

```txt
<code>
<pre>
HTML comments
escaped brackets
fake placeholder panels
```

Bad:

```html
<code>[fluentform id="3"]</code>
```

Good:

```html
[fluentform id="3"]
```

### Scaling form IDs

Hardcoding Fluent Form IDs is acceptable for one site, but not ideal across many sites.

Short-term:

```html
[fluentform id="3"]
```

Better future pattern:

```html
<!-- BROSEPH_FORM: general-contact -->
```

Then Broseph/GitPress can map:

```txt
general-contact -> [fluentform id="3"] on Site A
general-contact -> [fluentform id="9"] on Site B
```

---

## 12. SEO Rules

SEO meta is managed in WordPress through Broseph and Yoast/Rank Math, not inside the GitHub HTML file.

Do not rely on this in page body partials:

```html
<title>...</title>
<meta name="description" content="...">
```

For GitPress page body files, omit `<head>` entirely.

After creating or converting a page, set:

```txt
SEO title
meta description
focus keyphrase
slug if needed
```

Do not fake SEO plugin scores.

---

## 13. GitPress Cache and Webhooks

After pushing changes to GitHub, GitPress may continue serving cached content until cache clears.

Expected workflow:

```txt
push to GitHub
GitHub webhook calls GitPress
GitPress clears cache
WordPress page updates
```

If webhook fails or changes do not show:

```txt
purge GitPress cache manually
hard refresh browser
check shortcode path/branch
check webhook secret/payload URL
check cache TTL
```

A GitHub webhook `403` usually means the site was reached but the webhook was rejected, often from secret mismatch or route/security rules.

---

## 14. Agent Workflow Checklist

Before editing:

```txt
identify target client folder
identify render mode
identify whether file is header/footer/page body
check if page is GitPress Managed or Theme Wrapped
avoid editing plugin repos unless explicitly requested
```

When creating a new page file:

```txt
create body partial only
no full document shell
no header/footer fetch
use inline SVG icons
content visible without JS
raw form shortcodes only
root-relative links
```

When creating/updating WordPress page through Broseph:

```txt
refresh /broseph/v1/tools
confirm GitPress active
confirm supported render modes
create draft page or convert existing page
set SEO meta
return preview URL
publish only when explicitly asked
```

When converting an existing page:

```txt
use convert-to-gitpress
backup_first: true
expected_slug required
expected_status required
preserve page ID/permalink
stop if partial/failed
```

When publishing:

```txt
publish only explicit page IDs
use bulk-publish if multiple
return permalinks
never publish automatically
```

When cleaning up:

```txt
trash only explicit draft IDs
never permanently delete
never trash published pages
```

---

## 15. Common Anti-Patterns

Avoid these:

```txt
full standalone HTML documents inside page body files
JavaScript header/footer injection
fetch('header.html') from page body
hidden content dependent on JS loading
fake form placeholders instead of real shortcodes
hardcoded .html links for WordPress navigation
rewriting all icons into CSS masks when inline SVG works
mixing Divi Code Module embeds with GitPress page-level rendering
creating replacement pages when original URL/page ID must be preserved
publishing without explicit user approval
storing Broseph shared secrets in markdown, repo files, logs, or memory
```

---

## 16. Standard Test Plan

After changes are pushed and cache is purged, verify:

```txt
page loads without fatal error
managed header displays once
managed footer displays once
no duplicate Divi/theme header/footer in GitPress Managed mode
page body content displays
icons render
buttons/links work
mobile menu works
forms render
forms submit if testing is approved
SEO meta remains correct
old Divi content is gone after conversion
cache/webhook updates work
```

For GitPress Managed pages specifically:

```txt
GitPress header renders
page body renders
GitPress footer renders
WordPress/Divi header/footer do not duplicate
wp_head/wp_footer assets load
admin bar appears for logged-in admins if supported
```

---

## 17. Quick Templates

### GitPress Managed Header Partial

```html
<style>
  .site-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }
</style>

<header class="site-header" id="siteHeader">
  <nav class="nav" aria-label="Primary">
    <a class="brand" href="/home">Brand</a>
    <a href="/services">Services</a>
    <a href="/contact">Contact</a>
  </nav>
</header>

<script>
(function(){
  if (window.__gitpressHeaderInit) return;
  window.__gitpressHeaderInit = true;

  var header = document.getElementById('siteHeader');
  function onScroll(){
    if (header) header.classList.toggle('scrolled', window.scrollY > 24);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
</script>
```

### GitPress Managed Page Body Partial

```html
<style>
  .hero { padding: 136px 0 72px; }
</style>

<main>
  <section class="hero">
    <div class="container">
      <h1>Page Headline</h1>
      <p>Page intro copy.</p>
      <a class="btn btn-primary" href="/contact">Get Started</a>
    </div>
  </section>
</main>
```

### Contact Form Block

```html
<section class="contact-section">
  <div class="container">
    <div class="contact-form-card">
      <h2>Send us a message</h2>
      <p>Tell us what you need and our team will follow up.</p>
      <div class="form-embed">
        [fluentform id="3"]
      </div>
    </div>
  </div>
</section>
```

---

## 18. Final Rule

GitPress website files should be clean, portable HTML fragments designed to render inside WordPress through GitPress.

When in doubt:

```txt
Header/footer live in GitPress global managed layout.
Page files are body partials only.
WordPress handles SEO, forms, publishing, and routing.
GitHub stores the design/content source.
Broseph connects the workflow safely.
```
