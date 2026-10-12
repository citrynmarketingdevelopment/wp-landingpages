"""Rebuild the Amicus GitPress fragments and asset inventory from public pages.

The checked-in HTML is the deployable artifact. This importer is for audits and
controlled refreshes; it does not alter the WordPress site.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup, Comment


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://amicusfoundation.com"
OWNER = "citrynmarketingdevelopment"
REPO = "wp-landingpages"
BRANCH = "main"
UA = {"User-Agent": "Mozilla/5.0 (compatible; AmicusMigration/1.0)"}
CONTACT_TOKEN = "__AMICUS_CONTACT_FORM_ID__"
PAGE_SLUGS = [
    "", "zakouma", "ww2-memorial", "contact-us",
    "dolly-parton-imagination", "warriors-quiet-waters",
    "montana-wild-sheep-foundation", "returning-charities-application",
    "bakersfield-pregnancy-center", "independence-through-grace",
    "recommended-charities", "grant-forms", "new-charities-application",
    "montana-classrooms",
]
EXTRA_SLUGS = ["project/test"]


def fetch(url: str) -> bytes:
    parts = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, urllib.parse.quote(parts.path, safe="/%"), parts.query, parts.fragment))
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def get_page(slug: str) -> tuple[str, BeautifulSoup]:
    url = f"{ORIGIN}/{slug + '/' if slug else ''}"
    if not slug:
        saved = ROOT / "references" / "Amicus Foundation _ Matching Grants for Charities.html"
    elif slug == "recommended-charities":
        saved = ROOT / "references" / "Recommended Charities-Amicus Foundation.html"
    else:
        saved = None
    raw = saved.read_bytes() if saved and saved.exists() else fetch(url)
    return url, BeautifulSoup(raw, "lxml")


def localize_links(tag: BeautifulSoup) -> None:
    for node in tag.select("a[href]"):
        href = node.get("href", "")
        if href.startswith(ORIGIN + "/"):
            node["href"] = href[len(ORIGIN):]
        elif href == ORIGIN:
            node["href"] = "/"


def extract_inline_styles(tag: BeautifulSoup) -> str:
    rules = []
    for idx, node in enumerate(tag.select("[style]")):
        declaration = node.get("style", "").strip().rstrip(";")
        del node["style"]
        if not declaration:
            continue
        cls = f"amicus-inline-{idx}"
        node["class"] = list(node.get("class", [])) + [cls]
        rules.append(f".{cls}{{{declaration};}}")
    return "\n".join(rules)


def strip_executable_nodes(tag: BeautifulSoup) -> None:
    for node in tag.select("script, style, noscript"):
        node.decompose()
    for node in tag.find_all(True):
        for key in list(node.attrs):
            if key.lower().startswith("on"):
                del node[key]


def add_shortcode(soup: BeautifulSoup, parent, shortcode: str) -> None:
    parent.append(soup.new_string("\n" + shortcode + "\n"))


def replace_forms(soup: BeautifulSoup, slug: str, content) -> None:
    if slug in ("contact-us", "recommended-charities"):
        forms = content.select("form")
        for form in forms:
            host = form.find_parent(class_=re.compile("et_pb_contact_form_container")) or form
            holder = soup.new_tag("div", attrs={"class": "amicus-contact-form"})
            add_shortcode(soup, holder, f'[gitpress_form id="{CONTACT_TOKEN}"]')
            add_shortcode(soup, holder, f'[amicus_form_status id="{CONTACT_TOKEN}"]')
            host.replace_with(holder)
    if slug in ("new-charities-application", "returning-charities-application"):
        form_id = "230195983314055" if slug.startswith("new") else "250696793084167"
        scripts = content.select('script[src*="form.jotform.com/jsform/"]')
        if scripts:
            for script in scripts:
                holder = soup.new_tag("div", attrs={"class": "amicus-jotform"})
                add_shortcode(soup, holder, f'[amicus_jotform id="{form_id}"]')
                script.replace_with(holder)
        else:
            host = content.select_one(".et_pb_code_inner") or content
            add_shortcode(soup, host, f'[amicus_jotform id="{form_id}"]')
    if slug == "project/test":
        for form in content.select("form"):
            form.decompose()
        add_shortcode(soup, content, "[amicus_comments]")


def replace_embeds(soup: BeautifulSoup, content) -> None:
    for frame in content.select("iframe[src]"):
        source = urllib.parse.urlparse(frame.get("src", ""))
        if source.netloc not in ("www.youtube.com", "youtube.com"):
            continue
        match = re.fullmatch(r"/embed/([A-Za-z0-9_-]{11})", source.path)
        if not match:
            continue
        holder = soup.new_tag("div", attrs={"class": "amicus-video-embed"})
        add_shortcode(soup, holder, f'[amicus_youtube id="{match.group(1)}"]')
        frame.replace_with(holder)


def preserve_interactions(soup: BeautifulSoup, content) -> None:
    for row in content.select(".et_pb_row"):
        columns = sum("et_pb_column" in child.get("class", []) for child in row.find_all(recursive=False) if child.name)
        if columns in (4, 5, 6):
            generated = f"et_pb_row_{columns}col"
            if generated not in row.get("class", []):
                row["class"] = list(row.get("class", [])) + [generated]
    for row in content.select(".et_pb_row_inner"):
        widths = []
        for child in row.find_all(recursive=False):
            if "et_pb_column_inner" not in child.get("class", []):
                continue
            match = next((re.fullmatch(r"et_pb_column_([0-9]+)_([0-9]+)", c) for c in child.get("class", []) if re.fullmatch(r"et_pb_column_[0-9]+_[0-9]+", c)), None)
            if match:
                widths.append(match.group(1) + "-" + match.group(2))
        if len(widths) > 1:
            generated = "et_pb_row_" + "_".join(widths)
            if generated not in row.get("class", []):
                row["class"] = list(row.get("class", [])) + [generated]
    for toggle in content.select(".et_pb_toggle"):
        summary = toggle.select_one(".et_pb_toggle_title")
        if not summary:
            continue
        was_open = "et_pb_toggle_open" in toggle.get("class", [])
        toggle.name = "details"
        toggle["class"] = [c for c in toggle.get("class", []) if c not in ("et_pb_toggle_open", "et_pb_toggle_close")]
        toggle["class"].append("amicus-toggle")
        if was_open:
            toggle["open"] = ""
        summary.name = "summary"
    for counter in content.select(".et_pb_number_counter"):
        value = counter.get("data-number-value", "")
        display = counter.select_one(".percent-value")
        if display and value:
            display.string = value
    for bar in content.select(".et_pb_counter_amount[data-width]"):
        width = bar.get("data-width", "")
        if re.fullmatch(r"(?:100|[0-9]{1,2})%", width):
            bar["class"] = list(bar.get("class", [])) + ["amicus-progress-fill"]
            bar["data-amicus-width"] = width


def normalize_body(soup: BeautifulSoup, slug: str) -> tuple[str, str]:
    post = soup.select_one(".et-l--post") or soup.select_one("#main-content article")
    if not post:
        raise ValueError(f"missing post body: {slug}")
    post = BeautifulSoup(str(post), "lxml").select_one(".et-l--post, article")
    replace_forms(soup, slug, post)
    replace_embeds(soup, post)
    preserve_interactions(soup, post)
    localize_links(post)
    inline_css = extract_inline_styles(post)
    strip_executable_nodes(post)
    if slug == "project/test":
        post.select_one(".et_builder_inner_content") or post
    content = str(post)
    classes = "amicus-page amicus-home" if not slug else "amicus-page amicus-" + slug.replace("/", "-")
    body = (
        f'<!-- amicus-source: {slug or "home"}; generated from public WordPress HTML -->\n'
        f'<div class="{classes}" data-amicus-route="/{slug + "/" if slug else ""}">'
        f'<div class="entry-content"><div class="et-db et-boc" id="et-boc">{content}</div></div>'
        '</div>\n'
    )
    return body, inline_css


def css_from_source(soup: BeautifulSoup, inline_css: str) -> str:
    chunks = []
    for node in soup.select("style"):
        css = node.string or node.get_text()
        if css and css.strip():
            chunks.append(css)
    chunks.append(inline_css)
    css = "\n".join(chunks)
    # GitPress Managed supplies this wrapper instead of Divi's page-container.
    css = css.replace("#page-container", ".dgs-managed-page")
    return css


def seo_data(soup: BeautifulSoup, slug: str) -> dict:
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    meta = soup.select_one('meta[name="description"]')
    canonical = soup.select_one('link[rel="canonical"]')
    og = soup.select_one('meta[property="og:image"]')
    page = soup.select_one("#main-content article[id]")
    source_post_id = page.get("id", "").removeprefix("post-") if page else ""
    remote = {}
    if source_post_id and "type-page" in page.get("class", []):
        try:
            remote = json.loads(fetch(f"{ORIGIN}/wp-json/wp/v2/pages/{source_post_id}"))
        except (ValueError, urllib.error.URLError):
            remote = {}
    return {
        "title": title,
        "description": meta.get("content", "") if meta else "",
        "canonical": canonical.get("href", "") if canonical else "",
        "og_image": og.get("content", "") if og else "",
        "source_post_id": source_post_id,
        "source_slug": remote.get("slug") or ("test" if slug == "project/test" else ""),
        "source_parent_id": remote.get("parent"),
        "source_status": remote.get("status", "publish"),
    }


def shortcode(path: str) -> str:
    return (
        f'[divi_github_content owner="{OWNER}" repo="{REPO}" '
        f'branch="{BRANCH}" path="amicus/{path}" format="html"]'
    )


def extract_media_urls(soup: BeautifulSoup, css: str) -> set[str]:
    urls = set()
    for node in soup.select("[src], [srcset], [poster], a[href]"):
        for key in ("src", "poster", "href"):
            if node.has_attr(key):
                urls.add(node[key])
        if node.has_attr("srcset"):
            urls.update(part.strip().split(" ")[0] for part in node["srcset"].split(","))
    for item in re.findall(r"url\(([^)]+)\)", css):
        urls.add(item.strip(" \"'"))
    # Favicon links, preload hints and image URLs inside builder data scripts are
    # part of the original asset inventory even when they are not visible in DOM.
    for node in soup.select("link[href]"):
        urls.add(node["href"])
    for item in re.findall(r"(?:https?:)?//amicusfoundation\.com/wp-content/uploads/[^\s\"'<>),;\\]+", str(soup)):
        urls.add(item)
    output = set()
    for raw in urls:
        url = urllib.parse.urljoin(ORIGIN + "/", raw)
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc != "amicusfoundation.com":
            continue
        if parsed.path.startswith("/wp-content/uploads/") or re.search(
            r"/wp-content/themes/Divi/.+\.(?:woff2?|ttf|eot|svg|gif|png|jpe?g|webp)$", parsed.path
        ):
            output.add(ORIGIN + parsed.path)
    return output


def build_header(home: BeautifulSoup) -> str:
    nav = home.select_one("header .et-menu-nav > ul")
    if not nav:
        raise ValueError("source header menu missing")
    nav = BeautifulSoup(str(nav), "lxml").select_one("ul")
    nav["class"] = ["amicus-nav-list"]
    nav.attrs.pop("id", None)
    localize_links(nav)
    for item in nav.select("li"):
        item["class"] = [name for name in item.get("class", []) if not name.startswith("current-") and name != "current_page_item"]
    for link in nav.select("a[href]"):
        link.attrs.pop("aria-current", None)
        href = link.get("href", "")
        if href.startswith("/"):
            link["data-nav"] = href.strip("/") or "home"
    for item in nav.select("li.menu-item-has-children"):
        trigger = item.find("a", recursive=False)
        if trigger:
            trigger["aria-haspopup"] = "true"
            trigger["aria-expanded"] = "false"
            trigger["class"] = list(trigger.get("class", [])) + ["amicus-parent-link"]
    mobile = BeautifulSoup(str(nav), "lxml").select_one("ul")
    mobile["class"] = ["amicus-mobile-list"]
    mobile.attrs.pop("id", None)
    logo = home.select_one("header .et_pb_menu__logo img")
    logo_url = logo.get("src") if logo else f"{ORIGIN}/wp-content/uploads/2022/07/Asset-1.png"
    return f'''<!-- Amicus managed header; interaction is loaded by amicus-site.php -->
<div class="site-header amicus-header" id="siteHeader">
  <div class="amicus-grant-bar"><a href="/grant-forms/">Grants Applications</a></div>
  <div class="amicus-header-inner">
    <a class="amicus-brand" href="/" aria-label="Amicus Foundation, home"><img src="{html.escape(logo_url)}" width="287" height="87" alt="Amicus Foundation"></a>
    <nav class="amicus-desktop-nav" aria-label="Primary">{nav}</nav>
    <a class="amicus-header-cta" href="/grant-forms/">Grants Applications</a>
    <button class="amicus-hamburger" id="hamburger" type="button" aria-label="Open menu" aria-controls="mobileSheet" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <div class="amicus-scrim" id="sheetScrim"></div>
  <nav class="mobile-sheet amicus-mobile-sheet" id="mobileSheet" aria-label="Mobile">{mobile}</nav>
</div>
'''


def build_footer(home: BeautifulSoup) -> str:
    footer = home.select_one("footer")
    if not footer:
        raise ValueError("source footer missing")
    columns = footer.select(".et_pb_row_0_tb_footer > .et_pb_column")
    quick_links = columns[1].select_one(".et_pb_text_inner") if len(columns) > 1 else None
    projects = columns[2].select_one(".et_pb_text_inner") if len(columns) > 2 else None
    quick = str(quick_links) if quick_links else ""
    project = str(projects) if projects else ""
    quick = quick.replace(ORIGIN, "")
    project = project.replace(ORIGIN, "")
    return f'''<!-- Amicus managed footer -->
<div class="amicus-footer">
  <div class="amicus-footer-grid">
    <div class="amicus-footer-brand"><a href="/" aria-label="Amicus Foundation, home"><img src="{ORIGIN}/wp-content/uploads/2022/07/Asset-1.png" width="287" height="87" alt="Amicus Foundation"></a><h5>Email: <a href="mailto:info@amicusfoundation.com">info@amicusfoundation.com</a></h5><a class="amicus-footer-cta" href="/grant-forms/">GrANTS aPPLICATION</a></div>
    <div><h5>Quick Links</h5>{quick}</div>
    <div><h5>Projects</h5>{project}</div>
  </div>
  <div class="amicus-footer-bottom">©2026 Amicus Foundation | All Rights Reserved | Powered &amp; Designed by WestCose Designs</div>
</div>
'''


def save_media(url: str) -> dict:
    parsed = urllib.parse.urlparse(url)
    path = ROOT / "assets" / parsed.path.lstrip("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        data = fetch(url)
        path.write_bytes(data)
    else:
        data = path.read_bytes()
    return {
        "source": url,
        "local": str(path.relative_to(ROOT)).replace("\\", "/"),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-assets", action="store_true")
    args = parser.parse_args()
    (ROOT / "assets" / "css").mkdir(parents=True, exist_ok=True)
    pages = {}
    media = set()
    home = None
    for slug in PAGE_SLUGS + EXTRA_SLUGS:
        url, soup = get_page(slug)
        if not slug:
            home = soup
        body, inline_css = normalize_body(soup, slug)
        file_stem = slug.replace("/", "-") or "home"
        output = f"{file_stem}.html"
        (ROOT / output).write_text(body, encoding="utf-8")
        css = css_from_source(soup, inline_css)
        (ROOT / "assets" / "css" / f"{file_stem}.css").write_text(css, encoding="utf-8")
        media.update(extract_media_urls(soup, css))
        pages["/" + slug + "/" if slug else "/"] = {
            "source_url": url,
            "file": output,
            "css": f"assets/css/{file_stem}.css",
            "shortcode": shortcode(output),
            "render_mode": "gitpress_managed",
            "render_position": "replace",
            "full_page_canvas": True,
            "full_width_content": False,
            "seo": seo_data(soup, slug),
        }
        print(f"{url} -> {output} ({len(body)} chars)")
    assert home is not None
    (ROOT / "header.html").write_text(build_header(home), encoding="utf-8")
    (ROOT / "footer.html").write_text(build_footer(home), encoding="utf-8")
    manifest = {
        "origin": ORIGIN,
        "owner": OWNER,
        "repo": REPO,
        "branch": BRANCH,
        "managed_header_shortcode": shortcode("header.html"),
        "managed_footer_shortcode": shortcode("footer.html"),
        "pages": pages,
        "archives": {
            "/project/": {"handler": "native-project-archive", "source_url": ORIGIN + "/project/", "file": "project-archive.html", "shortcode": shortcode("project-archive.html")},
            "/author/amicus/": {"handler": "native-author-archive", "source_url": ORIGIN + "/author/amicus/", "file": "author-amicus.html", "shortcode": shortcode("author-amicus.html")},
        },
        "redirects": {"/layout_tag/light/": "/"},
    }
    (ROOT / "routes.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.download_assets:
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            for result in pool.map(save_media, sorted(media)):
                results.append(result)
        (ROOT / "assets" / "manifest.json").write_text(
            json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"Downloaded {len(results)} assets, {sum(item['bytes'] for item in results):,} bytes")
    else:
        (ROOT / "assets" / "sources.json").write_text(json.dumps(sorted(media), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
