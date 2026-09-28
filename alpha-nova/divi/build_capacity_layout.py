"""Build a Divi 4 page-portability export from the approved HTML (stdlib only).

Run from anywhere: python alpha-nova/divi/build_capacity_layout.py
This writes an import JSON, readable shortcodes, and a simulated local preview.
It does not connect to WordPress or alter the original HTML/reference export.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "capacity-constraint-assessment.html"
OUTPUT = ROOT / "capacity-constraint-assessment.divi.json"
INK, MUTED, RED = "#111114", "#6d6d6d", "#d71920"
ZERO = "0px|0px|0px|0px|false|false"


@dataclass
class Element:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    start: str = ""
    end: str = ""

    @property
    def inner(self):
        return "".join(c.outer if isinstance(c, Element) else c for c in self.children)

    @property
    def outer(self):
        return self.start + self.inner + self.end

    @property
    def text(self):
        return unescape(re.sub(r"<[^>]+>", "", self.inner)).strip()

    def all(self, tag=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Element):
                if (tag is None or child.tag == tag) and (cls is None or cls in child.attrs.get("class", "").split()):
                    found.append(child)
                found.extend(child.all(tag, cls))
        return found

    def one(self, tag=None, cls=None):
        return self.all(tag, cls)[0]

    def elements(self):
        return [c for c in self.children if isinstance(c, Element)]


class SourceParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.root = Element("root")
        self.stack = [self.root]
        self.feed(source)
        assert len(self.stack) == 1, "Unclosed source HTML"

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs), start=self.get_starttag_text())
        self.stack[-1].children.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        assert self.stack[-1].tag == tag, (self.stack[-1].tag, tag)
        self.stack.pop().end = f"</{tag}>"

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")

    def handle_comment(self, data):
        self.handle_data(f"<!--{data}-->")


@dataclass
class Module:
    kind: str
    attrs: dict
    content: str = ""
    children: list = field(default_factory=list)

    def shortcode(self):
        attrs = " ".join(f'{k}="{escape(str(v), quote=True)}"' for k, v in self.attrs.items())
        inner = self.content + "".join(c.shortcode() for c in self.children)
        return f"[et_pb_{self.kind} {attrs}]{inner}[/et_pb_{self.kind}]"

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()


def module(kind, label, content="", children=None, **attrs):
    return Module(kind, {
        "admin_label": label, "_builder_version": "4.27.4", "_module_preset": "default",
        "global_colors_info": "{}", **attrs,
    }, content, children or [])


def text(content, label, *, size=16, color=MUTED, weight=400, align="left", bottom=0, cls="", **attrs):
    settings = dict(text_font=f"Arial|{weight}|||||||", text_text_color=color,
                    text_font_size=f"{size}px", text_line_height="1.55em", text_orientation=align,
                    custom_margin=f"0px|0px|{bottom}px|0px|false|false", custom_padding=ZERO,
                    module_class=cls)
    settings.update(attrs)
    return module("text", label, content.outer if isinstance(content, Element) else content, **settings)


def heading(node, label, *, size=46, phone=28, color=INK, align="center", bottom=14, spacing="-0.035em"):
    level = int(node.tag[1])
    prefix = "header" if level == 1 else f"header_{level}"
    return text(node, label, color=color, align=align, bottom=bottom, **{
        f"{prefix}_font": "Arial|900|||||||", f"{prefix}_text_color": color,
        f"{prefix}_font_size": f"{size}px", f"{prefix}_font_size_tablet": f"{min(size, 46)}px",
        f"{prefix}_font_size_phone": f"{phone}px", f"{prefix}_font_size_last_edited": "on|phone",
        f"{prefix}_line_height": "1.08em", f"{prefix}_letter_spacing": spacing,
    })


def column(children, label="Content", kind="4_4", cls="", padding=ZERO, **attrs):
    return module("column", label, children=children, type=kind, module_class=cls,
                  custom_padding=padding, **attrs)


def row(columns, label, *, width=1140, bottom=0, cls="", equal=False):
    kinds = {1: "4_4", 2: "1_2", 3: "1_3", 4: "1_4"}
    kind = kinds[len(columns)]
    for col in columns:
        col.attrs["type"] = kind
    return module("row", label, children=columns, column_structure=",".join([kind] * len(columns)),
                  module_class=f"anca-row {cls}".strip(), width="calc(100% - 40px)", max_width=f"{width}px",
                  use_custom_gutter="on", gutter_width="2", equalize_column_heights="on" if equal else "off",
                  custom_padding=ZERO, custom_margin=f"0px|auto|{bottom}px|auto|false|false")


def single(children, label, **attrs):
    return row([column(children)], label, **attrs)


def section(rows, label, *, cls="", bg="#ffffff", anchor=None, padding="76px|0px|76px|0px|false|false", phone="58px|0px|58px|0px|false|false"):
    attrs = dict(fb_built="1", module_class=f"anca-section {cls}".strip(), background_color=bg,
                 custom_padding=padding, custom_padding_phone=phone,
                 custom_padding_last_edited="on|phone")
    if anchor:
        attrs["module_id"] = anchor
    return module("section", label, children=rows, **attrs)


def section_head(src, *, dark=False, bonus=False):
    head = src.one(cls="section-head")
    h = head.one("h2")
    parts = [heading(h, h.text, size=56 if bonus else 46, phone=30 if bonus else 28,
                     color="#ffffff" if dark else INK, spacing="-0.05em" if bonus else "-0.035em")]
    for p in head.all("p"):
        parts.append(text(p, "Section introduction", size=17, color="rgba(255,255,255,.72)" if dark else MUTED, align="center"))
    return single(parts, "Section heading and introduction", width=790, bottom=42)


def button(src, label):
    return module("button", label, button_text=src.text, button_url=src.attrs["href"], url_new_window="off",
                  button_alignment="center", custom_button="on", button_text_size="14px",
                  button_text_color="#ffffff", button_bg_color=RED, button_bg_color__hover="#9f1018",
                  button_border_width="0px", button_border_radius="999px", button_font="Arial|800|||||||",
                  button_use_icon="off", custom_padding="13px|24px|13px|24px|false|false",
                  custom_margin=ZERO, module_class="anca-button")


def card_columns(src):
    cols = []
    for card in src.all(cls="card"):
        h = card.one("h3")
        cols.append(column([
            text(card.one(cls="icon").inner, "Icon: " + h.text, size=23, color=RED, weight=900, align="center", bottom=18, cls="anca-icon"),
            heading(h, h.text, size=18, phone=18, align="center", bottom=10, spacing="0px"),
            text(card.one("p"), "Description: " + h.text, size=14, align="center"),
        ], h.text, cls="anca-card", background_color="#ffffff", padding="28px|24px|28px|24px|false|false"))
    return row(cols, "Four editable benefit cards", cls="anca-four-row", equal=True)


def image_module(img, *, logo=False, tall=False):
    # All source assets were checked to be available over HTTPS. Keep their paths
    # and alt text; existing WordPress-hosted images are referenced,
    # not re-imported into the Media Library or replaced by unrelated sample images.
    return module("image", img.attrs["alt"], src=img.attrs["src"].replace("http://alphanovaconsulting.com/", "https://alphanovaconsulting.com/"), alt=img.attrs["alt"],
                  title_text=img.attrs["alt"], align="center", show_in_lightbox="off",
                  force_fullwidth="off" if logo else "on",
                  module_class=("anca-logo" + (" anca-logo-tall" if tall else "")) if logo else "anca-testimonial",
                  background_color="#ffffff" if logo else "#0b0b0d", custom_margin=ZERO,
                  custom_padding="18px|20px|18px|20px|false|false" if logo else ZERO,
                  min_height="104px" if logo else "auto")


def build():
    html = SOURCE.read_text(encoding="utf-8")
    dom = SourceParser(html).root
    sources = dom.one("main").all("section")
    assert len(sources) == 14, "Source sections changed; update the mapping before rebuilding"
    css = (HERE / "capacity-constraint-assessment.css").read_text(encoding="utf-8")
    gear_url = re.search(r'background-image: url\("(data:image/svg\+xml,[^"]+)"\)', html).group(1)
    css = '.anca-section { --anca-gear: url("' + gear_url + '"); }\n' + css
    sections = [section([single([module("code", "Shared layout CSS - keep this module", "<style>\n" + css + "\n</style>", custom_margin=ZERO, custom_padding=ZERO)], "Shared CSS")],
                        "00 | Shared layout styles (keep)", cls="anca-styles", padding=ZERO, phone=ZERO)]

    src = sources[0]
    sections.append(section([single([
        heading(src.one("h1"), "Hero title", size=78, phone=40, color="#ffffff", bottom=18, spacing="-0.045em"),
        text(src.one(cls="hero-sub"), "Hero description", size=25, color="rgba(255,255,255,.92)", weight=700, align="center", bottom=12,
             max_width="720px", module_alignment="center", text_font_size_phone="18px", text_font_size_last_edited="on|phone"),
        text(src.one(cls="hero-support"), "Hero supporting headline", size=32, color="rgba(255,255,255,.96)", weight=800, align="center", bottom=30,
             max_width="760px", module_alignment="center", text_line_height="1.3em", text_font_size_phone="20px", text_font_size_last_edited="on|phone"),
        button(src.one("a"), "Request Your Assessment"),
    ], "Hero content", width=920)], "01 | Hero", cls="anca-hero", bg="#08080a", padding="105px|0px|95px|0px|false|false", phone="72px|0px|70px|0px|false|false"))

    src = sources[1]
    rows = [single([text(src.one("p"), "Trusted by manufacturers nationwide", size=34, color=INK, weight=800, align="center",
                         text_font_size_phone="22px", text_font_size_last_edited="on|phone")], "Trust headline", bottom=34)]
    logos = src.all(cls="logo-pill")
    for i in range(0, len(logos), 4):
        rows.append(row([column([image_module(p.one("img"), logo=True, tall="tall" in p.attrs.get("class", "").split())], p.one("img").attrs["alt"]) for p in logos[i:i+4]],
                        f"Client logos {i+1}-{i+4}", bottom=18 if i < 8 else 0, cls="anca-logo-row"))
    sections.append(section(rows, "02 | Trusted manufacturers", bg="#f7f7f7", padding="38px|0px|44px|0px|false|false", phone="38px|0px|44px|0px|false|false"))

    src = sources[2]
    cards = card_columns(src)
    cards.attrs["custom_margin"] = "0px|auto|34px|auto|false|false"
    sections.append(section([section_head(src), cards, single([button(src.one("a"), "Find My Constraint")], "Assessment CTA")],
                            "03 | Risks of capacity gaps", cls="anca-soft", anchor="assessment"))

    src = sources[3]
    copy = src.one(cls="copy-block")
    visual = src.one(cls="visual-card")
    visual_label = text("<p>CAPACITY CONSTRAINT ASSESSMENT</p>", "Visual card label", size=12, color="rgba(255,255,255,.7)", weight=900, bottom=70, text_letter_spacing=".16em")
    sections.append(section([row([
        column([heading(copy.one("h2"), "Who this assessment is for", size=45, phone=28, align="left", bottom=18),
                text(copy.one("p"), "Audience introduction", bottom=22),
                text(copy.one("ul"), "Operational symptoms checklist", size=17, color="#303030", weight=700)], "Audience copy"),
        column([visual_label, text(visual.inner, "Growth uncertainty callout", size=28, color="#ffffff", weight=900, text_line_height="1.1em")],
               "Assessment visual card", cls="anca-visual", padding="26px|26px|26px|26px|false|false", min_height="360px"),
    ], "Audience and callout", cls="anca-audience-row anca-stack-tablet", equal=True)], "04 | Who the assessment is for", bg="#f7f7f7"))

    src = sources[4]
    sections.append(section([section_head(src), card_columns(src)], "05 | Why manufacturers choose this", cls="anca-soft"))

    src = sources[5]
    cols = []
    for item in src.all(cls="availability-item"):
        kicker = item.one(cls="availability-kicker")
        cols.append(column([text(kicker.inner, kicker.text, size=12, color=RED, weight=900, bottom=12, text_letter_spacing=".12em", text_font="Arial|900||on|||||"),
                            text(item.one("p"), kicker.text + " details", text_line_height="1.75em")], kicker.text,
                           cls="anca-availability-card", background_color="#ffffff", padding="24px|24px|22px|24px|false|false"))
    sections.append(section([
        section_head(src),
        single([text(src.one(cls="availability-lead"), "Senior consultants and custom analysis", size=22, align="center", cls="anca-availability-lead", text_line_height="1.7em",
                     text_font_size_phone="19px", text_font_size_last_edited="on|phone")], "Availability introduction", width=860, bottom=24),
        row(cols, "Availability cards", width=980, bottom=24, cls="anca-stack-tablet", equal=True),
        single([text(src.one(cls="availability-foot").inner, "Leadership team callout", size=18, color=INK, align="center", cls="anca-availability-foot",
                     custom_padding="20px|24px|20px|24px|false|false", text_line_height="1.7em")], "Availability closing note", width=760),
    ], "06 | Limited availability", bg="#f7f7f7"))

    src = sources[6]
    cols = []
    for card in src.all(cls="deliverable"):
        parts = []
        for child in card.elements():
            if child.tag == "h3":
                parts.append(heading(child, child.text, size=21, phone=21, align="left", bottom=14, spacing="0px"))
            else:
                parts.append(text(child, "Deliverable checklist" if child.tag == "ul" else "Deliverable description", size=13 if child.tag == "ul" else 15,
                                  color="#333333" if child.tag == "ul" else MUTED, bottom=18))
        parts[-1].attrs["custom_margin"] = ZERO
        cols.append(column(parts, card.one("h3").text, cls="anca-deliverable", background_color="#ffffff", padding="32px|28px|32px|28px|false|false"))
    sections.append(section([section_head(src, dark=True), row(cols, "Three assessment deliverables", cls="anca-stack-tablet", equal=True)],
                            "07 | What you get", bg=INK, anchor="deliverables"))

    for index, label in [(7, "08 | Bonus 1 - Benchmark report"), (8, "09 | Bonus 2 - Cost intelligence")]:
        src = sources[index]
        children = src.one(cls="benchmark-copy").elements()
        parts = []
        for child in children:
            if child.tag == "h3":
                part = heading(child, child.text, size=22, phone=22, align="left", bottom=18, spacing="-0.02em")
                part.attrs["custom_margin"] = "14px|0px|18px|0px|false|false"
            elif child.tag == "ul":
                detail = "benchmark-list--detail" in child.attrs.get("class", "")
                part = text(child, "Cost intelligence findings" if detail else "Benchmark metrics", size=18 if detail else 20,
                            color=MUTED if detail else INK, weight=400 if detail else 800, bottom=20, text_line_height="1.75em" if detail else "1.55em")
            else:
                emphasis = "bonus-emphasis" in child.attrs.get("class", "")
                part = text(child, "Bonus explanation", size=18, color=INK if emphasis else MUTED, weight=800 if emphasis else 400, bottom=20, text_line_height="1.8em")
            parts.append(part)
        parts[-1].attrs["custom_margin"] = ZERO
        card = column(parts, "Bonus report details", cls="anca-benchmark", background_color="#ffffff", padding="42px|40px|42px|40px|false|false",
                      custom_padding_phone="28px|24px|28px|24px|false|false", custom_padding_last_edited="on|phone")
        sections.append(section([section_head(src, bonus=True), row([card], "Bonus report", width=760)], label, bg="#f7f7f7" if index == 7 else "#ffffff", cls="" if index == 7 else "anca-soft"))

    src = sources[9]
    quote = text(src.one(cls="quote-callout").inner, "Constraint visibility quote", size=24, color="#ffffff", weight=900, align="center", cls="anca-quote",
                 background_color="#070707", custom_padding="42px|42px|42px|42px|false|false", text_line_height="1.22em", text_letter_spacing="-.025em",
                 text_font_size_phone="18px", text_font_size_last_edited="on|phone", custom_padding_phone="32px|24px|32px|24px|false|false", custom_padding_last_edited="on|phone")
    sections.append(section([section_head(src), single([quote], "Leadership quote", width=900)], "10 | Why visibility matters now", cls="anca-soft"))

    src = sources[10]
    cols = []
    for card in src.all(cls="decision"):
        cols.append(column([
            text(card.one(cls="num").inner, "Outcome number " + card.one(cls="num").text, color="#ffffff", weight=900, align="center", bottom=14, cls="anca-number"),
            heading(card.one("h3"), card.one("h3").text, size=17, phone=17, bottom=0, spacing="0px"),
        ], card.one("h3").text, cls="anca-card", background_color="#ffffff", padding="26px|22px|26px|22px|false|false"))
    sections.append(section([section_head(src), row(cols, "Four business outcomes", cls="anca-four-row", equal=True)], "11 | What additional capacity means", bg="#f7f7f7"))

    src = sources[11]
    sections.append(section([section_head(src, dark=True), row([column([image_module(img)], img.attrs["alt"]) for img in src.all("img")],
                                                              "Client testimonial images", cls="anca-stack-tablet")], "12 | Manufacturer testimonials", bg=INK))

    src = sources[12]
    toggles = []
    for detail in src.all("details"):
        summary = detail.one("summary")
        answer = "".join(c.outer for c in detail.elements() if c.tag != "summary")
        toggles.append(module("toggle", summary.text, answer, title=summary.text, open="off", module_class="anca-faq-item",
                              title_font="Arial|900|||||||", title_font_size="16px", title_line_height="1.5em",
                              title_text_color="#070707", closed_title_text_color="#070707", icon_color=RED,
                              closed_toggle_background_color="#ffffff", open_toggle_background_color="#ffffff",
                              body_font="Arial||||||||", body_font_size="16px", body_line_height="1.55em", body_text_color=MUTED,
                              custom_padding="20px|24px|20px|24px|false|false", custom_margin="0px|0px|12px|0px|false|false"))
    toggles[-1].attrs["custom_margin"] = ZERO
    sections.append(section([section_head(src), single(toggles, "Eleven editable FAQ toggles", width=920)], "13 | Frequently asked questions", bg="#f7f7f7", anchor="faq"))

    src = sources[13]
    copy = src.one(cls="form-copy")
    form_code = src.one(cls="iframe-holder").outer + '\n' + dom.one("script").outer
    form_header = src.one(cls="form-panel-header")
    sections.append(section([row([
        column([
            text(copy.one(cls="eyebrow").inner, "Request more information eyebrow", size=14, color=RED, weight=900, bottom=12, text_letter_spacing=".08em", text_font="Arial|900||on|||||"),
            heading(copy.one("h2"), "Request assessment heading", size=54, phone=32, color="#ffffff", align="left", bottom=18, spacing="-.04em"),
            text(copy.one("p"), "Request assessment introduction", size=17, color="rgba(255,255,255,.74)", bottom=22),
            text(copy.one("ul"), "Assessment benefits checklist", size=17, color="#ffffff", weight=700),
        ], "Request assessment copy"),
        column([
            text(form_header.inner, "Form panel title", color="#ffffff", weight=900, align="center", background_color=RED, custom_padding="18px|22px|18px|22px|false|false"),
            module("code", "LeadConnector assessment form and embed script", form_code, custom_margin=ZERO, custom_padding=ZERO),
        ], "Assessment form", cls="anca-form-panel", background_color="#ffffff", min_height="690px"),
    ], "Request copy and form", cls="anca-stack-tablet")], "14 | Request your assessment", cls="anca-form", bg="#060606", anchor="request-assessment",
                            padding="76px|0px|90px|0px|false|false", phone="58px|0px|90px|0px|false|false"))
    return html, sections


def validate(source, sections, shortcodes):
    """Check meaningful import risks: nesting, anchors, missing copy and embeds."""
    allowed = {"section": {"row"}, "row": {"column"}, "column": {"text", "button", "image", "code", "toggle"}}
    for root in sections:
        for m in root.walk():
            assert m.attrs.get("admin_label"), "Unlabeled builder element"
            assert all(c.kind in allowed.get(m.kind, set()) for c in m.children), f"Invalid children in {m.kind}"
    stack = []
    for match in re.finditer(r"\[(/?)(et_pb_\w+)\b([^\]]*)\]", shortcodes):
        close, name = match.group(1, 2)
        if close:
            assert stack and stack.pop() == name, f"Unbalanced shortcode: {name}"
        else:
            stack.append(name)
    assert not stack
    all_modules = [m for section in sections for m in section.walk()]
    ids = [m.attrs["module_id"] for m in all_modules if "module_id" in m.attrs]
    assert len(ids) == len(set(ids)), "Duplicate anchor IDs"
    for m in all_modules:
        if m.kind == "button" and m.attrs["button_url"].startswith("#"):
            assert m.attrs["button_url"][1:] in ids
    original = SourceParser(source).root.one("main")
    payload = "\n".join(m.content + " " + m.attrs.get("title", "") + " " + m.attrs.get("button_text", "") for m in all_modules if m.kind not in {"section", "row", "column"})
    normalize = lambda s: re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", s))).strip()
    flattened = normalize(payload)
    for tag in ("h1", "h2", "h3", "p", "li", "summary"):
        for original_node in original.all(tag):
            assert normalize(original_node.outer) in flattened, "Missing copy: " + original_node.text[:100]
    secure = lambda url: url.replace("http://alphanovaconsulting.com/", "https://alphanovaconsulting.com/")
    assert [(m.attrs["src"], m.attrs["alt"]) for m in all_modules if m.kind == "image"] == [(secure(i.attrs["src"]), i.attrs["alt"]) for i in original.all("img")]
    assert shortcodes.count('src="https://link.msgsndr.com/js/form_embed.js"') == 1
    original_frame = original.one("iframe")
    exported_code = "\n".join(m.content for m in all_modules if m.kind == "code")
    assert SourceParser(exported_code).root.one("iframe").attrs == original_frame.attrs
    counts = Counter(m.kind for m in all_modules)
    assert counts["section"] == 15 and counts["toggle"] == 11 and counts["image"] == 15
    return counts


def preview(sections):
    """Simulate Divi wrappers/settings for local visual QA; not a Divi runtime."""
    styles, serial = [], [0]

    def render(m):
        n = serial[0]
        serial[0] += 1
        key, a = f"preview-module-{n}", m.attrs
        style = []
        for prop in ("background_color", "width", "max_width", "min_height"):
            if prop in a:
                style.append(prop.replace("_", "-") + ":" + a[prop])
        def spacing(value):
            return " ".join(value.split("|")[:4])
        for prop in ("padding", "margin"):
            if "custom_" + prop in a and not (m.kind == "button" and prop == "padding"):
                style.append(prop + ":" + spacing(a["custom_" + prop]))
        if a.get("module_alignment") == "center":
            style.append("margin-left:auto;margin-right:auto")
        base_class = "et_pb_button_module_wrapper" if m.kind == "button" else "et_pb_" + m.kind
        cls = " ".join([base_class, "et_pb_module" if m.kind not in {"section", "row", "column"} else "", a.get("module_class", ""), key])
        attrs = f' class="{escape(cls)}"' + (f' id="{escape(a["module_id"])}"' if "module_id" in a else "")
        if m.kind == "row":
            style.extend([f'--preview-cols:{len(m.children)}', "display:flex" if a.get("equalize_column_heights") == "on" else "display:flow-root"])
        styles.append(f".{key}" + "{" + ";".join(style) + "}")
        for breakpoint, suffix in ((980, "tablet"), (767, "phone")):
            responsive = []
            for prop in ("padding", "margin"):
                if f"custom_{prop}_{suffix}" in a:
                    responsive.append(prop + ":" + spacing(a[f"custom_{prop}_{suffix}"]))
            if responsive:
                styles.append(f"@media(max-width:{breakpoint}px){{.{key}{{" + ";".join(responsive) + "}}")
        if m.kind in {"text", "toggle"}:
            prefix = "text" if m.kind == "text" else "body"
            font = a.get(prefix + "_font", "Arial|400").split("|")
            styles.append(f".{key}{{font-family:Arial,Helvetica,sans-serif;font-weight:{font[1] or 400};font-size:{a.get(prefix+'_font_size','16px')};color:{a.get(prefix+'_text_color',MUTED)};line-height:{a.get(prefix+'_line_height','1.55em')};text-align:{a.get('text_orientation','left')};letter-spacing:{a.get('text_letter_spacing','normal')}}}")
            for breakpoint, suffix in ((980, "tablet"), (767, "phone")):
                if f"{prefix}_font_size_{suffix}" in a:
                    styles.append(f"@media(max-width:{breakpoint}px){{.{key}{{font-size:{a[f'{prefix}_font_size_{suffix}']}}}}}")
            for level in (1, 2, 3):
                p = "header" if level == 1 else f"header_{level}"
                if p + "_font_size" in a:
                    styles.append(f".{key} h{level}{{font-size:{a[p+'_font_size']};color:{a[p+'_text_color']};font-weight:900;line-height:{a[p+'_line_height']};letter-spacing:{a[p+'_letter_spacing']}}}")
                    for breakpoint, suffix in ((980, "tablet"), (767, "phone")):
                        if f"{p}_font_size_{suffix}" in a:
                            styles.append(f"@media(max-width:{breakpoint}px){{.{key} h{level}{{font-size:{a[f'{p}_font_size_{suffix}']}}}}}")
        inner = m.content + "".join(render(c) for c in m.children)
        if m.kind == "text":
            inner = '<div class="et_pb_text_inner">' + inner + "</div>"
        elif m.kind == "code":
            inner = '<div class="et_pb_code_inner">' + inner + "</div>"
        elif m.kind == "image":
            inner = f'<span class="et_pb_image_wrap"><img src="{escape(a["src"])}" alt="{escape(a["alt"])}"></span>'
        elif m.kind == "button":
            styles.append(f".{key}{{text-align:center}}.{key} a{{font-size:14px;font-weight:800;color:white;background:#d71920;border-radius:999px;padding:13px 24px;text-decoration:none}}.{key} a:hover{{background:#9f1018}}")
            inner = f'<a class="et_pb_button" href="{escape(a["button_url"])}">{escape(a["button_text"])}</a>'
        elif m.kind == "toggle":
            styles.append(f".{key}{{background:white}}.{key} summary{{font-size:16px;line-height:1.5;font-weight:900;color:#070707;cursor:pointer;list-style:none;padding-right:24px;position:relative}}.{key} summary:after{{content:'+';position:absolute;right:0;color:#d71920}}.{key}[open] summary:after{{content:'−'}}.{key} .et_pb_toggle_content{{padding-top:20px}}")
            return f'<details{attrs}><summary class="et_pb_toggle_title">{escape(a["title"])}</summary><div class="et_pb_toggle_content">{inner}</div></details>'
        return f'<div{attrs}>{inner}</div>'

    markup = "".join(render(s) for s in sections)
    base = """
    body{margin:0;font-family:Arial,Helvetica,sans-serif}h1,h2,h3,p,ul{margin:0}img{max-width:100%;height:auto}
    .et_pb_section,.et_pb_row,.et_pb_column{position:relative}.et_pb_row{margin:0 auto}
    .et_pb_row>.et_pb_column{float:left;width:calc((100% - (var(--preview-cols) - 1)*3%)/var(--preview-cols));margin-right:3%}
    .et_pb_row>.et_pb_column:last-child{margin-right:0}.et_pb_row:after{content:'';display:table;clear:both}
    @media(max-width:980px){.et_pb_row{display:flow-root!important}.et_pb_row>.et_pb_column{width:100%;margin-right:0;margin-bottom:30px}.anca-four-row>.et_pb_column,.anca-logo-row>.et_pb_column{width:47.25%;margin-right:5.5%}.anca-four-row>.et_pb_column:nth-child(2n),.anca-logo-row>.et_pb_column:nth-child(2n){margin-right:0}}
    """
    # Simulation CSS precedes portable CSS, like Divi's generated design settings.
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Capacity Constraint Assessment — Divi layout preview</title><style>' + base + "\n" + "\n".join(styles) + '</style></head><body><!-- LOCAL PREVIEW: simulated Divi HTML, not proof of a WordPress import. --><main>' + markup + "</main></body></html>"


def main():
    source, sections = build()
    shortcodes = "".join(s.shortcode() for s in sections)
    counts = validate(source, sections, shortcodes)
    payload = {"context": "et_builder", "data": {"1": shortcodes}, "presets": {}, "global_colors": [], "images": {}, "thumbnails": []}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert json.loads(OUTPUT.read_text(encoding="utf-8")) == payload
    (HERE / "capacity-constraint-assessment.shortcodes.txt").write_text("\n\n".join(s.shortcode() for s in sections) + "\n", encoding="utf-8")
    dest = ROOT / "preview" / "capacity-constraint-assessment.divi.preview.html"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(preview(sections), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "preview": str(dest), "counts": counts, "validation": "passed: source copy, image URLs/alt text, shortcode nesting, anchors, form attributes, single embed script, JSON round trip"}, indent=2))


if __name__ == "__main__":
    main()
