"""Audit checked-in routes, fragment structure and original media copies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
routes = json.loads((ROOT / "routes.json").read_text(encoding="utf-8"))
assets = json.loads((ROOT / "assets/manifest.json").read_text(encoding="utf-8"))
valid_paths = set(routes["pages"]) | set(routes["archives"]) | set(routes["redirects"])
fragments = [ROOT / "header.html", ROOT / "footer.html"] + [
    ROOT / record["file"] for record in list(routes["pages"].values()) + list(routes["archives"].values())
]
failures: list[str] = []
unmapped_links: set[str] = set()
manifest_sources = {record["source"] for record in assets}

for fragment in fragments:
    contents = fragment.read_text(encoding="utf-8")
    soup = BeautifulSoup(contents, "html.parser")
    if soup.find(["html", "head", "body"]) or "<!doctype" in contents.lower():
        failures.append(f"Nested document in {fragment.name}")
    if soup.find("script"):
        failures.append(f"Executable script in {fragment.name}")
    if fragment.name not in ("header.html", "footer.html") and not soup.select_one(".amicus-page"):
        failures.append(f"Missing page wrapper in {fragment.name}")
    for link in soup.select("a[href]"):
        href = link["href"]
        if not href.startswith("/") or href.startswith("//"):
            continue
        path = urlsplit(href).path
        if path in valid_paths or path.startswith("/wp-content/uploads/"):
            continue
        unmapped_links.add(path)
    for tag in soup.select("img[src],video[src],source[src],a[href]"):
        url = tag.get("src") or tag.get("href", "")
        if url.startswith("https://amicusfoundation.com/wp-content/") and urlsplit(url)._replace(query="", fragment="").geturl() not in manifest_sources:
            failures.append(f"Media missing from inventory: {url}")

for record in assets:
    local = ROOT / record["local"]
    if not local.is_file():
        failures.append(f"Missing asset: {record['local']}")
        continue
    if local.stat().st_size != record["bytes"] or hashlib.sha256(local.read_bytes()).hexdigest() != record["sha256"]:
        failures.append(f"Corrupt asset: {record['local']}")

contact = [ROOT / "contact-us.html", ROOT / "recommended-charities.html"]
for path in contact:
    content = path.read_text(encoding="utf-8")
    if content.count("[gitpress_form id=") != 1 or content.count("[amicus_form_status id=") != 1:
        failures.append(f"Contact form binding incomplete in {path.name}")

report = {
    "routes": len(routes["pages"]) + len(routes["archives"]),
    "redirects": len(routes["redirects"]),
    "fragments": len(fragments),
    "original_assets": len(assets),
    "uploads": sum("/wp-content/uploads/" in item["source"] for item in assets),
    "pdfs": sum(item["source"].lower().endswith(".pdf") for item in assets),
    "videos": sum(item["source"].lower().endswith(".mp4") for item in assets),
    "unmapped_internal_links": sorted(unmapped_links),
    "failures": failures,
}
(ROOT / "qa/source-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
if failures:
    raise SystemExit(1)
