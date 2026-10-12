"""Build Optimax GitPress event partials and standalone previews.

Run from any directory: python optimax/events/build.py
Requires Pillow for web-optimized copies of the supplied photos.
"""

import argparse
from datetime import date, datetime
from html import escape
import json
from pathlib import Path
import re
from string import Template
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "events"
TEMPLATES = EVENTS / "templates"
ASSET_BASE = (
    "https://raw.githubusercontent.com/citrynmarketingdevelopment/"
    "wp-landingpages/main/optimax/events/assets/"
)
NAVIGATION = [
    ("/about-us/", "About Us"),
    ("/consulting-services/", "Services"),
    ("/revenue-cycle-management/", "Revenue Cycle"),
    ("/credentialing/", "Credentialing"),
    ("/resources/", "Resources"),
    ("/events/", "Events"),
]


def render(template_name, **values):
    return Template((TEMPLATES / template_name).read_text(encoding="utf-8")).substitute(values)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = "\n".join(line.rstrip() for line in content.strip().splitlines())
    path.write_text(clean + "\n", encoding="utf-8")


def text(value):
    return escape(str(value), quote=True)


def safe_url(value):
    parsed = urlparse(value)
    if value.startswith("/") and not value.startswith("//"):
        return text(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"Use an HTTPS or site-relative URL: {value}")
    return text(value)


def image_html(filename, alt, eager=False):
    # Preserve originals; generate compressed copies with their entire artwork intact.
    source = (EVENTS / filename).resolve()
    if source.parent != EVENTS or not source.is_file():
        raise ValueError(f"Event image must be an existing file in optimax/events: {filename}")
    destination = EVENTS / "assets" / (source.stem + ".webp")
    destination.parent.mkdir(exist_ok=True)
    with Image.open(source) as original:
        optimized = ImageOps.exif_transpose(original).convert("RGB")
        optimized.thumbnail((1280, 1708))
        optimized.save(destination, format="WEBP", quality=86, method=6)
        width, height = optimized.size
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        f'<img src="{ASSET_BASE}{text(destination.name)}" alt="{text(alt)}" '
        f'width="{width}" height="{height}" {loading} decoding="async">'
    )


def date_html(event):
    return f'<time datetime="{event["start_date"]}">{text(event["date_label"])}</time>'


def card(event, today):
    past = date.fromisoformat(event["end_date"]) < today
    summary = event.get("past_summary", event["summary"]) if past else event["summary"]
    return f'''<a class="ev-event-card" href="/{text(event['slug'])}/" aria-labelledby="card-{text(event['slug'])}">
      <div class="ev-card-media">{image_html(event['image'], event['image_alt'])}</div>
      <div class="ev-card-copy">
        <p class="ev-eyebrow">{text(event['category'])}</p>
        <h3 id="card-{text(event['slug'])}">{text(event['name'])}</h3>
        <div class="ev-card-meta"><span>{date_html(event)}</span><span>{text(event['location'])}</span></div>
        <p class="ev-card-description">{text(summary)}</p>
        <span class="ev-card-link">Explore event <span aria-hidden="true">&rarr;</span></span>
      </div>
    </a>'''


def topics_html(event):
    if not event.get("topics"):
        return ""
    rows = "".join(
        f'<div class="ev-topic"><h3><a href="{safe_url(topic["url"])}">'
        f'{text(topic["title"])} <span aria-hidden="true">&rarr;</span></a></h3>'
        f'<p>{text(topic["copy"])}</p></div>'
        for topic in event["topics"]
    )
    return f'<div class="ev-wrap ev-topics">{rows}</div>'


def gallery_html(event):
    if not event.get("gallery_image"):
        return ""
    image = image_html(event["gallery_image"], event["gallery_alt"])
    return f'''<section class="ev-section" aria-labelledby="gallery-heading">
      <div class="ev-wrap ev-gallery-grid">
        <figure class="ev-gallery-image">{image}</figure>
        <div class="ev-gallery-copy"><p class="ev-eyebrow">Meet the Optimax team</p>
          <h2 id="gallery-heading">{text(event['gallery_heading'])}</h2>
          <p>{text(event['gallery_copy'])}</p>
          <a class="ev-btn ev-btn-blue" href="/contact-us/">Start a conversation</a>
        </div>
      </div>
    </section>'''


def event_page(event, today, styles):
    past = date.fromisoformat(event["end_date"]) < today
    status = "Past event" if past else (
        "Happening now" if date.fromisoformat(event["start_date"]) <= today else "Upcoming event"
    )
    values = {key: text(value) for key, value in event.items() if isinstance(value, str)}
    # Future/past copy keeps pages reusable after an event has ended.
    for key in ("headline", "intro", "detail_label", "detail", "body", "cta_heading", "cta_copy"):
        if past and event.get("past_" + key):
            values[key] = text(event["past_" + key])
    values.update(
        build_date=today.isoformat(), styles=styles, status=status,
        hero_image=image_html(event["image"], event["image_alt"], eager=True),
        date_html=date_html(event), topics_html=topics_html(event),
        gallery_html=gallery_html(event),
        note_html=f'<p class="ev-note">{text(event["note"])}</p>' if event.get("note") else "",
        organizer_url=safe_url(event["organizer_url"]),
    )
    return render("event.html", **values)


