#!/usr/bin/env python3
"""
West Coast Construction Group GitPress fragment generator.

Reads data/services.json + the shared CSS/JS and emits Theme-Wrapped
body-partial fragments (<style> + <main> + <script>), one per page.
Also writes standalone preview docs (mock Divi shell + placeholder art)
to a preview/ dir for local review; those are NOT committed fragments.

Usage:
  python build.py            # write production fragments
  python build.py --preview <dir>   # also write preview docs to <dir>
"""
import json, os, re, sys, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "data", "services.json"), encoding="utf-8"))
CSS  = open(os.path.join(ROOT, "assets", "css", "wcc-system.css"), encoding="utf-8").read()
JS   = open(os.path.join(ROOT, "assets", "js", "wcc.js"), encoding="utf-8").read()

SITE = DATA["site"]
IDX  = DATA["pageIndex"]
BASE = "https://wccgrp.com"   # confirmed from live asset URLs on the old pages
MARK = datetime.date.today().isoformat()

# Images committed to the GitHub repo are served through the jsDelivr CDN.
# In content, write image paths as "asset:img/foo.jpg"; assemble() rewrites the
# "asset:" prefix to this base for production, and preview_wrap() rewrites it to a
# local path so the preview shows the images before anything is pushed.
# NOTE: jsDelivr only serves PUBLIC repos. If wp-landingpages is private, either
# make it public, or upload these images to the WordPress media library instead.
ASSET_CDN = "https://cdn.jsdelivr.net/gh/citrynmarketingdevelopment/wp-landingpages@main/wcc/assets/"
REVISION = "gitpress-interactions-2026-07-29-v6"

