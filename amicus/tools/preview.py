"""Local GitPress Managed preview. This does not submit or publish anything."""

from __future__ import annotations

import html
import json
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ROUTES = json.loads((ROOT / "routes.json").read_text(encoding="utf-8"))


class Preview(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == "/layout_tag/light/":
            self.send_response(301)
            self.send_header("Location", "/")
            self.end_headers()
            return
        if path.startswith("/wp-content/"):
            self.path = "/assets" + path
            return super().do_GET()
        if path.startswith("/assets/") or path.startswith("/logos/"):
            return super().do_GET()
        record = ROUTES["pages"].get(path)
        if path == "/project/":
            record = {"file": "project-archive.html", "css": "assets/css/project-archive.css"}
        if path == "/author/amicus/":
            record = {"file": "author-amicus.html", "css": "assets/css/author-amicus.css"}
        if not record:
            self.send_error(404)
            return
        page = (ROOT / record["file"]).read_text(encoding="utf-8")
        page = page.replace(
            '[amicus_project_archive]',
            '<div class="amicus-archive-list"><article class="amicus-project-card"><a href="/project/test/"><h2>test</h2></a></article></div><form action="/" role="search"><input type="search" name="s" aria-label="Search"><button>Search</button></form>',
        ).replace(
            '[amicus_author_archive]',
            '<h1>No Results Found</h1><form action="/" role="search"><input type="search" name="s" aria-label="Search"><button>Search</button></form>',
        ).replace('[amicus_comments]', '<div class="amicus-preview-comment-note">WordPress renders the native comment form here.</div>')
        page = re.sub(
            r'\[amicus_jotform id="([0-9]+)"\]',
            r'<iframe title="Amicus grant application" src="https://form.jotform.com/\1" loading="lazy"></iframe>',
            page,
        )
        page = re.sub(
            r'\[amicus_youtube id="([A-Za-z0-9_-]+)"\]',
            r'<iframe title="Amicus Foundation video" src="https://www.youtube.com/embed/\1" loading="lazy" allowfullscreen></iframe>',
            page,
        )
        page = re.sub(
            r'\[gitpress_form id="(?:__AMICUS_CONTACT_FORM_ID__|[0-9]+)"\]',
            '<form class="amicus-preview-form" onsubmit="return false"><label>Name<input required></label><label>Email Address<input type="email" required></label><label>Message<textarea required></textarea></label><button type="submit">Submit</button></form>',
            page,
        )
        page = re.sub(r'\[amicus_form_status id="(?:__AMICUS_CONTACT_FORM_ID__|[0-9]+)"\]', '', page)
        for k, v in (
            ('https://amicusfoundation.com/wp-content/', '/wp-content/'),
            ('//amicusfoundation.com/wp-content/', '/wp-content/'),
        ):
            page = page.replace(k, v)
        header = (ROOT / "header.html").read_text(encoding="utf-8")
        footer = (ROOT / "footer.html").read_text(encoding="utf-8")
        header = header.replace('https://amicusfoundation.com/wp-content/', '/wp-content/')
        footer = footer.replace('https://amicusfoundation.com/wp-content/', '/wp-content/')
        site = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Amicus GitPress preview - {html.escape(path)}</title>
<link rel="stylesheet" href="/{record['css']}"><link rel="stylesheet" href="/assets/css/site.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800&amp;subset=latin,latin-ext&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Plus+Jakarta+Sans:200,300,regular,500,600,700,800,200italic,300italic,italic,500italic,600italic,700italic,800italic|Poppins:100,100italic,200,200italic,regular,italic,500,500italic,600,600italic,700,700italic,800,800italic,900,900italic|Roboto:100,200,300,regular,italic,500,500italic,700,700italic,900,900italic|Inter:100,200,300,regular,500,600,700,800,900|Roboto+Condensed:300,300italic,regular,italic,700,700italic|Manrope:200,300,regular,500,600,700,800|Oswald:200,300,regular,500,600,700|Lora:regular,500,600,700,italic,500italic,600italic,700italic|Urbanist:100,200,300,regular,500,600,700,800,900,100italic,200italic,300italic,italic,500italic,600italic,700italic,800italic,900italic|DM+Sans:regular,italic,500,500italic,700,700italic&amp;subset=latin,latin-ext&amp;display=swap">
</head><body class="dgs-gitpress-managed et_pb_pagebuilder_layout et_pb_button_helper_class et-db"><div class="dgs-managed-page">
<header class="dgs-managed-header">{header}</header><main class="dgs-managed-main" id="main">{page}</main><footer class="dgs-managed-footer">{footer}</footer></div>
<script src="/assets/js/site.js"></script></body></html>'''
        data = site.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def translate_path(self, path):
        return str(ROOT / path.split("?", 1)[0].lstrip("/"))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    print(f"Preview at http://127.0.0.1:{args.port}/")
    ThreadingHTTPServer(("127.0.0.1", args.port), Preview).serve_forever()
