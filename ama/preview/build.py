#!/usr/bin/env python3
"""Wrap the AMA GitPress body partials in a full HTML document for local preview.

The files in ama/ are GitPress body partials: per GITPRESS_WEBSITE_STRUCTURE.md
section 3, they must never contain <!DOCTYPE>, <html>, <head> or <body>, because
GitPress Managed mode supplies the document shell plus the global header/footer.

That makes them impossible to open directly in a browser. This script writes a
throwaway *.preview.html next to it that adds only the document shell, leaving
the partial byte-for-byte intact so what you review is what GitPress renders.

Usage:  python ama/preview/build.py
"""

import html
import pathlib
import re
import sys

PREVIEW_DIR = pathlib.Path(__file__).resolve().parent
PARTIAL_DIR = PREVIEW_DIR.parent

# Partials to wrap -> browser tab title.
PAGES = {
    "home.html": "Home",
    "donate.html": "Donate",
    "our-team.html": "Our Team",
    "our-programs.html": "Our Programs",
    "our-programs/comfort-kits.html": "Comfort Kits",
    "our-programs/family-relief-fund.html": "Family Relief Fund",
    "our-programs/family-grants.html": "Gift of Family Grants",
    "our-programs/prayer-support.html": "Prayer Support",
    "our-programs/support-group.html": "Support Groups",
    "our-programs/angels-of-comfort.html": "Angels of Comfort",
}

# Grouped for the preview index. Keys are the PAGES keys above.
INDEX_GROUPS = [
    ("Site pages", ["home.html", "our-team.html", "donate.html"]),
    ("Programs", [
        "our-programs.html",
        "our-programs/comfort-kits.html",
        "our-programs/family-relief-fund.html",
        "our-programs/family-grants.html",
        "our-programs/prayer-support.html",
        "our-programs/support-group.html",
        "our-programs/angels-of-comfort.html",
    ]),
]

# The live WordPress slug each partial is rendered at, shown on the index so
# the shortcode path and the permalink can be checked against each other.
SLUGS = {
    "home.html": "/",
    "our-team.html": "/who-we-are/",
    "donate.html": "/ways-to-give/",
    "our-programs.html": "/our-programs/",
    "our-programs/comfort-kits.html": "/our-programs/comfort-kits/",
    "our-programs/family-relief-fund.html": "/our-programs/family-relief-fund/  (new page)",
    "our-programs/family-grants.html": "/our-programs/family-grants/",
    "our-programs/prayer-support.html": "/our-programs/prayer-support/",
    "our-programs/support-group.html": "/our-programs/support-group/",
    "our-programs/angels-of-comfort.html": "/our-programs/angels-of-comfort/  (new page)",
}

SITE = "Amelia Molloy's Angels"

# The shell stays deliberately thin. Every rule added here is a rule the live
# WordPress page does not have, and would hide real bugs behind a local-only
# fix. The partials are self-scoped (font, background, box-sizing, links), so
# collapsing the default body margin is all the shell owes them.
SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{
    margin: 0;
  }}
</style>
</head>
<body>

<!-- ==========================================================================
     GENERATED FILE - DO NOT EDIT. Edit ama/{source} instead, then re-run:
         python ama/preview/build.py
     Source marker: {marker}
     ==========================================================================
     This preview has no Divi and no GitPress managed header/footer, so it is
     a layout and content check only. Divi ships global !important rules on
     h1-h6/p/a that can still shift colors and spacing on the live page --
     GITPRESS_WEBSITE_STRUCTURE.md section 8 -- so confirm on staging before
     calling a visual change done.

     One content change is made here: root-relative links whose slug matches a
     page in this preview set are repointed at the sibling *.preview.html so
     the set is clickable offline. Everything else is verbatim. The live files
     in ama/ keep the real WordPress permalinks.
-->

{partial}

