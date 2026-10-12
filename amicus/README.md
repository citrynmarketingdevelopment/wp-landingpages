# Amicus Foundation GitPress migration

This folder contains GitPress body fragments for the existing Amicus Foundation
WordPress URLs, a shared managed header and footer, the original media archive,
and a small site companion plugin. The public URL paths stay unchanged.

## Source and layout

`routes.json` maps every migrated page to its HTML fragment, original WordPress
ID, title, description, canonical URL and GitPress shortcode. `deployment.json`
contains the 14 backup-first Broseph conversion requests. The page files contain
only body fragments; `header.html` and `footer.html` are the GitPress Managed
global fragments. The source page CSS lives in `assets/css/<route>.css`, with
site-specific integration rules in `assets/css/site.css`.

The page HTML and CSS were captured from the public site on 2026-10-01. The two
saved reference pages in `references/` matched the live source at capture time.
`assets/manifest.json` maps each of the 225 downloaded files to its original URL
and SHA-256 checksum. This includes all 205 referenced uploads, the original
image variants, five PDFs, two MP4 files, and 20 Divi icon/font resources.
Public pages continue to use the existing `/wp-content/uploads/` URLs; the
repository copies support local preview and recovery.

To refresh the capture after the source site changes, run:

```powershell
python amicus/tools/import_site.py --download-assets
python amicus/tools/package_plugin.py
python amicus/tools/build_deployment.py
```

Refresh regenerates the page fragments. Rebind the contact form ID afterward.

## Local preview and checks

From the repository root:

```powershell
python amicus/tools/preview.py --port 8765
python amicus/tools/verify_preview.py
python amicus/tools/verify_source.py
```

Open `http://127.0.0.1:8765/`. The preview uses local media copies and a visual
stand-in for GitPress Forms; submissions are disabled there. `qa/report.json`
records route, breakpoint and interaction checks. `qa/source-report.json`
records asset hashes and internal-link coverage. Selected screenshots are in
`qa/screenshots/`; the captured source comparisons are in
`qa/original-screenshots/`.

## WordPress staging setup

1. Confirm GitPress and GitPress Forms are installed and active. GitPress Forms
   `0.1.1-dev` is a development preview. Complete the form checks on staging
   before switching the live contact pages.
2. Copy `wp-plugin/` to `wp-content/plugins/amicus-site/` and activate **Amicus
   GitPress Site**. This package supplies route styles, menu/slider behavior,
   approved Jotform and YouTube embeds, native project/author archives, and the
   `/layout_tag/light/` redirect. It changes no shared plugin source.
3. In GitPress global settings, set the managed header and footer shortcodes
   from `routes.json`. Use the `gitpress_managed` mode and `replace` position
   for every page. GitPress supplies the document shell.
4. Preview `forms/contact-import.json` through authenticated
   `POST /wp-json/gitpress-forms/v1/import/preview`, then import through
   `POST /wp-json/gitpress-forms/v1/import`. The import creates a **draft** and
   returns `forms[0].id`. The stable source ID prevents duplicate forms on a
   repeated import.
5. Run `python amicus/tools/bind_contact_form.py --id <returned-number>` and
   commit the two changed page fragments. Review and publish that form in
   WordPress. Its notifications go to `info@amicusfoundation.com`. Confirm the
   site's mail service and cron jobs are working. Both pages show a contact
   email fallback while the form is unavailable. The repository intentionally
   retains `__AMICUS_CONTACT_FORM_ID__` until the target WordPress importer
   supplies its real ID; the isolated test ID must not be used on production.
6. Configure the existing pages using `deployment.json`. Before each in-place
   conversion, verify its current ID, slug, status, parent and SEO values. Use
   the supplied `backup_first: true` payload. Stop on a partial or failed
   conversion. Broseph v1 converts only `page` posts; attach the GitPress
   shortcode in `deployment.json` to the existing `/project/test/` custom post
   through its GitPress meta box. The companion plugin renders `/project/` and
   `/author/amicus/` with native WordPress queries and search.
7. After the repository is pushed, verify the GitPress webhook/cache refresh.
   Check the source marker at the top of each rendered page before diagnosing
   stale CSS. Verify the managed header and footer appear once, media loads,
   Yoast metadata remains intact, and every link follows its original target.

The two grant forms remain on Jotform. Their IDs are `230195983314055` (new)
and `250696793084167` (returning). The site companion shortcode embeds the
original Jotform script after GitPress has sanitized the page fragment, so
Jotform retains its multi-file uploads, validation, and notifications.

## Required staging checks

- Test 1440px desktop, 1024px landscape tablet, 820px and 768px portrait
  tablet, and 390px and 375px mobile; check both sides of 980px and 767px.
- Check desktop dropdowns, mobile submenu, hamburger, scrim, Escape, active
  navigation, sliders, accordion, counters, progress bar, videos, PDFs, icons,
  and reduced-motion behavior.
- Verify Contact Us and Recommended Charities render the **same imported form**.
  Test required fields, invalid email, successful synthetic submission,
  notification routing, and a simulated mail failure. Do not submit test
  applications to the production Jotforms.
- Confirm all 14 in-place page conversions preserve page ID, permalink,
  published status, parent/menu identity, and SEO data. Verify native project
  search and comments and the tag redirect.

The route manifest contains live public IDs for planning and review. Recheck
them against WordPress immediately before any conversion.

The isolated WordPress test passed native form import, idempotency, fragment
rendering through GitPress, required-field/email validation, session rejection,
synthetic submission, intercepted notification delivery, and mail-failure retry.
See `qa/form-test-result.json`. To repeat it in a disposable WordPress install
with GitPress and GitPress Forms active, set `AMICUS_TEST_WP` to that install's
directory and run `tools/validate_contact_form.php`,
`tools/validate_gitpress.php`, and `tools/test_contact_submission.php` with PHP.
These scripts never submit to the live site or Jotform.
