"""Bind the numeric ID returned by GitPress Forms import to both body partials."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "__AMICUS_CONTACT_FORM_ID__"
FILES = ("contact-us.html", "recommended-charities.html")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, type=int, help="numeric ID returned by GitPress Forms /import")
    args = parser.parse_args()
    if args.id < 1:
        parser.error("form ID must be a positive integer")
    original = {}
    for name in FILES:
        path = ROOT / name
        content = path.read_text(encoding="utf-8")
        if content.count(TOKEN) != 2 and not (
            re.search(r'\[gitpress_form id="[0-9]+"\]', content)
            and re.search(r'\[amicus_form_status id="[0-9]+"\]', content)
        ):
            raise SystemExit(f"expected contact form and status shortcodes in {name}")
        original[path] = content
    for path, content in original.items():
        content = content.replace(TOKEN, str(args.id))
        content = re.sub(r'\[gitpress_form id="[0-9]+"\]', f'[gitpress_form id="{args.id}"]', content)
        content = re.sub(r'\[amicus_form_status id="[0-9]+"\]', f'[amicus_form_status id="{args.id}"]', content)
        path.write_text(content, encoding="utf-8")
    (ROOT / "forms" / "binding.json").write_text(json.dumps({"contact_form_id": args.id}, indent=2) + "\n", encoding="utf-8")
    print(f"Bound GitPress Forms ID {args.id} in {', '.join(FILES)}")


if __name__ == "__main__":
    main()