# ---------------------------------------------------------------- icons
# Inline, stroke-based, GitPress-safe (no script/href/foreignObject).
_I = {
  "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9.5 21v-6h5v6"/>',
  "building": '<path d="M4 21V4a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v17"/><path d="M15 9h4a1 1 0 0 1 1 1v11"/><path d="M8 7h3M8 11h3M8 15h3M18 13h0M18 17h0"/>',
  "alert": '<path d="M12 3 2.5 20.5h19L12 3Z"/><path d="M12 10v5"/><path d="M12 18h.01"/>',
  "hammer": '<path d="m14 8-8.5 8.5a2.1 2.1 0 0 0 3 3L17 11"/><path d="M13 7l4-4 4 4-4 4"/><path d="m11 9 4 4"/>',
  "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
  "shield": '<path d="M12 3 5 6v6c0 4 3 6.5 7 9 4-2.5 7-5 7-9V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
  "pin": '<path d="M12 21s7-5.5 7-11a7 7 0 0 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
  "phone": '<path d="M6 3h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 14l5 2v3a2 2 0 0 1-2.2 2A16 16 0 0 1 4 5.2 2 2 0 0 1 6 3Z"/>',
  "mail": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m3 7 9 6 9-6"/>',
  "check": '<circle cx="12" cy="12" r="9"/><path d="m8.5 12 2.5 2.5L16 9"/>',
  "clipboard": '<rect x="6" y="4" width="12" height="17" rx="1.5"/><path d="M9 4V3h6v1"/><path d="M9 10h6M9 14h6M9 18h4"/>',
  "key": '<circle cx="8" cy="8" r="4.5"/><path d="m11 11 8 8"/><path d="m16 16 2-2M18.5 18.5 20 17"/>',
  "roof": '<path d="M2 12 12 4l10 8"/><path d="M5 10.5V20h14v-9.5"/><path d="M9 20v-4a3 3 0 0 1 6 0v4"/>',
  "tree": '<path d="M12 3c3 2.5 4.5 5 4.5 7A4.5 4.5 0 0 1 12 21a4.5 4.5 0 0 1-4.5-11c0-2 1.5-4.5 4.5-7Z"/><path d="M12 21v-6"/>',
  "arrow": '<path d="M5 12h13"/><path d="m13 6 6 6-6 6"/>',
  "search": '<circle cx="11" cy="11" r="7"/><path d="m16.5 16.5 4 4"/>',
  "star": '<path d="m12 4 2.3 4.9 5.2.6-3.9 3.6 1.1 5.2L12 16.2 7.2 18.9l1.1-5.2L4.4 9.5l5.2-.6L12 4Z"/>',
}
def icon(name, cls="ico"):
    p = _I.get(name, _I["check"])
    return (f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round">{p}</svg></span>')

def e(t):
    return html.escape(str(t), quote=False)

_LINK_RE = re.compile(r'\[\[([a-z0-9\-]+)\|([^\]]+)\]\]')

def rich(t):
    """Escape copy, then turn [[page-id|anchor text]] tokens into contextual
       internal links. Keeps SEO's in-content linking without a card section."""
    s = e(t)
    def sub(m):
        pid, label = m.group(1), m.group(2)
        p = IDX.get(pid)
        return f'<a class="wcc-ilink" href="{p["url"]}">{label}</a>' if p else label
    return _LINK_RE.sub(sub, s)

def arrow_link(text, url):
    return (f'<a class="arrow-link" href="{url}">{e(text)}'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{_I["arrow"]}</svg></a>')

def phone_btn(cls="btn btn-outline"):
    return (f'<a class="{cls}" href="tel:{SITE["phoneHref"]}">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{_I["phone"]}</svg>'
            f'{SITE["phone"]}</a>')

def call_btn(cls="btn btn-primary btn-lg"):
    return (f'<a class="{cls}" href="tel:{SITE["phoneHref"]}">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{_I["phone"]}</svg>'
            f'Call {SITE["phone"]}</a>')

def emergency_band(kicker, h2, p):
    return (f'<section class="wcc-section wcc-section--tight"><div class="wcc-wrap">'
            f'<div class="wcc-emg" data-reveal>'
            f'<div><p class="kicker">{e(kicker)}</p><h2>{e(h2)}</h2><p>{e(p)}</p></div>'
            f'<div class="wcc-emg__call"><span class="num">{SITE["phone"]}</span>'
            f'<a class="btn btn-primary btn-lg" href="tel:{SITE["phoneHref"]}">Call now</a></div>'
            f'</div></div></section>')

# ---------------------------------------------------------------- sections
def crumbs(items):
    """items: list of (name, url|None). Last item = current page (url None)."""
    lis, jl = [], []
    for i, (name, url) in enumerate(items):
        pos = i + 1
        if url:
            lis.append(f'<li><a href="{url}">{e(name)}</a></li>')
            jl.append({"@type": "ListItem", "position": pos, "name": name, "item": BASE + url})
        else:
            lis.append(f'<li aria-current="page">{e(name)}</li>')
            jl.append({"@type": "ListItem", "position": pos, "name": name})
        if i < len(items) - 1:
            lis.append('<li class="sep" aria-hidden="true">/</li>')
    nav = f'<nav class="wcc-crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'
    return nav, {"@type": "BreadcrumbList", "itemListElement": jl}

def hero_dark(eyebrow, h1_text, value, intro, image, alt, crumbs_html="", emergency=False):
    # CSLB/trust now lives in the elevated card directly below the hero.
    crumbs_block = f'<div class="wcc-hero__crumbs">{crumbs_html}</div>' if crumbs_html else ""
    if emergency:
        cta = call_btn("btn btn-primary btn-lg") + '<a class="btn btn-outline-light btn-lg" href="/contact/">Get an estimate</a>'
    else:
        cta = cta_buttons("Get an estimate", "/contact/", on_dark=True)
    return (f'<section class="wcc-hero">'
            f'<div class="wcc-hero__bg"><img src="{image}" alt="{e(alt)}" fetchpriority="high"></div>'
            f'<div class="wcc-wrap wcc-hero__inner">'
            f'<div class="wcc-hero__content">'
            f'{crumbs_block}'
            f'<p class="kicker">{e(eyebrow)}</p>'
            f'<h1>{e(h1_text)}</h1>'
            f'<p class="wcc-hero__value">{e(value)}</p>'
            f'<p class="wcc-hero__intro">{e(intro)}</p>'
            f'<div class="wcc-hero__cta">{cta}</div>'
            f'</div></div></section>')

def trust_bar(items):
    lis = "".join(
        f'<li>{icon(it["icon"], "ico ico--box")}<div><b>{e(it["b"])}</b><span>{e(it["s"])}</span></div></li>'
        for it in items)
    return (f'<section class="wcc-trust" aria-label="Credentials"><div class="wcc-wrap">'
            f'<ul class="wcc-trust__card">{lis}</ul></div></section>')

def cta_buttons(primary, primary_url, phone=True, on_dark=False):
    b = [f'<a class="btn btn-primary btn-lg" href="{primary_url}">{e(primary)}'
         f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         f'stroke-linecap="round" stroke-linejoin="round">{_I["arrow"]}</svg></a>']
    if phone:
        b.append(phone_btn("btn btn-outline-light btn-lg" if on_dark else "btn btn-outline btn-lg"))
    return "".join(b)

def faq_block(faqs):
    items = ""
    for i, f in enumerate(faqs):
        items += (
            f'<details class="wcc-faq__item">'
            f'<summary class="wcc-faq__q">'
            f'<span>{e(f["q"])}</span><span class="wcc-faq__icon" aria-hidden="true"></span></summary>'
            f'<div class="wcc-faq__a"><div class="wcc-faq__a-inner"><p>{rich(f["a"])}</p></div></div>'
            f'</details>')
    return items

def related_block(ids, heading="Related services"):
    cards = ""
    for pid in ids:
        p = IDX[pid]
        cards += (f'<div class="wcc-relcard" data-reveal><h3>{e(p["title"])}</h3>'
                  f'<p>{e(p["blurb"])}</p>{arrow_link("View " + p["title"], p["url"])}</div>')
    return (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
            f'<p class="kicker">Keep Exploring</p><h2>{e(heading)}</h2>'
            f'<div class="wcc-related" style="margin-top:34px">{cards}</div></div></section>')

def video_gallery_section(v):
    """Dark band. Featured bracketed player plus a playlist rail that swaps the
       source in. No poster images: both the featured player and every rail
       thumbnail are real <video> elements set to preload="metadata", and a
       tiny JS nudge (see wcc.js primeFirstFrame) seeks to ~0.01s so the
       browser paints the clip's own first frame instead of a black box.
       Nothing plays or downloads in full until the visitor clicks."""
    items = v["items"]
    first = items[0]
    play_path = '<path d="M8 5v14l11-7z"/>'

    thumbs = ""
    for i, it in enumerate(items):
        thumbs += (
            f'<button class="wcc-vg__thumb" type="button" aria-pressed="{"true" if i == 0 else "false"}" '
            f'data-src="{it["src"]}" data-title="{e(it["title"])}" data-alt="{e(it["alt"])}">'
            f'<span class="wcc-vg__thumbimg">'
            f'<video class="wcc-vg__thumbvideo" muted playsinline preload="metadata" '
            f'aria-hidden="true" tabindex="-1"><source src="{it["src"]}" type="video/mp4"></video>'
            f'<span class="wcc-vg__badge" aria-hidden="true">'
            f'<svg viewBox="0 0 24 24" fill="currentColor">{play_path}</svg></span></span>'
            f'<span class="wcc-vg__label">{e(it["title"])}</span></button>')

    note = f'<p class="wcc-vg__note">{e(v["note"])}</p>' if v.get("note") else ""

    return (f'<section class="wcc-section wcc-section--dark wcc-video" data-video data-video-gallery>'
            f'<div class="wcc-wrap">'
            f'<div data-reveal><p class="kicker">{e(v["kicker"])}</p>'
            f'<h2 class="wcc-vg__heading">{e(v["h2"])}</h2>'
            f'<p class="lede wcc-vg__intro">{e(v["intro"])}</p></div>'
            f'<div class="wcc-vg">'
            f'<div class="wcc-vg__stage" data-reveal>'
            f'<div class="wcc-video__frame">'
            f'<video preload="metadata" playsinline controls '
            f'aria-label="{e(first["alt"])}"><source src="{first["src"]}" type="video/mp4"></video>'
            f'<button class="wcc-video__play" type="button" aria-label="Play video">'
            f'<svg viewBox="0 0 24 24" fill="currentColor">{play_path}</svg></button></div>'
            f'<h3 class="wcc-vg__now">{e(first["title"])}</h3>'
            f'<p class="wcc-vg__count">{len(items)} project videos</p>'
            f'</div>'
            f'<div class="wcc-vg__rail" aria-label="Choose a project video">{thumbs}</div>'
            f'</div>{note}</div></section>')

def before_after_section(b):
    """Toggle gallery sized for vertical photos. Native details elements keep the
       crossfade working when WordPress strips or blocks JavaScript."""
    cards = ""
    for it in b["items"]:
        cards += (
            f'<figure class="wcc-ba__card" data-reveal>'
            f'<div class="wcc-ba__frame">'
            f'<img class="wcc-ba__img wcc-ba__img--before" src="{it["before"]}" '
            f'loading="lazy" alt="{e(it["beforeAlt"])}">'
            f'<img class="wcc-ba__img wcc-ba__img--after" src="{it["after"]}" '
            f'loading="lazy" alt="{e(it["afterAlt"])}">'
            f'<span class="wcc-ba__pill wcc-ba__pill--before">Before</span>'
            f'<span class="wcc-ba__pill wcc-ba__pill--after">After</span>'
            f'</div>'
            f'<figcaption>{e(it["label"])}<span class="wcc-ba__sub">{e(it["sub"])}</span></figcaption>'
            f'</figure>')

    note = f'<p class="wcc-ba__note">{e(b["note"])}</p>' if b.get("note") else ""

    switch = (f'<div class="wcc-ba__switch" role="group" aria-label="Show before or after photos">'
              f'<details class="wcc-ba__state wcc-ba__state--before" name="wcc-ba-state">'
              f'<summary class="wcc-ba__btn wcc-ba__btn--before">Before</summary></details>'
              f'<details class="wcc-ba__state wcc-ba__state--after" name="wcc-ba-state" open>'
              f'<summary class="wcc-ba__btn wcc-ba__btn--after">After</summary></details>'
              f'</div>')

    return (f'<section class="wcc-section wcc-section--alt wcc-ba-sec" data-ba-state="after"><div class="wcc-wrap">'
            f'<div class="wcc-ba__head">'
            f'<div class="wcc-ba__intro" data-reveal><p class="kicker">{e(b["kicker"])}</p>'
            f'<h2 class="wcc-heading-standard">{e(b["h2"])}</h2>'
            f'<p class="lede">{e(b["intro"])}</p></div>'
            f'{switch}</div>'
            f'<div class="wcc-ba">{cards}</div>{note}'
            f'</div></section>')

def gallery_section(g):
    """Simple project-photo grid for a service page (e.g. bathroom remodels)."""
    imgs = "".join(
        f'<figure class="wcc-gallery__item" data-reveal>'
        f'<img src="{im["src"]}" loading="lazy" alt="{e(im["alt"])}"></figure>'
        for im in g["images"])
    note = f'<p class="wcc-ba__note">{e(g["note"])}</p>' if g.get("note") else ""
    return (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
            f'<div class="wcc-ba__intro" data-reveal><p class="kicker">{e(g["kicker"])}</p>'
            f'<h2 class="wcc-heading-standard">{e(g["h2"])}</h2>'
            f'<p class="lede">{e(g["intro"])}</p></div>'
            f'<div class="wcc-gallery" style="margin-top:34px">{imgs}</div>{note}'
            f'</div></section>')

def instagram_section(ig):
    """Official Instagram profile embed with a plain link fallback."""
    arrow = (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             f'stroke-linecap="round" stroke-linejoin="round">{_I["arrow"]}</svg>')
    embed_url = ig.get("embedUrl", ig["url"])
    embed = (f'<div class="wcc-ig__embed" data-reveal="right">'
             f'<blockquote class="instagram-media" data-instgrm-permalink="{embed_url}" '
             f'data-instgrm-version="14">'
             f'<a class="wcc-ig__embed-fallback" href="{ig["url"]}" target="_blank" rel="noopener">'
             f'View {e(ig["handle"])} on Instagram</a>'
             f'</blockquote></div>'
             f'<script async src="https://www.instagram.com/embed.js"></script>')
    return (f'<section class="wcc-section wcc-section--dark"><div class="wcc-wrap"><div class="wcc-ig">'
            f'<div data-reveal="left"><p class="kicker">{e(ig["kicker"])}</p>'
            f'<h2 class="wcc-ig__heading">{e(ig["h2"])}</h2>'
            f'<p class="lede wcc-ig__intro">{e(ig["intro"])}</p>'
            f'<span class="wcc-ig__handle">{e(ig["handle"])}</span>'
            f'<a class="btn btn-primary" href="{ig["url"]}" target="_blank" rel="noopener">'
            f'Follow on Instagram{arrow}</a></div>'
            f'{embed}'
            f'</div></div></section>')

def final_cta(h2, p, primary, primary_url, emergency=False):
    if emergency:
        actions = call_btn("btn btn-primary btn-lg") + f'<a class="btn btn-outline-light btn-lg" href="{primary_url}">{e(primary)}</a>'
    else:
        actions = (f'<a class="btn btn-primary btn-lg" href="{primary_url}">{e(primary)}</a>'
                   + phone_btn("btn btn-outline-light btn-lg"))
    return (f'<section class="wcc-section wcc-cta"><div class="wcc-wrap">'
            f'<h2>{e(h2)}</h2><p>{e(p)}</p>'
            f'<div class="wcc-cta__actions">{actions}</div></div></section>')

def sticky_bar():
    return (f'<div class="wcc-sticky" aria-label="Quick actions">'
            f'<a class="s-call" href="tel:{SITE["phoneHref"]}">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{_I["phone"]}</svg>Call</a>'
            f'<a class="s-quote" href="/contact/">Get an Estimate</a></div>')

# ---------------------------------------------------------------- schema
def business_node():
    return {
        "@type": ["GeneralContractor", "LocalBusiness"],
        "@id": BASE + "/#business",
        "name": SITE["name"],
        "alternateName": SITE["legalName"],
        "telephone": SITE["phone"],
        "email": SITE["email"],
        "url": BASE + "/",
        "image": BASE + "/wp-content/uploads/wcc/logo.png",
        "identifier": {"@type": "PropertyValue", "name": "CSLB License", "value": SITE["cslb"]},
        "areaServed": [
            {"@type": "City", "name": "Bakersfield"},
            {"@type": "AdministrativeArea", "name": "Kern County"},
            {"@type": "AdministrativeArea", "name": "San Luis Obispo County"},
        ],
    }

def service_schema(name, url, desc):
    return {
        "@type": "Service", "name": name, "serviceType": name,
        "url": BASE + url, "description": desc,
        "provider": {"@id": BASE + "/#business"},
        "areaServed": [{"@type": "City", "name": "Bakersfield"},
                       {"@type": "AdministrativeArea", "name": "Kern County"}],
    }

def webpage_node(url, name, desc):
    return {"@type": "WebPage", "@id": BASE + url + "#webpage", "url": BASE + url,
            "name": name, "description": desc,
            "isPartOf": {"@id": BASE + "/#website"},
            "about": {"@id": BASE + "/#business"}}

def website_node():
    return {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
            "name": SITE["name"], "publisher": {"@id": BASE + "/#business"}}

def ldjson(graph):
    doc = {"@context": "https://schema.org", "@graph": graph}
    return ('<script type="application/ld+json">'
            + json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + '</script>')

# ---------------------------------------------------------------- page: HOME
def build_home():
    d = DATA["home"]; h = d["hero"]
    hero = hero_dark(h["eyebrow"], h["h1"], h["value"], h["intro"], h["image"], h["alt"])

    tb = trust_bar(d["trust"])

    silos = ""
    for s in d["silos"]:
        cls = "wcc-silo wcc-silo--dark" if s.get("emergency") else "wcc-silo"
        silos += (f'<div class="{cls}" data-reveal><div class="wcc-silo__n">{s["n"]}</div>'
                  f'{icon(s["icon"], "ico ico--box")}<h3>{e(s["title"])}</h3><p>{e(s["text"])}</p>'
                  f'{arrow_link(s["cta"], IDX[s["id"]]["url"])}</div>')
    silo_sec = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
                f'<p class="kicker">Three Ways We Build</p>'
                f'<h2 class="wcc-home-silos__heading">Residential, commercial, and 24/7 emergency construction</h2>'
                f'<div class="wcc-silos">{silos}</div></div></section>')

    def feature(block, parent_id, tone="", media_right=False):
        lis = "".join(f'<li>{icon("check")}<a href="{IDX[pid]["url"]}">{e(IDX[pid]["title"])}</a></li>'
                      for pid in block["ids"])
        media = (f'<div class="wcc-split__media" data-reveal>'
                 f'<img src="{block["image"]}" width="720" height="540" loading="lazy" alt="{e(block["alt"])}"></div>')
        copy = (f'<div data-reveal><p class="kicker">{e(block["kicker"])}</p>'
                f'<h2 class="wcc-heading-standard">{e(block["h2"])}</h2>'
                f'<p class="lede">{e(block["intro"])}</p><ul>{lis}</ul>'
                f'<a class="btn btn-outline" href="{IDX[parent_id]["url"]}">View all {block["kicker"].lower()}'
                f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                f'stroke-linecap="round" stroke-linejoin="round">{_I["arrow"]}</svg></a></div>')
        inner = (copy + media) if media_right else (media + copy)
        return (f'<section class="wcc-section {tone}"><div class="wcc-wrap">'
                f'<div class="wcc-split">{inner}</div></div></section>')

    res = feature(d["residentialFeature"], "residential")
    com = feature(d["commercialFeature"], "commercial", tone="wcc-section--alt", media_right=True)

    emg = (f'<section class="wcc-section"><div class="wcc-wrap"><div class="wcc-emg" data-reveal>'
           f'<div><p class="kicker">24/7 Emergency Response</p>'
           f'<h2>Urgent damage? We respond fast.</h2>'
           f'<p>Roof leaks, storm damage, water intrusion, and structural issues don\'t wait. '
           f'We prioritize containment and stabilization first, then a clear repair plan.</p>'
           f'<div class="wcc-inline-action wcc-inline-action--20">{arrowish("Emergency services", IDX["emergency"]["url"])}</div></div>'
           f'<div class="wcc-emg__call"><span class="num">{SITE["phone"]}</span>'
           f'<a class="btn btn-primary" href="tel:{SITE["phoneHref"]}">Call now</a></div>'
           f'</div></div></section>')

    w = d["whyUs"]
    why_items = "".join(f'<div class="wcc-why__item" data-reveal>{icon(i["icon"], "ico ico--box")}'
                        f'<h3>{e(i["h3"])}</h3><p>{e(i["p"])}</p></div>' for i in w["items"])
    why = (f'<section class="wcc-section"><div class="wcc-wrap">'
            f'<p class="kicker">{e(w["kicker"])}</p><h2 class="wcc-home-why__heading">{e(w["h2"])}</h2>'
           f'<div class="wcc-why">{why_items}</div></div></section>')

    pr = d["process"]
    steps = "".join(f'<div class="wcc-step" data-reveal><div class="wcc-step__n">{str(i+1).zfill(2)}</div>'
                    f'<h3>{e(s["h3"])}</h3><p>{e(s["p"])}</p></div>' for i, s in enumerate(pr["steps"]))
    proc = (f'<section class="wcc-section wcc-section--dark"><div class="wcc-wrap">'
             f'<p class="kicker">{e(pr["kicker"])}</p><h2 class="wcc-home-process__heading">{e(pr["h2"])}</h2>'
            f'<div class="wcc-process">{steps}</div></div></section>')

    sa = d["serviceArea"]
    area = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap"><div class="wcc-local">'
            f'<div data-reveal><p class="kicker">{e(sa["kicker"])}</p>'
            f'<h2 class="wcc-home-area__heading">{e(sa["h2"])}</h2>'
            f'<p class="prose">{e(sa["intro"])}</p>'
            f'<div class="wcc-inline-action wcc-inline-action--22">{arrowish("Contact our team", "/contact/")}</div></div>'
            f'<div class="wcc-local__media" data-reveal><img src="{sa["image"]}" width="640" height="512" loading="lazy" alt="{e(sa["alt"])}"></div>'
            f'</div></div></section>')

    fin = (f'<section class="wcc-section wcc-section--tight wcc-financing-section"><div class="wcc-wrap">'
           f'<div class="wcc-financing">'
           f'<div><p class="kicker">Financing</p><h3>We offer financing options</h3></div>'
           f'<a class="btn btn-outline" href="/contact/">Ask about financing</a></div></div></section>')

    qs = "".join(
        f'<div class="wcc-quote" data-reveal>'
        f'<div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
        f'<blockquote>{e(t["quote"])}</blockquote><cite>{e(t["cite"])}</cite></div>'
        for t in DATA["testimonials"])
    test = (f'<section class="wcc-section wcc-reviews-section"><div class="wcc-wrap">'
            f'<p class="kicker">Reviews</p><h2 class="wcc-heading-list">What clients say</h2>'
            f'<div class="wcc-quotes">{qs}</div></div></section>')

    faqs = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
            f'<p class="kicker">FAQ</p><h2 class="wcc-heading-faq">General contractor FAQs</h2>'
            f'<div class="wcc-faq">{faq_block(d["faqs"])}</div></div></section>')

    fc = d["finalCta"]
    cta = final_cta(fc["h2"], fc["p"], fc["primary"], fc["primaryUrl"])

    vid = video_gallery_section(d["videoGallery"])
    ba  = before_after_section(d["beforeAfter"])
    ig  = instagram_section(d["instagram"])

    main = "".join([hero, tb, silo_sec, res, com, vid, emg, ba, why, proc, area, fin, test, ig, faqs, cta])

    graph = [website_node(), business_node(),
             webpage_node("/", "General Contractor in Bakersfield, CA", d["hero"]["intro"][:180])]
    return assemble("home", main, ldjson(graph)), "General Contractor Bakersfield, CA"

