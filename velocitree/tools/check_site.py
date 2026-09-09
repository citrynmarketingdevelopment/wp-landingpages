#!/usr/bin/env python3
"""Check the GitPress fragments and standalone previews without dependencies.

Run from any directory:
    python velocitree/tools/check_site.py

This validates document boundaries, landmarks, IDs, packaged assets, routes,
and local preview destinations. It does not replace browser layout checks or
verification on WordPress. External URLs are not fetched.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


FRAGMENTS = {
    "header.html": "header",
    "footer.html": "footer",
    "hero.html": "hero",
    "home.html": "body",
    "contact.html": "body",
}
PREVIEWS = (
    "preview/velocitree-home-preview.html",
    "preview/velocitree-contact-preview.html",
)
ROUTES = {"/": "home.html", "/contact": "contact.html"}
RAW_BASE = (
    "https://raw.githubusercontent.com/"
    "citrynmarketingdevelopment/wp-landingpages/main/velocitree/"
)
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I | re.S)
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".pdf", ".ico"}


@dataclass
class Reference:
    value: str
    line: int
    kind: str


class Document(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.source = path.read_text(encoding="utf-8-sig")
        self.tags: Counter[str] = Counter()
        self.ids: Counter[str] = Counter()
        self.links: list[Reference] = []
        self.assets: list[Reference] = []
        self.doctypes: list[str] = []
        self.missing_alt: list[int] = []
        self.in_style = False
        self.feed(self.source)

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype"):
            self.doctypes.append(decl.lower())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags[tag] += 1
        values = dict(attrs)
        line = self.getpos()[0]
        if values.get("id"):
            self.ids[values["id"]] += 1
        if tag == "style":
            self.in_style = True
        if tag == "img" and "alt" not in values:
            self.missing_alt.append(line)
        if tag in {"a", "area"}:
            self.links.append(Reference(values.get("href") or "", line, "link"))
        for attribute in ("src", "poster"):
            if values.get(attribute):
                self.assets.append(Reference(values[attribute], line, attribute))
        if tag == "link" and values.get("href"):
            self.assets.append(Reference(values["href"], line, "stylesheet/icon"))
        srcset = values.get("srcset")
        if srcset and not srcset.startswith("data:"):
            for candidate in srcset.split(","):
                if candidate.strip():
                    self.assets.append(Reference(candidate.strip().split()[0], line, "srcset"))
        if values.get("style"):
            self.css_assets(values["style"], line)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.css_assets(data, self.getpos()[0])

    def css_assets(self, css: str, line: int) -> None:
        for match in CSS_URL.finditer(css):
            self.assets.append(Reference(match.group(2).strip(), line, "CSS url"))


class Audit:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.documents: dict[str, Document] = {}
        self.errors: list[str] = []
        self.external: set[str] = set()
        self.checked_assets: set[Path] = set()

    def error(self, name: str, message: str, line: int | None = None) -> None:
        location = f"{name}:{line}" if line else name
        self.errors.append(f"{location}: {message}")

    def count(self, name: str, tag: str, expected: int) -> None:
        actual = self.documents[name].tags[tag]
        if actual != expected:
            self.error(name, f"expected {expected} <{tag}>, found {actual}")

    def load(self) -> None:
        for name in (*FRAGMENTS, *PREVIEWS):
            path = self.root / name
            if not path.is_file():
                self.error(name, "required file is missing")
                continue
            try:
                self.documents[name] = Document(path)
            except (OSError, UnicodeError) as exc:
                self.error(name, f"cannot read HTML: {exc}")

    def structure(self) -> None:
        for name, doc in self.documents.items():
            for identifier, count in doc.ids.items():
                if count > 1:
                    self.error(name, f"duplicate id={identifier!r} ({count} occurrences)")
            for line in doc.missing_alt:
                self.error(name, "image is missing its alt attribute", line)
            if name in FRAGMENTS:
                role = FRAGMENTS[name]
                if doc.doctypes:
                    self.error(name, "GitPress fragments must not include a doctype")
                for tag in ("html", "head", "body", "title"):
                    self.count(name, tag, 0)
                self.count(name, "main", int(role == "body"))
                self.count(name, "h1", int(role in {"body", "hero"}))
                self.count(name, "header", int(role == "header"))
                self.count(name, "footer", int(role == "footer"))
                if re.search(r"fetch\s*\(\s*['\"][^'\"]*(?:header|footer)\.html", doc.source, re.I):
                    self.error(name, "fragment fetches a header/footer; GitPress must assemble the shell")
                if role == "body" and "main-content" not in doc.ids:
                    self.error(name, "body partial lacks the main-content skip-link destination")
            else:
                if doc.doctypes != ["doctype html"]:
                    self.error(name, "preview must contain exactly one HTML5 doctype")
                for tag in ("html", "head", "body", "title", "main", "h1", "header", "footer"):
                    self.count(name, tag, 1)
        for body in ROUTES.values():
            names = ("header.html", body, "footer.html")
            if all(name in self.documents for name in names):
                combined: Counter[str] = Counter()
                for name in names:
                    combined.update(self.documents[name].ids)
                for identifier, count in combined.items():
                    if count > 1:
                        self.error(body, f"assembled header/body/footer repeats id={identifier!r}")

    def asset(self, name: str, ref: Reference) -> None:
        value = ref.value.strip()
        if not value or value.startswith(("data:", "blob:", "#")):
            return
        parts = urlsplit(value)
        if value.startswith(RAW_BASE):
            path = self.root / unquote(urlsplit(value[len(RAW_BASE):]).path)
        elif parts.scheme or parts.netloc:
            self.external.add(value)
            return
        elif parts.path.startswith("/"):
            path = self.root / unquote(parts.path.lstrip("/"))
        else:
            path = self.documents[name].path.parent / unquote(parts.path)
        path = path.resolve()
        self.checked_assets.add(path)
        if not path.is_file():
            self.error(name, f"missing packaged asset: {value}", ref.line)

    def target_ids(self, body: str) -> set[str]:
        result: set[str] = set()
        for name in ("header.html", body, "footer.html"):
            if name in self.documents:
                result.update(self.documents[name].ids)
        return result

    def links(self) -> None:
        for name, doc in self.documents.items():
            for ref in doc.assets:
                self.asset(name, ref)
            for ref in doc.links:
                value = ref.value.strip()
                if not value or value == "#":
                    self.error(name, "empty or placeholder link", ref.line)
                    continue
                parts = urlsplit(value)
                if parts.scheme in {"mailto", "tel"}:
                    if not parts.path:
                        self.error(name, "contact link has no destination", ref.line)
                    continue
                if parts.scheme and parts.scheme not in {"http", "https"}:
                    self.error(name, f"unsupported navigation scheme: {parts.scheme}", ref.line)
                    continue
                if value.startswith(RAW_BASE) or Path(parts.path).suffix.lower() in ASSET_EXTENSIONS:
                    self.asset(name, Reference(value, ref.line, "linked download"))
                    continue
                if parts.scheme or parts.netloc:
                    self.external.add(value)
                    continue
                fragment = unquote(parts.fragment)
                if name in FRAGMENTS:
                    if parts.path and not parts.path.startswith("/"):
                        self.error(name, f"production navigation must be root-relative: {value}", ref.line)
                        continue
                    route = parts.path.rstrip("/") or "/"
                    if not parts.path:
                        body = name if FRAGMENTS[name] == "body" else "home.html"
                    elif route in ROUTES:
                        body = ROUTES[route]
                    else:
                        self.error(name, f"unknown production route: {value}", ref.line)
                        continue
                    if fragment and body in self.documents and fragment not in self.target_ids(body):
                        self.error(name, f"missing production anchor: {value}", ref.line)
                else:
                    if parts.path.startswith("/"):
                        self.error(name, f"preview link needs a local file destination: {value}", ref.line)
                        continue
                    target = (doc.path.parent / unquote(parts.path)).resolve() if parts.path else doc.path.resolve()
                    if not target.is_file():
                        self.error(name, f"missing preview destination: {value}", ref.line)
                        continue
                    if fragment:
                        target_doc = next((item for item in self.documents.values() if item.path.resolve() == target), None)
                        if target_doc is None:
                            target_doc = Document(target)
                        if fragment not in target_doc.ids:
                            self.error(name, f"missing preview anchor: {value}", ref.line)

    def run(self) -> int:
        self.load()
        self.structure()
        self.links()
        for error in self.errors:
            print(f"FAIL {error}")
        print(
            f"Checked {len(self.documents)} HTML files and "
            f"{len(self.checked_assets)} packaged assets; {len(self.errors)} error(s)."
        )
        if self.external:
            print(f"Skipped {len(self.external)} external URL(s); no network requests were made.")
        if not self.errors:
            print("PASS GitPress structure, document IDs, assets, routes, and preview links.")
        return int(bool(self.errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site-dir", type=Path, default=Path(__file__).resolve().parents[1],
        help="site directory containing header.html, home.html and preview/",
    )
    return Audit(parser.parse_args().site_dir).run()


if __name__ == "__main__":
    sys.exit(main())
