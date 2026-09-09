"""Sync the reusable hero and assemble full HTML previews. No dependencies.

Run from any directory: python velocitree/tools/build_preview.py
The GitPress partials remain the editable source; previews are generated output.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REMOTE = 'https://raw.githubusercontent.com/citrynmarketingdevelopment/wp-landingpages/main/velocitree/'


def inline_icons(markup):
    def replace(match):
        svg = (ROOT / 'assets' / 'icons' / (match.group(1) + '.svg')).read_text(encoding='utf-8')
        svg = re.sub(r'<\?xml[^>]*>|<!DOCTYPE[^>]*>|<!--.*?-->', '', svg, flags=re.S).strip()
        svg = re.sub(r'\s(?:width|height)="[^"]*"', '', svg)
        return svg.replace('<svg ', '<svg class="vts-icon" aria-hidden="true" focusable="false" ', 1)
    return re.sub(r'\{\{icon:([a-z-]+)\}\}', replace, markup)


def sync_sources():
    hero = inline_icons((ROOT / 'hero.html').read_text(encoding='utf-8'))
    (ROOT / 'hero.html').write_text(hero, encoding='utf-8')
    home = inline_icons((ROOT / 'home.html').read_text(encoding='utf-8'))
    home, count = re.subn(r'(?<=<!-- VTS:HERO:START -->).*?(?=<!-- VTS:HERO:END -->)', lambda _: '\n' + hero + '\n  ', home, flags=re.S)
    if count != 1:
        raise ValueError('home.html must contain exactly one VTS:HERO marker pair')
    (ROOT / 'home.html').write_text(home, encoding='utf-8')


def localize(markup):
    markup = markup.replace(REMOTE, '../')
    def route(match):
        quote, target = match.group(1), match.group(2)
        if target == '/contact/':
            target = 'velocitree-contact-preview.html'
        elif target == '/' or target.startswith('/#'):
            target = 'velocitree-home-preview.html' + target[1:]
        return 'href=' + quote + target + quote
    return re.sub(r'href=([\"\'])([^\"\']+)\1', route, markup)


def build(page, title, description):
    parts = [(ROOT / filename).read_text(encoding='utf-8') for filename in ('header.html', page + '.html', 'footer.html')]
    css = []
    def collect(match):
        css.append(match.group(1))
        return ''
    body = re.sub(r'<style>(.*?)</style>', collect, '\n'.join(parts), flags=re.S)
    document = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#111511">
  <title>{title}</title>
  <!-- GENERATED PREVIEW ONLY. Edit ../header.html, ../{page}.html, ../hero.html and ../footer.html. -->
  <style>
    html {{ scroll-behavior: smooth; background: #111511; }}
    body {{ margin: 0; min-width: 280px; }}
    @media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
    {''.join(css)}
  </style>
  <script src="../assets/js/shared.js" defer></script>
</head>
<body data-vts-preview-page="{page}">
{body}
</body>
</html>
'''
    target = ROOT / 'preview' / f'velocitree-{page}-preview.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(localize(document), encoding='utf-8')
    print('Built ' + str(target.relative_to(ROOT)))


if __name__ == '__main__':
    sync_sources()
    build('home', 'Velocitree Solutions | Strategic Advisory for the UVM Industry', 'Practical experience and strategic insight for growth in Utility Vegetation Management. From the Jobsite to the Boardroom.')
    build('contact', 'Contact Ed Martinez | Velocitree Solutions', 'Start with your business challenge. Connect with Ed Martinez at Velocitree Solutions for strategic advisory in the UVM industry.')
