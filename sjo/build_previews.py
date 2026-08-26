#!/usr/bin/env python3
"""Build and validate standalone previews for the SJO GitPress fragments."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PREVIEW_DIR = ROOT / "preview"
HEADER_SOURCE = ROOT / "header.html"
FOOTER_SOURCE = ROOT / "footer.html"
CDN_BASE = (
    "https://cdn.jsdelivr.net/gh/citrynmarketingdevelopment/"
    "wp-landingpages@main/sjo/assets/images/"
)
FORM_SHORTCODE = '[fluentform id="3"]'
LEGACY_FORM_MARKER = "<!-- BROSEPH_FORM: general-contact -->"


@dataclass(frozen=True)
class Page:
    key: str
    title: str
    source: Path
    preview: Path


PAGES = (
    Page("home", "Home", ROOT / "home.html", PREVIEW_DIR / "home-preview.html"),
    Page(
        "services",
        "Services",
        ROOT / "services.html",
        PREVIEW_DIR / "services-preview.html",
    ),
    Page(
        "contact",
        "Contact Us",
        ROOT / "contact.html",
        PREVIEW_DIR / "contact-preview.html",
    ),
)

BODY_CLASSES = {
    "home": "home page-id-12 sjo-preview-page-home",
    "services": "page-id-96 sjo-preview-page-services",
    "contact": "page-id-71 sjo-preview-page-contact",
}


class FragmentStructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.headings: list[int] = []
        self.images: list[dict[str, str | None]] = []
        self.sources: list[dict[str, str | None]] = []
        self.links: list[dict[str, str | None]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        elif tag == "img":
            self.images.append(attributes)
        elif tag == "source":
            self.sources.append(attributes)
        elif tag == "a":
            self.links.append(attributes)


PREVIEW_FORM = """
          <div class="fluentform frm-fluent-form sjo-preview-form-facsimile">
            <p class="sjo-preview-form-note"><strong>Preview form:</strong> Fields are shown for layout review only. This preview does not submit.</p>

            <div class="ff-t-container">
              <div class="ff-t-cell">
                <div class="ff-el-group">
                  <div class="ff-el-input--label"><label for="sjo-preview-first-name">First Name</label></div>
                  <input class="ff-el-form-control" id="sjo-preview-first-name" type="text" autocomplete="given-name" placeholder="First name">
                </div>
              </div>
              <div class="ff-t-cell">
                <div class="ff-el-group">
                  <div class="ff-el-input--label"><label for="sjo-preview-last-name">Last Name</label></div>
                  <input class="ff-el-form-control" id="sjo-preview-last-name" type="text" autocomplete="family-name" placeholder="Last name">
                </div>
              </div>
            </div>

            <div class="ff-el-group">
              <div class="ff-el-input--label"><label for="sjo-preview-company">Company</label></div>
              <input class="ff-el-form-control" id="sjo-preview-company" type="text" autocomplete="organization" placeholder="Company name">
            </div>

            <div class="ff-t-container">
              <div class="ff-t-cell">
                <div class="ff-el-group">
                  <div class="ff-el-input--label"><label for="sjo-preview-email">Email</label></div>
                  <input class="ff-el-form-control" id="sjo-preview-email" type="email" autocomplete="email" placeholder="name@company.com">
                </div>
              </div>
              <div class="ff-t-cell">
                <div class="ff-el-group">
                  <div class="ff-el-input--label"><label for="sjo-preview-phone">Phone</label></div>
                  <input class="ff-el-form-control" id="sjo-preview-phone" type="tel" autocomplete="tel" placeholder="(555) 555-5555">
                </div>
              </div>
            </div>

            <div class="ff-el-group">
              <div class="ff-el-input--label"><label for="sjo-preview-project-type">Project Type</label></div>
              <select class="ff-el-form-control" id="sjo-preview-project-type">
                <option selected disabled>Select project type</option>
                <option>Owner's Representation</option>
                <option>QA/QC &amp; Inspections</option>
                <option>Construction Management</option>
                <option>Project Controls &amp; Reporting</option>
                <option>Preconstruction Services</option>
                <option>Commissioning Support</option>
                <option>Other</option>
              </select>
            </div>

            <div class="ff-el-group">
              <div class="ff-el-input--label"><label for="sjo-preview-subject">Subject</label></div>
              <input class="ff-el-form-control" id="sjo-preview-subject" type="text" placeholder="How can we help?">
            </div>

            <div class="ff-el-group">
              <div class="ff-el-input--label"><label for="sjo-preview-message">Message</label></div>
              <textarea class="ff-el-form-control" id="sjo-preview-message" rows="6" placeholder="Tell us about your project or how we can help."></textarea>
            </div>

            <button class="ff-btn ff-btn-submit" type="button">SEND MESSAGE</button>
          </div>