def preview(content, title, description, main_id, today, routes, active=True):
    current = "page" if main_id == "opx-events" else "location"
    nav = "".join(
        f'<a href="{url}"' + (f' class="pv-current" aria-current="{current}"' if active and url == "/events/" else "")
        + f'>{label}</a>' for url, label in NAVIGATION
    )
    result = render(
        "preview.html", content=content, title=text(title), description=text(description),
        main_id=main_id, nav_links=nav, year=today.year,
    )
    # Previews link to other previews; unrelated WordPress links go to the live site.
    result = result.replace(ASSET_BASE, "../events/assets/")
    def local_link(match):
        url = match.group(1)
        return f'href="{routes.get(url, "https://optimaxcs.net" + url)}"'
    return re.sub(r'href="(/[^\"]*)"', local_link, result)


def validate(events):
    slugs = set()
    for event in events:
        slug = event["slug"]
        if not re.fullmatch(r"event-[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in slugs:
            raise ValueError(f"Event slugs must be unique, lowercase and start with event-: {slug}")
        slugs.add(slug)
        if date.fromisoformat(event["start_date"]) > date.fromisoformat(event["end_date"]):
            raise ValueError(f"Event end date precedes start date: {slug}")
        safe_url(event["organizer_url"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--today", type=date.fromisoformat, help="Override the Pacific calendar date (YYYY-MM-DD).")
    args = parser.parse_args()
    today = args.today or datetime.now(ZoneInfo("America/Los_Angeles")).date()
    events = json.loads((EVENTS / "events.json").read_text(encoding="utf-8-sig"))["events"]
    validate(events)
    styles = (TEMPLATES / "events.css").read_text(encoding="utf-8").strip()
    upcoming = sorted((e for e in events if date.fromisoformat(e["end_date"]) >= today), key=lambda e: e["start_date"])
    past = sorted((e for e in events if date.fromisoformat(e["end_date"]) < today), key=lambda e: e["end_date"], reverse=True)
    past_section = ""
    if past:
        past_section = f'''<section class="ev-section ev-past" aria-labelledby="past-heading">
          <div class="ev-wrap"><div class="ev-section-heading">
            <p class="ev-eyebrow">Where we've been</p><h2 id="past-heading">Recent events</h2>
            <p>Missed us at an event? We'd still love to connect.</p>
          </div><div class="ev-event-list">{''.join(card(e, today) for e in past)}</div></div>
        </section>'''
    empty = '<div class="ev-empty"><p>Our next event will be announced here. In the meantime, we\'d love to connect with you.</p><a class="ev-text-link" href="/contact-us/">Contact our team &rarr;</a></div>'
    hub = render(
        "index.html", styles=styles, build_date=today.isoformat(),
        hero_image=image_html("MGMA.jpg", "Optimax team members at their healthcare conference booth.", eager=True),
        upcoming_cards="".join(card(e, today) for e in upcoming) or empty,
        past_section=past_section,
    )
    pages = [("events", "Events", "Meet Optimax at upcoming healthcare conferences and community events.", hub, "opx-events")]
    for event in events:
        pages.append((event["slug"], event["name"], event["summary"], event_page(event, today, styles), "opx-event"))
    routes = {"/": "optimax-home-preview.html", **{f"/{slug}/": f"optimax-{slug}-preview.html" for slug, *_ in pages}}
    for slug, title, description, content, main_id in pages:
        write(ROOT / f"{slug}.html", content)
        write(ROOT / "preview" / f"optimax-{slug}-preview.html", preview(content, title, description, main_id, today, routes))
    # Refresh the existing homepage preview only; the production home body is untouched.
    home = (ROOT / "home.html").read_text(encoding="utf-8")
    home = home.replace('<main class="opx-home">', '<main class="opx-home" id="opx-home">', 1)
    write(ROOT / "preview" / "optimax-home-preview.html", preview(home, "Revenue Cycle Management", "Optimax Consulting Services", "opx-home", today, routes, active=False))
    manifest = {
        "built_for_date": today.isoformat(),
        "render_settings": {"render_mode": "theme_wrapped", "render_position": "replace", "full_width_content": True, "full_page_canvas": False},
        "pages": [
            {"slug": slug, "title": title, "meta_description": description,
             "source": f"optimax/{slug}.html", "url": f"https://optimaxcs.net/{slug}/",
             "shortcode": f'[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="optimax/{slug}.html" format="html"]'}
            for slug, title, description, *_ in pages
        ],
        "menu_entry": {"label": "Events", "url": "/events/", "placement": "After Resources in the existing primary menu", "include_in_mobile_menu": True},
    }
    write(EVENTS / "wordpress-setup.json", json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Built {len(pages)} page partials and {len(pages) + 1} previews for {today}: {len(upcoming)} upcoming, {len(past)} recent.")


if __name__ == "__main__":
    main()