def arrowish(text, url):
    return arrow_link(text, url)

def block_icon(pid):
    m = {"custom-home-building": "home", "adu-garage-conversions": "key",
         "home-additions-expansions": "layers", "remodeling-home-renovations": "hammer",
         "roofing-roof-leak-repair": "roof", "outdoor-living-patios-patio-covers-pergolas-pool-areas": "tree",
         "commercial-gc-project-management": "clipboard", "tenant-improvements-build-outs": "building",
         "commercial-remodeling-renovations": "hammer", "new-commercial-construction": "building",
         "concrete-asphalt-parking-lots-flatwork": "layers", "facility-maintenance-on-call-repairs": "shield",
         "emergency-water-damage-response": "alert", "emergency-roof-leaks": "roof",
         "storm-damage-emergency-repairs": "alert", "emergency-property-damage-repairs": "shield",
         "ceiling-collapse-drywall-failure-emergency-repairs": "alert",
         "emergency-structural-stabilization": "layers"}
    return m.get(pid, "check")

# ---------------------------------------------------------------- page: PARENT
def build_parent(pid):
    d = DATA["parents"][pid]; h = d["hero"]
    emg_page = d.get("ctaType") == "emergency"
    cb, cb_ld = crumbs([("Home", "/"), (d["category"] + " Services", None)])
    hero = hero_dark(h["eyebrow"], d["h1"], h["value"], h["intro"], h["image"], h["alt"], crumbs_html=cb, emergency=emg_page)
    band = emergency_band(d["band"]["kicker"], d["band"]["h2"], d["band"]["p"]) if emg_page and d.get("band") else ""

    ov = d["overview"]
    cards = ""
    for c in d["cards"]:
        p = IDX[c["id"]]
        cards += (f'<div class="wcc-service" data-reveal>{icon(c["icon"], "ico ico--box")}'
                  f'<h3>{e(p["title"])}</h3><p>{e(c["desc"])}</p>'
                  f'{arrow_link("Learn more", p["url"])}</div>')
    overview = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
                f'<div class="wcc-featured__head"><div style="max-width:54ch">'
                f'<p class="kicker">{e(ov["kicker"])}</p><h2 style="margin:12px 0 12px">{e(ov["h2"])}</h2>'
                f'<p class="lede">{e(ov["intro"])}</p></div></div>'
                f'<div class="wcc-servicegrid">{cards}</div></div></section>')

    sg = d["signs"]
    items = "".join(f'<li>{icon("check")}<div><b>{e(i["b"])}</b><span>{e(i["s"])}</span></div></li>'
                    for i in sg["items"])
    signs = (f'<section class="wcc-section"><div class="wcc-wrap"><div class="wcc-signs">'
             f'<div data-reveal><p class="kicker">{e(sg["kicker"])}</p>'
             f'<h2 style="margin:12px 0 16px">{e(sg["h2"])}</h2><p class="prose">{e(sg["intro"])}</p></div>'
             f'<ul data-reveal>{items}</ul></div></div></section>')

    pr = d["process"]
    steps = "".join(f'<div class="wcc-step" data-reveal><div class="wcc-step__n">{str(i+1).zfill(2)}</div>'
                    f'<h3>{e(s["h3"])}</h3><p>{e(s["p"])}</p></div>' for i, s in enumerate(pr["steps"]))
    proc = (f'<section class="wcc-section wcc-section--dark"><div class="wcc-wrap">'
            f'<p class="kicker">{e(pr["kicker"])}</p><h2 style="margin:12px 0 40px;max-width:22ch">{e(pr["h2"])}</h2>'
            f'<div class="wcc-process">{steps}</div></div></section>')

    lo = d["local"]
    pts = "".join(f'<li>{icon("check")}<span>{e(x)}</span></li>' for x in lo["points"])
    local = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap"><div class="wcc-local">'
             f'<div class="wcc-local__media" data-reveal><img src="{lo["image"]}" width="640" height="512" alt="{e(lo["alt"])}"></div>'
             f'<div data-reveal><p class="kicker">{e(lo["kicker"])}</p>'
             f'<h2 style="margin:10px 0 16px">{e(lo["h2"])}</h2><p class="prose">{rich(lo["p"])}</p>'
             f'<ul>{pts}</ul></div></div></div></section>')

    faqs = (f'<section class="wcc-section"><div class="wcc-wrap">'
            f'<p class="kicker">FAQ</p><h2 style="margin:10px 0 30px">Frequently asked questions</h2>'
            f'<div class="wcc-faq">{faq_block(d["faqs"])}</div></div></section>')

    fc = d.get("cta", {})
    cta = final_cta(fc.get("h2", "Ready to start your project?"),
                    fc.get("p", "Tell us about your project and we will help you plan the scope, timeline, and next steps."),
                    "Get an estimate", "/contact/", emergency=emg_page)

    main = "".join([hero, band, overview, signs, proc, local, faqs, cta])

    graph = [website_node(), business_node(),
             webpage_node(IDX[pid]["url"], d["h1"], d["metaDescription"]),
             cb_ld,
             service_schema(d["h1"], IDX[pid]["url"], d["metaDescription"])]
    return assemble(pid, main, ldjson(graph)), d["seoTitle"]