""".strip("\n")


PREVIEW_CSS = """
    :root {
      color-scheme: light;
      --preview-ink: #071514;
      --preview-green: #2b9e50;
      --preview-paper: #ffffff;
      --preview-soft: #f4f4f4;
      --preview-line: #d8e0dc;
    }

    *, *::before, *::after { box-sizing: border-box; }

    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      background: var(--preview-soft);
      color: var(--preview-ink);
      font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
    }

    .sjo-preview-notice {
      margin: 0;
      padding: 9px 18px;
      border-bottom: 1px solid #b7d9c1;
      background: #e7f3ea;
      color: #0b4f26;
      font-size: 13px;
      font-weight: 700;
      line-height: 1.4;
      text-align: center;
    }

    .sjo-preview-canvas {
      position: relative;
      min-height: 50vh;
      background: var(--preview-paper);
    }

    .sjo-preview-stage { min-height: 50vh; }

    .sjo-preview-form-note {
      margin: 0 0 20px !important;
      padding: 11px 13px !important;
      border-left: 3px solid var(--preview-green);
      background: #eef7f0;
      color: #234139 !important;
      font-size: 13px !important;
      line-height: 1.5 !important;
    }

    .sjo-preview-form-facsimile .ff-t-container {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }

    .sjo-preview-form-facsimile .ff-t-cell { min-width: 0; }

    @media (max-width: 760px) {
      .sjo-preview-form-facsimile .ff-t-container { grid-template-columns: 1fr; }
    }

    @media (max-width: 420px) {
      .sjo-preview-notice { padding-inline: 12px; }
    }
"""


PREVIEW_SCRIPT = """
    (() => {
      const body = document.body;
      const header = document.getElementById("siteHeader");
      const hamburger = document.getElementById("hamburger");
      const scrim = document.getElementById("sheetScrim");
      const sheet = document.getElementById("mobileSheet");
      const stage = document.querySelector(".sjo-preview-stage");
      const footer = document.getElementById("siteFooter");
      const desktopQuery = window.matchMedia("(min-width: 941px)");
      let previousFocus = null;

      if (!header || !hamburger || !scrim || !sheet) return;

      const setMenu = (isOpen, restoreFocus = false) => {
        if (isOpen) previousFocus = document.activeElement;
        body.classList.toggle("menu-open", isOpen);
        hamburger.setAttribute("aria-expanded", String(isOpen));
        hamburger.setAttribute(
          "aria-label",
          isOpen ? "Close navigation menu" : "Open navigation menu"
        );
        sheet.setAttribute("aria-hidden", String(!isOpen));
        [stage, footer].forEach((element) => {
          if (element) element.inert = isOpen;
        });

        if (isOpen) {
          window.requestAnimationFrame(() => {
            sheet.querySelector("a")?.focus();
          });
        } else if (restoreFocus && previousFocus instanceof HTMLElement) {
          previousFocus.focus();
        }
      };

      hamburger.addEventListener("click", () => {
        setMenu(!body.classList.contains("menu-open"));
      });
      scrim.addEventListener("click", () => setMenu(false, true));
      sheet.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => setMenu(false));
      });
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && body.classList.contains("menu-open")) {
          setMenu(false, true);
        }
      });
      document.addEventListener("keydown", (event) => {
        if (event.key !== "Tab" || !body.classList.contains("menu-open")) return;
        const focusable = [hamburger, ...sheet.querySelectorAll("a")];
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      });
      const closeAtDesktop = (event) => {
        if (event.matches && body.classList.contains("menu-open")) {
          setMenu(false);
        }
      };
      if (desktopQuery.addEventListener) {
        desktopQuery.addEventListener("change", closeAtDesktop);
      } else {
        desktopQuery.addListener(closeAtDesktop);
      }
      setMenu(false);

      const setScrolled = () => {
        header.classList.toggle("scrolled", window.scrollY > 24);
      };
      setScrolled();
      window.addEventListener("scroll", setScrolled, { passive: true });
    })();
