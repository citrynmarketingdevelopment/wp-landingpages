# AMA preview build

Local-only wrappers for the AMA GitPress body partials. **Nothing in this folder is
deployed.** GitPress fetches one explicit path per shortcode, so these files are
never served:

```txt
[divi_github_content owner="OWNER" repo="REPO" branch="main" path="ama/home.html" format="html"]
```

## Why the folder exists

Everything in `ama/` — `home.html`, `donate.html`, `our-team.html`,
`our-programs.html` and the six pages under `our-programs/` — is a body partial.
Per `GITPRESS_WEBSITE_STRUCTURE.md` section 3, they must not contain `<!DOCTYPE>`,
`<html>`, `<head>` or `<body>` — GitPress Managed mode supplies the document shell
and the global header/footer. That rule is also what stops you double-clicking a
partial to look at it.

`build.py` writes a `*.preview.html` per partial with the shell added, plus an
`index.html` listing every page with its live slug and version marker.

## Use

```bash
python ama/preview/build.py
```

Then open `ama/preview/index.html` and click through from there. Re-run after every
edit to a partial — the previews are generated, so edits made to them are
overwritten and never reach the live site. Edit the file in `ama/`.

## Adding a page

Add it to `PAGES`, `INDEX_GROUPS` and `SLUGS` in `build.py`. The build fails loudly
if those three disagree, so a new partial cannot silently miss the index.

## Links in the preview

The partials use real WordPress permalinks (`/our-programs/comfort-kits/`), which do
not resolve from the filesystem. The build repoints only those hrefs whose slug
matches a page in the set at the sibling `*.preview.html`, so the Programs set is
clickable offline. Anchors, `mailto:`, `tel:`, external URLs, and links to site pages
we do not build here are left verbatim — so a genuinely broken link still reads as
broken. The files in `ama/` are untouched and keep the real permalinks.

## What this preview does not tell you

No Divi and no managed header/footer are present, so treat it as a layout and
content check only. Section 8 of the structure guide covers the gap: Divi ships
global `!important` rules on `h1`–`h6`, `p` and `a` that can still move colors and
spacing once the fragment renders through WordPress, and the GitPress sanitizer
strips inline `style="..."`. Both are invisible here.

Before calling a visual change done, confirm on the live/staging page — and if a
fix looks like it "didn't take", check the `<!-- webhook retrigger ... -->` marker
in the rendered page source before assuming a specificity fight. A stale GitPress
content cache reads exactly like a Divi override:

```bash
curl -s -A "Mozilla/5.0" "https://SITE/slug/" | grep -o "webhook retrigger [0-9-]*[a-z]*"
```
