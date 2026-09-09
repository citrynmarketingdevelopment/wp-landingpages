# AMA preview build

Local-only wrappers for the AMA GitPress body partials. **Nothing in this folder is
deployed.** GitPress fetches one explicit path per shortcode, so these files are
never served:

```txt
[divi_github_content owner="OWNER" repo="REPO" branch="main" path="ama/home.html" format="html"]
```

## Why the folder exists

`ama/home.html`, `ama/donate.html` and `ama/our-team.html` are body partials. Per
`GITPRESS_WEBSITE_STRUCTURE.md` section 3, they must not contain `<!DOCTYPE>`,
`<html>`, `<head>` or `<body>` — GitPress Managed mode supplies the document shell
and the global header/footer. That rule is also what stops you double-clicking a
partial to look at it.

`build.py` writes a `*.preview.html` beside each partial with the shell added and
the fragment left byte-for-byte intact.

## Use

```bash
python ama/preview/build.py
```

Then open `ama/preview/home.preview.html` in a browser. Re-run after every edit to
a partial — the previews are generated, so edits made to them are overwritten and
never reach the live site. Edit `ama/home.html`.

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