"""


def read_fragment(page: Page) -> str:
    return page.source.read_text(encoding="utf-8")


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def source_digest(*fragments: str) -> str:
    digest = hashlib.sha256()
    for fragment in fragments:
        encoded = fragment.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()


def rewrite_for_preview(fragment: str) -> str:
    rendered = fragment.replace(CDN_BASE, "../assets/images/")
    route_rewrites = (
        ('href="/services/"', 'href="services-preview.html"'),
        ('href="/contact-us/"', 'href="contact-preview.html"'),
        ('href="/"', 'href="home-preview.html"'),
    )
    for source, replacement in route_rewrites:
        rendered = rendered.replace(source, replacement)
    return rendered


def split_fragment(fragment: str, source: Path) -> tuple[str, str]:
    style_matches = list(
        re.finditer(r"<style>(.*?)</style>", fragment, re.IGNORECASE | re.DOTALL)
    )
    if len(style_matches) != 1:
        raise ValueError(f"{source}: expected exactly one style block")
    style_match = style_matches[0]
    styles = style_match.group(1).strip("\n")
    body = (fragment[: style_match.start()] + fragment[style_match.end() :]).strip()
    return styles, body


def preview_page_fragment(page: Page, fragment: str) -> tuple[str, str]:
    rendered = rewrite_for_preview(fragment)

    if page.key == "contact":
        rendered = rendered.replace(FORM_SHORTCODE, PREVIEW_FORM)

    return split_fragment(rendered, page.source)


def preview_shell_fragment(path: Path, fragment: str) -> tuple[str, str]:
    return split_fragment(rewrite_for_preview(fragment), path)


def mark_current_navigation(header_body: str, page: Page) -> str:
    pattern = re.compile(
        rf'(<a\b(?=[^>]*\bdata-nav="{re.escape(page.key)}")[^>]*)(>)',
        re.IGNORECASE,
    )
    return pattern.sub(r'\1 aria-current="page"\2', header_body)


def render_preview(
    page: Page,
    fragment: str,
    header_fragment: str,
    footer_fragment: str,
) -> str:
    bundle_digest = source_digest(header_fragment, fragment, footer_fragment)
    header_digest = source_digest(header_fragment)
    page_digest = source_digest(fragment)
    footer_digest = source_digest(footer_fragment)

    header_styles, header_body = preview_shell_fragment(
        HEADER_SOURCE, header_fragment
    )
    page_styles, page_body = preview_page_fragment(page, fragment)
    footer_styles, footer_body = preview_shell_fragment(
        FOOTER_SOURCE, footer_fragment
    )
    header_body = mark_current_navigation(header_body, page)

    return f"""<!DOCTYPE html>
<!-- SJO_PREVIEW_BUNDLE_SHA256: {bundle_digest} -->
<!-- SJO_PREVIEW_HEADER_SHA256: {header_digest} -->
<!-- SJO_PREVIEW_PAGE_SHA256: {page_digest} -->
<!-- SJO_PREVIEW_FOOTER_SHA256: {footer_digest} -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>{page.title} | SJO Local Preview</title>
  <style>
{PREVIEW_CSS}
    /* Production managed-header styles, hoisted for valid standalone HTML. */
{header_styles}

    /* Current production page-fragment styles, hoisted for valid standalone HTML. */
{page_styles}

    /* Production managed-footer styles, hoisted for valid standalone HTML. */
{footer_styles}
  </style>