# ---------------------------------------------------------------- page: SERVICE (child)
def build_service(sid):
    d = DATA["services"][sid]; h = d["hero"]; parent = IDX[d["parent"]]
    emg_page = d.get("ctaType") == "emergency"
    cb, cb_ld = crumbs([("Home", "/"), (d["category"] + " Services", parent["url"]),
                        (IDX[sid]["title"], None)])
    hero = hero_dark(h["eyebrow"], d["h1"], h["value"], h["intro"], h["image"], h["alt"], crumbs_html=cb, emergency=emg_page)
    band = emergency_band(d["band"]["kicker"], d["band"]["h2"], d["band"]["p"]) if emg_page and d.get("band") else ""

    ov = d["overview"]
    overview = (f'<section class="wcc-section"><div class="wcc-wrap" style="max-width:820px">'
                f'<p class="kicker">{e(ov["kicker"])}</p>'
                f'<h2 style="margin:10px 0 20px">{e(ov["h2"])}</h2>'
                f'<div class="prose" style="font-size:1.08rem"><p>{rich(ov["p1"])}</p><p>{rich(ov["p2"])}</p></div></div></section>')

    sc = d["scope"]
    sc_items = "".join(
        f'<div class="wcc-scope__item" data-reveal><span class="num">{str(i+1).zfill(2)}</span>'
        f'<h3>{e(it["h3"])}</h3><p>{e(it["p"])}</p></div>' for i, it in enumerate(sc["items"]))
    scope = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
             f'<p class="kicker">{e(sc["kicker"])}</p><h2 style="margin:10px 0 34px">{e(sc["h2"])}</h2>'
             f'<div class="wcc-scope">{sc_items}</div></div></section>')

    sg = d["signs"]
    sg_items = "".join(f'<li>{icon("check")}<div><b>{e(i["b"])}</b><span>{e(i["s"])}</span></div></li>'
                       for i in sg["items"])
    signs = (f'<section class="wcc-section"><div class="wcc-wrap"><div class="wcc-signs">'
             f'<div data-reveal><p class="kicker">{e(sg["kicker"])}</p>'
             f'<h2 style="margin:10px 0 16px">{e(sg["h2"])}</h2><p class="prose">{e(sg["intro"])}</p></div>'
             f'<ul data-reveal>{sg_items}</ul></div></div></section>')

    pr = d["process"]
    steps = "".join(f'<div class="wcc-step" data-reveal><div class="wcc-step__n">{str(i+1).zfill(2)}</div>'
                    f'<h3>{e(s["h3"])}</h3><p>{e(s["p"])}</p></div>' for i, s in enumerate(pr["steps"]))
    proc = (f'<section class="wcc-section wcc-section--dark"><div class="wcc-wrap">'
            f'<p class="kicker">{e(pr["kicker"])}</p><h2 style="margin:10px 0 40px;color:#fff;max-width:22ch">{e(pr["h2"])}</h2>'
            f'<div class="wcc-process">{steps}</div></div></section>')

    lo = d["local"]
    pts = "".join(f'<li>{icon("check")}<span>{e(x)}</span></li>' for x in lo["points"])
    local = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap"><div class="wcc-local">'
             f'<div class="wcc-local__media" data-reveal><img src="{lo["image"]}" width="640" height="512" alt="{e(lo["alt"])}"></div>'
             f'<div data-reveal><p class="kicker">{e(lo["kicker"])}</p>'
             f'<h2 style="margin:10px 0 16px">{e(lo["h2"])}</h2><p class="prose">{rich(lo["p"])}</p>'
             f'<ul>{pts}</ul></div></div></div></section>')

    w = d["whyUs"]
    why_items = "".join(f'<div class="wcc-why__item" data-reveal>{icon(i["icon"], "ico ico--box")}'
                        f'<h3>{e(i["h3"])}</h3><p>{e(i["p"])}</p></div>' for i in w["items"])
    why = (f'<section class="wcc-section"><div class="wcc-wrap">'
           f'<p class="kicker">{e(w["kicker"])}</p><h2 style="margin:12px 0 34px;max-width:24ch">{e(w["h2"])}</h2>'
           f'<div class="wcc-why">{why_items}</div></div></section>')

    faqs = (f'<section class="wcc-section wcc-section--alt"><div class="wcc-wrap">'
            f'<p class="kicker">FAQ</p><h2 style="margin:12px 0 30px">Frequently asked questions</h2>'
            f'<div class="wcc-faq">{faq_block(d["faqs"])}</div></div></section>')

    gallery = gallery_section(d["gallery"]) if d.get("gallery") else ""

    sc = d.get("cta", {})
    cta = final_cta(sc.get("h2", "Ready to start your project?"),
                    sc.get("p", "Tell us about your project and we will help you plan scope, timeline, and next steps."),
                    "Get an estimate", "/contact/", emergency=emg_page)

    main = "".join([hero, band, overview, scope, signs, proc, local, gallery, why, faqs, cta])

    graph = [website_node(), business_node(),
             webpage_node(IDX[sid]["url"], d["h1"], d["metaDescription"]),
             cb_ld,
             service_schema(d["h1"], IDX[sid]["url"], d["metaDescription"])]
    return assemble(sid, main, ldjson(graph)), d["seoTitle"]