</body>
</html>
"""


INDEX_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{site} - preview index</title>
<style>
  body {{
    margin: 0;
    padding: 48px 20px 80px;
    background: #F7F7FC;
    color: #3D3D58;
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }}
  .wrap {{ width: min(100% - 8px, 860px); margin: 0 auto; }}
  h1 {{ margin: 0 0 6px; font-size: 1.9rem; }}
  .sub {{ margin: 0 0 12px; color: #5D5F79; }}
  .warn {{
    margin: 0 0 34px; padding: 14px 18px; border-radius: 12px;
    background: #FFF6E2; border: 1px solid #E7D9BC; color: #6B5526; font-size: .92rem;
  }}
  h2 {{ margin: 34px 0 14px; font-size: .78rem; letter-spacing: .22em;
       text-transform: uppercase; color: #6F74AE; }}
  ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }}
  a.row {{
    display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 10px 20px;
    align-items: baseline; padding: 16px 20px; border-radius: 14px;
    background: #fff; border: 1px solid rgba(153,157,206,.28);
    color: inherit; text-decoration: none;
  }}
  a.row:hover {{ border-color: #999DCE; box-shadow: 0 10px 26px rgba(102,106,160,.14); }}
  .name {{ font-weight: 600; }}
  .slug {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .8rem; color: #6F74AE; }}
  .src {{ grid-column: 1 / -1; font-family: ui-monospace, Menlo, Consolas, monospace;
          font-size: .76rem; color: #8A8CA6; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>{site}</h1>
  <p class="sub">Local preview of the GitPress body partials. Generated by
    <code>ama/preview/build.py</code> - do not edit these files.</p>
  <p class="warn">No Divi and no GitPress managed header/footer are present here, so this is a
    layout and content check only. Colors and spacing can still shift once the fragment renders
    through Divi (GITPRESS_WEBSITE_STRUCTURE.md section 8). Confirm on staging before signing off.</p>
{groups}
</div>
</body>
</html>
"""


def marker_of(text: str) -> str:
    """Pull the `<!-- webhook retrigger ... -->` version marker off the top."""
    found = re.match(r"\s*<!--\s*(webhook retrigger[^>]*?)\s*-->", text)
    return found.group(1) if found else "none found"


def preview_name(page: str) -> str:
    """preview file for a PAGES key, e.g. our-programs/comfort-kits.html."""
    return f"{pathlib.PurePosixPath(page).stem}.preview.html"


def localize_links(partial: str) -> str:
    """Point root-relative links at their sibling preview file.

    The partials use WordPress permalinks (/our-programs/comfort-kits/), which
    do not resolve when a preview is opened from the filesystem. Rewriting only
    the hrefs whose slug maps to a page we build keeps the preview clickable.
    Everything else - unbuilt site pages, anchors, mailto, tel, external - is
    left exactly as written so broken links still show up as broken.
    """
    by_slug = {SLUGS[page].split()[0]: preview_name(page) for page in PAGES}
    for slug, target in by_slug.items():
        partial = partial.replace(f'href="{slug}"', f'href="{target}"')
    return partial


def build_index(markers: dict) -> str:
    groups = []
    for title, pages in INDEX_GROUPS:
        rows = []
        for page in pages:
            rows.append(
                '    <li><a class="row" href="{href}">'
                '<span class="name">{name}</span>'
                '<span class="slug">{slug}</span>'
                '<span class="src">ama/{src} &middot; {marker}</span>'
                "</a></li>".format(
                    href=preview_name(page),
                    name=html.escape(PAGES[page]),
                    slug=html.escape(SLUGS[page]),
                    src=html.escape(page),
                    marker=html.escape(markers[page]),
                )
            )
        groups.append(
            f"  <h2>{html.escape(title)}</h2>\n  <ul>\n" + "\n".join(rows) + "\n  </ul>"
        )
    return "\n".join(groups)


def main() -> int:
    missing = [name for name in PAGES if not (PARTIAL_DIR / name).is_file()]
    if missing:
        print("missing partial(s): " + ", ".join(missing), file=sys.stderr)
        return 1

    indexed = {page for _, pages in INDEX_GROUPS for page in pages}
    if indexed != set(PAGES):
        print("INDEX_GROUPS and PAGES disagree: "
              f"{indexed ^ set(PAGES)}", file=sys.stderr)
        return 1
    if set(SLUGS) != set(PAGES):
        print(f"SLUGS and PAGES disagree: {set(SLUGS) ^ set(PAGES)}", file=sys.stderr)
        return 1

    markers = {}

    for name, label in PAGES.items():
        source = PARTIAL_DIR / name
        partial = source.read_text(encoding="utf-8")

        # A partial that grew a document shell would nest one document inside
        # another here, and would already be invalid as a GitPress fragment.
        stray = re.search(r"<!DOCTYPE|<html[\s>]|<head[\s>]|<body[\s>]", partial, re.I)
        if stray:
            print(f"{name}: contains {stray.group(0)!r} - not a valid GitPress "
                  f"body partial, refusing to wrap it", file=sys.stderr)
            return 1

        markers[name] = marker_of(partial)

        out = PREVIEW_DIR / preview_name(name)
        out.write_text(
            SHELL.format(
                title=f"{label} - {SITE} (preview)",
                source=name,
                marker=html.escape(markers[name]),
                partial=localize_links(partial.strip()),
            ),
            encoding="utf-8",
        )
        print(f"{name} -> preview/{out.name}  [{markers[name]}]")

    index = PREVIEW_DIR / "index.html"
    index.write_text(
        INDEX_SHELL.format(site=html.escape(SITE), groups=build_index(markers)),
        encoding="utf-8",
    )
    print(f"\nopen preview/{index.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
