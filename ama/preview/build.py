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
-->

{partial}

</body>
</html>
"""


def marker_of(text: str) -> str:
    """Pull the `<!-- webhook retrigger ... -->` version marker off the top."""
    found = re.match(r"\s*<!--\s*(webhook retrigger[^>]*?)\s*-->", text)
    return found.group(1) if found else "none found"


def main() -> int:
    missing = [name for name in PAGES if not (PARTIAL_DIR / name).is_file()]
    if missing:
        print("missing partial(s): " + ", ".join(missing), file=sys.stderr)
        return 1

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

        out = PREVIEW_DIR / f"{source.stem}.preview.html"
        out.write_text(
            SHELL.format(
                title=f"{label} - {SITE} (preview)",
                source=name,
                marker=html.escape(marker_of(partial)),
                partial=partial.strip(),
            ),
            encoding="utf-8",
        )
        print(f"{name} -> preview/{out.name}  [{marker_of(partial)}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