# ---------------------------------------------------------------- assemble
def assemble(page_id, main_html, jsonld):
    frag = (f"<!-- wcc build: {MARK} | revision: {REVISION} | page: {page_id} | render_mode: theme_wrapped -->\n"
            f"<style>\n{CSS}\n</style>\n\n"
            f'<div class="wcc wcc-has-sticky">\n'
            f"<main>\n{main_html}\n</main>\n"
            f"{sticky_bar()}\n"
            f"</div>\n\n"
            f"{jsonld}\n"
            f"<script>\n{JS}\n</script>\n")
    # resolve GitHub-hosted image references to the jsDelivr CDN
    return frag.replace("asset:", ASSET_CDN)

# ---------------------------------------------------------------- preview harness
def placeholder(label, w, h):
    """Data-URI SVG placeholder so preview screenshots look intentional."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
           f'<stop offset="0" stop-color="#33443d"/><stop offset="1" stop-color="#24322d"/></linearGradient></defs>'
           f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
           f'<g fill="none" stroke="#4a5b53" stroke-width="1">'
           + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 40))
           + "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 40))
           + '</g>'
           f'<text x="50%" y="50%" fill="#e6b79f" font-family="Oswald,sans-serif" font-size="{max(12,w//24)}" '
           f'letter-spacing="2" text-anchor="middle" dominant-baseline="middle">{html.escape(label.upper())}</text>'
           f'</svg>')
    import base64
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

def preview_wrap(fragment, title):
    # Real wccgrp.com image URLs are kept so the preview shows actual photos.
    # jsDelivr URLs aren't live until pushed, so point them at the local copies
    # that main() mirrors into <preview_dir>/assets/.
    frag = fragment.replace(ASSET_CDN, "assets/")
    nav = ('<div class="pv-top"><div class="pv-bar"><a class="pv-brand" href="#">WEST COAST '
           '<b>CONSTRUCTION</b> GRP</a><nav class="pv-nav"><a href="#">Home</a><a href="#">Services</a>'
           '<a href="#">Commercial</a><a href="#">Residential</a><a href="#">24/7 Emergency</a>'
           '<a href="#">About</a><a href="#">Contact</a></nav>'
           '<a class="pv-phone" href="#">661-345-7459</a><a class="pv-cta" href="#">Get a Quote</a></div></div>')
    foot = ('<footer class="pv-foot"><div class="pv-fwrap"><div><b>West Coast Construction GRP</b>'
            '<p>Phone: 661-345-7459 · Email: hhoward@wccgrp.com · Lic: #1138797</p></div>'
            '<p class="pv-copy">© 2025 West Coast Construction GRP - PREVIEW SHELL (mock header/footer, not part of the fragment)</p>'
            '</div></footer>')
    css = ('*{margin:0;box-sizing:border-box}body{font-family:Poppins,system-ui,sans-serif;background:#fff}'
           '.pv-top{position:sticky;top:0;z-index:1000;background:#141414;border-bottom:2px solid #F76400}'
           '.pv-bar{max-width:1200px;margin:auto;display:flex;align-items:center;gap:18px;padding:14px 24px}'
           '.pv-brand{font-family:Oswald,sans-serif;letter-spacing:.14em;color:#fff;text-decoration:none;font-size:1rem;font-weight:600}'
           '.pv-brand b{color:#F76400}'
           '.pv-nav{display:flex;gap:18px;margin-left:auto;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em}'
           '.pv-nav a{color:#e0e0da;text-decoration:none;font-family:Oswald,sans-serif}'
           '.pv-phone{color:#F76400;font-family:Oswald,sans-serif;text-decoration:none;font-size:.95rem}'
           '.pv-cta{background:#F76400;color:#141414;padding:10px 16px;border-radius:6px;text-decoration:none;'
           'font-size:.78rem;font-family:Oswald,sans-serif;text-transform:uppercase;letter-spacing:.06em;font-weight:600}'
           '.pv-foot{background:#141414;color:#b9beb0;padding:40px 24px}'
           '.pv-fwrap{max-width:1200px;margin:auto}.pv-foot b{color:#fff;font-family:Oswald,sans-serif;letter-spacing:.08em}'
           '.pv-foot p{font-size:.85rem;margin-top:6px}.pv-copy{margin-top:20px;color:#6f7266;font-size:.75rem}'
           '@media(max-width:900px){.pv-nav,.pv-phone{display:none}}')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>PREVIEW · {html.escape(title)}</title><style>{css}</style></head><body>'
            f'{nav}{frag}{foot}</body></html>')

# ---------------------------------------------------------------- main
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8", newline="\n").write(content)
    print("  wrote", path, f"({len(content)//1024} KB)")

def main():
    preview_dir = None
    if "--preview" in sys.argv:
        preview_dir = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(preview_dir, exist_ok=True)
        # mirror committed assets into the preview dir so asset: URLs resolve locally
        import shutil
        for sub in ("img", "video"):
            src = os.path.join(ROOT, "assets", sub)
            if os.path.isdir(src):
                dst = os.path.join(preview_dir, "assets", sub)
                os.makedirs(dst, exist_ok=True)
                for fn in os.listdir(src):
                    shutil.copy2(os.path.join(src, fn), os.path.join(dst, fn))

    print("Building fragments:")
    pages = [("home.html", build_home, ())]
    # hubs and service pages are all generated from the same templates + data records
    for pid in DATA["parents"]:
        pages.append((f"services/{pid}.html", build_parent, (pid,)))
    for sid in DATA["services"]:
        parent = DATA["services"][sid]["parent"]
        pages.append((f"services/{parent}/{sid}.html", build_service, (sid,)))
    for out, fn, args in pages:
        frag, title = fn(*args)
        write(out, frag)
        if preview_dir:
            name = out.replace("/", "__").replace(".html", "") + ".preview.html"
            open(os.path.join(preview_dir, name), "w", encoding="utf-8", newline="\n").write(preview_wrap(frag, title))
            print("     preview:", name)
    print("Done.")

if __name__ == "__main__":
    main()
