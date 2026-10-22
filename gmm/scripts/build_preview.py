"""Assemble the GitPress fragments into a standalone local review document."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RAW = 'https://raw.githubusercontent.com/citrynmarketingdevelopment/wp-landingpages/main/gmm/'

def build(source='home.html', output='index.html', title='GMM homepage', main_id='gmm-home', current_nav='home'):
    partials = '\n'.join((ROOT / name).read_text(encoding='utf-8') for name in ('header.html', source, 'footer.html'))
    partials = partials.replace(RAW, '../')
    # WordPress routes retain their real destination in this static preview.
    news = '#gmm-news' if source == 'home.html' else 'index.html#gmm-news'
    partials = partials.replace('href="/#gmm-news"', f'href="{news}"')
    partials = partials.replace('href="/clients/"', 'href="clients.html"').replace('href="/"', 'href="index.html"')
    partials = partials.replace(f'data-nav="{current_nav}"', f'data-nav="{current_nav}" aria-current="page"')
    partials = re.sub(r'href="(/[^\"]*)"', r'href="https://genesismedicalmanagement.com\1"', partials)
    document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>GMM homepage | Local review</title><style>html{scroll-behavior:smooth}body{margin:0;background:#fff}body:has(.gmm-header__mobile[open]){overflow-x:hidden}.gmm-preview-skip{position:absolute;left:20px;top:-90px;background:#191827;color:#fff;padding:12px 20px;z-index:100;font:700 16px Arial}.gmm-preview-skip:focus{top:12px}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}</style></head><body><a class="gmm-preview-skip" href="#gmm-home">Skip to content</a>'''
    document = document.replace('GMM homepage | Local review', title + ' | Local review').replace('href="#gmm-home"', f'href="#{main_id}"')
    document += partials + '\n</body></html>\n'
    out = ROOT / 'preview' / output
    out.parent.mkdir(exist_ok=True)
    out.write_text(document, encoding='utf-8')
    print(f'Preview ready: {out}')

if __name__ == '__main__':
    build()
    build('clients.html', 'clients.html', 'GMM Our Organizations', 'gmm-clients', 'clients')