</head>
<body class="{BODY_CLASSES[page.key]}" data-sjo-page="{page.key}">
  <p class="sjo-preview-notice" role="note">Preview only: the GitPress Managed header and footer shown are production fragments. The WordPress canvas is simulated locally, and the Contact form does not submit.</p>

  <div class="sjo-preview-canvas">
{header_body}

    <div class="sjo-preview-stage">
{page_body}
    </div>

{footer_body}
  </div>

  <script>
{PREVIEW_SCRIPT}
  </script>
</body>
</html>
"""


def fragment_errors(page: Page, fragment: str) -> list[str]:
    errors: list[str] = []
    label = page.source.relative_to(ROOT.parent).as_posix()

    if not re.match(r"\A<!--\s*SJO_[A-Z]+_VERSION:\s*[^>]+-->\s*", fragment):
        errors.append(f"{label}: missing top-of-file SJO version marker")

    shell_patterns = {
        "doctype": r"<!doctype\b",
        "html/head/body shell tag": r"<\s*/?\s*(?:html|head|body)\b",
        "theme header/footer tag": r"<\s*/?\s*(?:header|footer)\b",
    }
    for description, pattern in shell_patterns.items():
        if re.search(pattern, fragment, re.IGNORECASE):
            errors.append(f"{label}: production fragment contains {description}")

    if len(re.findall(r"<\s*main\b", fragment, re.IGNORECASE)) != 1:
        errors.append(f"{label}: production fragment must contain exactly one main root")

    expected_root = rf'<main\b[^>]*class="[^"]*\bsjo-page\b[^"]*\bsjo-{page.key}\b'
    if not re.search(expected_root, fragment, re.IGNORECASE):
        errors.append(f"{label}: main root is missing sjo-page and sjo-{page.key} classes")

    if re.search(r"<\s*/?\s*article\b", fragment, re.IGNORECASE):
        errors.append(f"{label}: visual components must not use article elements")

    if re.search(r"<\s*script\b", fragment, re.IGNORECASE):
        errors.append(f"{label}: production fragment must not require inline JavaScript")

    if re.search(r"(?:fetch\s*\(|(?:header|footer)\.html|site-(?:header|footer))", fragment, re.IGNORECASE):
        errors.append(f"{label}: possible header/footer injection detected")

    if re.search(r'(?:href|action)\s*=\s*["\'][^"\']+\.html(?:[?#][^"\']*)?["\']', fragment, re.IGNORECASE):
        errors.append(f"{label}: production navigation contains a .html link")

    if fragment.count("<style>") != 1 or fragment.count("</style>") != 1:
        errors.append(f"{label}: production fragment must contain one scoped style block")

    if any(token in fragment for token in ("â€™", "â€œ", "â€", "Ã", "Â", "�")):
        errors.append(f"{label}: mojibake or replacement characters detected")

    structure = FragmentStructureParser()
    structure.feed(fragment)
    if structure.headings.count(1) != 1:
        errors.append(f"{label}: production fragment must contain exactly one h1")
    if structure.headings and structure.headings[0] != 1:
        errors.append(f"{label}: first heading must be h1")
    for previous, current in zip(structure.headings, structure.headings[1:]):
        if current - previous > 1:
            errors.append(
                f"{label}: heading order jumps from h{previous} to h{current}"
            )
            break

    for image in structure.images:
        source = image.get("src") or "unnamed image"
        if "alt" not in image or not (image.get("alt") or "").strip():
            errors.append(f"{label}: useful alt text is required for {source}")
        for dimension in ("width", "height"):
            value = image.get(dimension) or ""
            if not value.isdigit() or int(value) <= 0:
                errors.append(f"{label}: valid {dimension} is required for {source}")

    for source_element in structure.sources:
        source = source_element.get("srcset") or "unnamed responsive source"
        for dimension in ("width", "height"):
            value = source_element.get(dimension) or ""
            if not value.isdigit() or int(value) <= 0:
                errors.append(f"{label}: valid {dimension} is required for {source}")

    for link in structure.links:
        href = link.get("href") or ""
        if not href:
            errors.append(f"{label}: anchor is missing href")
        if link.get("target") == "_blank" and "noopener" not in (link.get("rel") or ""):
            errors.append(f"{label}: target=_blank link is missing rel=noopener")

    style_blocks = re.findall(r"<style>(.*?)</style>", fragment, re.IGNORECASE | re.DOTALL)
    for style in style_blocks:
        if style.count("{") != style.count("}"):
            errors.append(f"{label}: unbalanced CSS braces")
        if re.search(r"!\s+important\b|;;", style, re.IGNORECASE):
            errors.append(f"{label}: common CSS punctuation corruption detected")
        if re.search(r"@import[^;]*(?:&|&amp;)", style, re.IGNORECASE):
            errors.append(f"{label}: unsafe ampersand in a fragment font import")
        if ":focus-visible" not in style:
            errors.append(f"{label}: keyboard focus-visible styling is missing")
        if "@media (max-width" not in style:
            errors.append(f"{label}: responsive max-width rules are missing")
        if "prefers-reduced-motion" not in style:
            errors.append(f"{label}: reduced-motion handling is missing")
        for alpha in re.findall(
            r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*([0-9.]+)\s*\)",
            style,
            re.IGNORECASE,
        ):
            try:
                if float(alpha) > 1:
                    errors.append(f"{label}: rgba alpha must be between 0 and 1")
            except ValueError:
                errors.append(f"{label}: malformed rgba alpha value")

    if page.key == "contact":
        if fragment.count(FORM_SHORTCODE) != 1:
            errors.append(f"{label}: approved Fluent Forms shortcode must appear exactly once")
        if LEGACY_FORM_MARKER in fragment:
            errors.append(f"{label}: legacy pending form marker must be removed")
        if "mailto:" in fragment or re.search(
            r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", fragment
        ):
            errors.append(f"{label}: pending contact email must not be published")
        if re.search(r"<a\b[^>]*>[^<]*Privacy Policy", fragment, re.IGNORECASE):
            errors.append(f"{label}: pending Privacy Policy must remain unlinked")
    elif FORM_SHORTCODE in fragment or LEGACY_FORM_MARKER in fragment:
        errors.append(f"{label}: unexpected contact form embed")

    if page.key == "services" and len(
        re.findall(r'<li\b[^>]*class="[^"]*\bsjo-service\b', fragment)
    ) != 6:
        errors.append(f"{label}: services page must contain exactly six service blocks")

    if page.key == "home":
        if len(
            re.findall(r'<div\b[^>]*class="sjo-home__value"', fragment)
        ) != 4:
            errors.append(f"{label}: home page must contain exactly four values")
        if len(
            re.findall(
                r'<li\b[^>]*class="sjo-home__affiliation-item"',
                fragment,
            )
        ) != 3:
            errors.append(f"{label}: home page must contain three affiliation items")
        affiliation_logos = {
            "2-LINE-UW-First-RGB-United-Way-Logo-Localization-Tool.webp": (
                "United Way of Central Eastern California"
            ),
            "bakersfield-chamber.png": (
                "Greater Bakersfield Chamber of Commerce"
            ),
            "KEDC-Final-Logo-wTagLine-1024x289.png": (
                "Kern Economic Development Corporation"
            ),
        }
        for filename, alt_text in affiliation_logos.items():
            if filename not in fragment:
                errors.append(f"{label}: missing approved affiliation logo: {filename}")
            if f'alt="{alt_text}"' not in fragment:
                errors.append(
                    f"{label}: affiliation logo requires approved alt text: {alt_text}"
                )
        if "PENDING LOGO" in fragment:
            errors.append(f"{label}: outdated affiliation-logo placeholder remains")

    for filename in re.findall(re.escape(CDN_BASE) + r"([^\"')\s]+)", fragment):
        asset = ROOT / "assets" / "images" / filename
        if not asset.is_file():
            errors.append(f"{label}: referenced asset is missing: {filename}")

    return errors


def shell_errors(kind: str, path: Path, fragment: str) -> list[str]:
    errors: list[str] = []
    label = path.relative_to(ROOT.parent).as_posix()
    opposite = "footer" if kind == "header" else "header"

    expected_marker = rf"\A<!--\s*SJO_{kind.upper()}_VERSION:\s*[^>]+-->\s*"
    if not re.match(expected_marker, fragment):
        errors.append(f"{label}: missing top-of-file SJO {kind} version marker")

    forbidden_patterns = {
        "doctype": r"<!doctype\b",
        "html/head/body document tag": r"<\s*/?\s*(?:html|head|body)\b",
        "page main tag": r"<\s*/?\s*main\b",
        f"{opposite} tag": rf"<\s*/?\s*{opposite}\b",
        "inline script": r"<\s*script\b",
        "fragment injection": r"(?:fetch\s*\(|(?:header|footer)\.html)",
    }
    for description, pattern in forbidden_patterns.items():
        if re.search(pattern, fragment, re.IGNORECASE):
            errors.append(f"{label}: production shell contains {description}")

    if len(re.findall(rf"<\s*{kind}\b", fragment, re.IGNORECASE)) != 1:
        errors.append(f"{label}: production shell must contain exactly one {kind}")

    if fragment.count("<style>") != 1 or fragment.count("</style>") != 1:
        errors.append(f"{label}: production shell must contain one style block")

    if FORM_SHORTCODE in fragment or LEGACY_FORM_MARKER in fragment:
        errors.append(f"{label}: contact form embed does not belong in the site shell")

    if re.search(
        r'(?:href|action)\s*=\s*["\'][^"\']+\.html(?:[?#][^"\']*)?["\']',
        fragment,
        re.IGNORECASE,
    ):
        errors.append(f"{label}: production shell navigation contains a .html link")

    if any(
        token in fragment
        for token in ("Ã¢â‚¬â„¢", "Ã¢â‚¬Å“", "Ã¢â‚¬", "Ãƒ", "Ã‚", "ï¿½")
    ):
        errors.append(f"{label}: mojibake or replacement characters detected")

    structure = FragmentStructureParser()
    structure.feed(fragment)
    if 1 in structure.headings:
        errors.append(f"{label}: global shell must not contain an h1")

    for image in structure.images:
        source = image.get("src") or "unnamed image"
        if "alt" not in image:
            errors.append(f"{label}: alt attribute is required for {source}")
        if kind == "footer" and not (image.get("alt") or "").strip():
            errors.append(f"{label}: footer brand image requires useful alt text")
        for dimension in ("width", "height"):
            value = image.get(dimension) or ""
            if not value.isdigit() or int(value) <= 0:
                errors.append(f"{label}: valid {dimension} is required for {source}")

    for link in structure.links:
        href = link.get("href") or ""
        if not href:
            errors.append(f"{label}: anchor is missing href")
        if link.get("target") == "_blank" and "noopener" not in (
            link.get("rel") or ""
        ):
            errors.append(f"{label}: target=_blank link is missing rel=noopener")

    approved_shell_hrefs = {
        "/",
        "/services/",
        "/contact-us/",
        "tel:+16618660219",
        "https://www.linkedin.com/company/sanjoaquin-operators",
    }
    for link in structure.links:
        href = link.get("href") or ""
        if href and href not in approved_shell_hrefs:
            errors.append(f"{label}: unapproved shell destination: {href}")

    style_blocks = re.findall(
        r"<style>(.*?)</style>", fragment, re.IGNORECASE | re.DOTALL
    )
    for style in style_blocks:
        if style.count("{") != style.count("}"):
            errors.append(f"{label}: unbalanced CSS braces")
        if re.search(r"!\s+important\b|;;", style, re.IGNORECASE):
            errors.append(f"{label}: common CSS punctuation corruption detected")
        if re.search(r"@import[^;]*(?:&|&amp;)", style, re.IGNORECASE):
            errors.append(f"{label}: unsafe ampersand in a shell font import")
        if ":focus-visible" not in style:
            errors.append(f"{label}: keyboard focus-visible styling is missing")
        if "@media (max-width" not in style:
            errors.append(f"{label}: responsive max-width rules are missing")
        if "prefers-reduced-motion" not in style:
            errors.append(f"{label}: reduced-motion handling is missing")
        for alpha in re.findall(
            r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*([0-9.]+)\s*\)",
            style,
            re.IGNORECASE,
        ):
            try:
                if float(alpha) > 1:
                    errors.append(f"{label}: rgba alpha must be between 0 and 1")
            except ValueError:
                errors.append(f"{label}: malformed rgba alpha value")

    for filename in re.findall(re.escape(CDN_BASE) + r"([^\"')\s]+)", fragment):
        asset = ROOT / "assets" / "images" / filename
        if not asset.is_file():
            errors.append(f"{label}: referenced asset is missing: {filename}")

    if "mailto:" in fragment or re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", fragment
    ):
        errors.append(f"{label}: pending contact email must not be published")

    if re.search(r"<a\b[^>]*>[^<]*Privacy Policy", fragment, re.IGNORECASE):
        errors.append(f"{label}: pending Privacy Policy must remain unlinked")

    if kind == "header":
        required_ids = ("siteHeader", "hamburger", "sheetScrim", "mobileSheet")
        for element_id in required_ids:
            if len(
                re.findall(
                    rf'\bid=["\']{re.escape(element_id)}["\']',
                    fragment,
                    re.IGNORECASE,
                )
            ) != 1:
                errors.append(f"{label}: required #{element_id} hook must appear once")

        if not re.search(
            r'class=["\'][^"\']*\bsite-header\b[^"\']*["\']',
            fragment,
            re.IGNORECASE,
        ):
            errors.append(f"{label}: required .site-header hook is missing")
        if not re.search(
            r'class=["\'][^"\']*\bmobile-sheet\b[^"\']*["\']',
            fragment,
            re.IGNORECASE,
        ):
            errors.append(f"{label}: required .mobile-sheet hook is missing")

        nav_values = [
            value
            for link in structure.links
            if (value := link.get("data-nav")) is not None
        ]
        for nav_key in ("home", "services", "contact"):
            if nav_values.count(nav_key) != 2:
                errors.append(
                    f"{label}: data-nav={nav_key} must appear in desktop and mobile navigation"
                )
        expected_nav_hrefs = {
            "home": "/",
            "services": "/services/",
            "contact": "/contact-us/",
        }
        for link in structure.links:
            nav_key = link.get("data-nav")
            if nav_key in expected_nav_hrefs and link.get("href") != expected_nav_hrefs[nav_key]:
                errors.append(
                    f"{label}: data-nav={nav_key} must link to {expected_nav_hrefs[nav_key]}"
                )

        button = re.search(
            r'<button\b(?=[^>]*\bid=["\']hamburger["\'])[^>]*>',
            fragment,
            re.IGNORECASE,
        )
        if not button:
            errors.append(f"{label}: hamburger must be a button")
        else:
            button_markup = button.group(0)
            for attribute in (
                r'\btype=["\']button["\']',
                r'\baria-controls=["\']mobileSheet["\']',
                r'\baria-expanded=["\']false["\']',
                r'\baria-label=["\'][^"\']+["\']',
            ):
                if not re.search(attribute, button_markup, re.IGNORECASE):
                    errors.append(
                        f"{label}: hamburger is missing an accessible control attribute"
                    )
                    break

        for state_hook in ("body.menu-open", ".scrolled"):
            if state_hook not in fragment:
                errors.append(f"{label}: required {state_hook} state hook is missing")

    else:
        if 'id="siteFooter"' not in fragment:
            errors.append(f"{label}: footer root must use id=siteFooter")
        for required_copy in (
            "tel:+16618660219",
            "California and Western U.S.",
            "https://www.linkedin.com/company/sanjoaquin-operators",
            "United Way of Central Eastern California",
            "Greater Bakersfield Chamber of Commerce",
            "Kern Economic Development Corporation",
        ):
            if required_copy not in fragment:
                errors.append(f"{label}: missing approved footer content: {required_copy}")
        if re.search(
            r"Business Park|5401\b|#208\b|93309\b", fragment, re.IGNORECASE
        ):
            errors.append(f"{label}: screenshot-only street address must remain unpublished")
        affiliation_match = re.search(
            r'<ul\b[^>]*class="[^"]*\bsjo-site-footer__affiliations\b[^"]*"[^>]*>(.*?)</ul>',
            fragment,
            re.IGNORECASE | re.DOTALL,
        )
        if not affiliation_match or len(
            re.findall(r"<li\b", affiliation_match.group(1), re.IGNORECASE)
        ) != 3:
            errors.append(f"{label}: footer must contain three affiliation fallbacks")

    return errors


def validate_fragments() -> tuple[dict[str, str], dict[str, str], list[str]]:
    fragments: dict[str, str] = {}
    shells: dict[str, str] = {}
    errors: list[str] = []
    for page in PAGES:
        if not page.source.is_file():
            errors.append(f"missing production fragment: {page.source}")
            continue
        try:
            fragment = read_fragment(page)
        except UnicodeDecodeError as exc:
            errors.append(f"{page.source}: not valid UTF-8 ({exc})")
            continue
        fragments[page.key] = fragment
        errors.extend(fragment_errors(page, fragment))

    for kind, path in (("header", HEADER_SOURCE), ("footer", FOOTER_SOURCE)):
        if not path.is_file():
            errors.append(f"missing production shell fragment: {path}")
            continue
        try:
            fragment = read_source(path)
        except UnicodeDecodeError as exc:
            errors.append(f"{path}: not valid UTF-8 ({exc})")
            continue
        shells[kind] = fragment
        errors.extend(shell_errors(kind, path, fragment))

    return fragments, shells, errors


def check_previews(
    fragments: dict[str, str], shells: dict[str, str]
) -> list[str]:
    errors: list[str] = []
    for page in PAGES:
        if page.key not in fragments or "header" not in shells or "footer" not in shells:
            continue
        expected = render_preview(
            page, fragments[page.key], shells["header"], shells["footer"]
        )
        if not page.preview.is_file():
            errors.append(f"missing preview: {page.preview}")
            continue
        actual = page.preview.read_text(encoding="utf-8")
        if not actual.startswith("<!DOCTYPE html>\n"):
            errors.append(f"{page.preview}: missing leading HTML5 doctype")
        expected_digests = {
            "BUNDLE": source_digest(
                shells["header"], fragments[page.key], shells["footer"]
            ),
            "HEADER": source_digest(shells["header"]),
            "PAGE": source_digest(fragments[page.key]),
            "FOOTER": source_digest(shells["footer"]),
        }
        for digest_name, expected_digest in expected_digests.items():
            digest_match = re.search(
                rf"SJO_PREVIEW_{digest_name}_SHA256:\s*([0-9a-f]{{64}})", actual
            )
            if not digest_match or digest_match.group(1) != expected_digest:
                errors.append(
                    f"{page.preview}: stale or missing {digest_name.lower()} hash"
                )
        if actual != expected:
            errors.append(f"{page.preview}: stale or manually edited; rebuild previews")
        if len(re.findall(r"<header\b", actual, re.IGNORECASE)) != 1:
            errors.append(f"{page.preview}: managed header must render exactly once")
        if len(re.findall(r"<footer\b", actual, re.IGNORECASE)) != 1:
            errors.append(f"{page.preview}: managed footer must render exactly once")
        if "sjo-preview-header" in actual or "sjo-preview-footer" in actual:
            errors.append(f"{page.preview}: obsolete shell facsimile markup remains")
        if page.key == "contact":
            if FORM_SHORTCODE in actual or 'type="button">SEND MESSAGE' not in actual:
                errors.append(f"{page.preview}: contact form facsimile is not safely rendered")
            if re.search(r"<\s*form\b", actual, re.IGNORECASE):
                errors.append(f"{page.preview}: preview contact controls must not submit")
    return errors


def print_errors(errors: list[str]) -> None:
    print("SJO preview validation failed:", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate fragments and verify that generated previews are current",
    )
    args = parser.parse_args()

    fragments, shells, errors = validate_fragments()
    if errors:
        print_errors(errors)
        return 1

    if args.check:
        errors = check_previews(fragments, shells)
        if errors:
            print_errors(errors)
            return 1
        print("SJO preview check passed for home, services, and contact.")
        return 0

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        rendered = render_preview(
            page, fragments[page.key], shells["header"], shells["footer"]
        )
        with page.preview.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
        print(f"built {page.preview.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
