"""Archive public brand assets referenced by the supplied homepage HTML."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'reference' / 'Genesis Medical Management _ Medical Management based in Phoenix.html'
SOUP = BeautifulSoup(REFERENCE.read_text(encoding='utf-8'), 'html.parser')
BASE = 'https://genesismedicalmanagement.com/wp-content/uploads/'
ASSETS = [
    ('logo.png', BASE + '2020/12/Genesis-Medical-Management-Logo-1-min.png'),
    ('logo-light.png', BASE + '2019/07/1.png'),
    ('original-hero.webp', BASE + '2026/03/GMM-Header-1-scaled.jpg'),
    ('grow-background.jpg', BASE + '2019/07/church-01.jpg'),
    ('revenue-cycle.png', BASE + '2020/12/Money-min.png'),
    ('growth.png', BASE + '2020/12/Chart-min.png'),
    ('operations.png', BASE + '2020/12/Operations-Management-min.png'),
    ('development.png', BASE + '2020/12/building-min.png'),
    ('aspire-logo.png', BASE + '2020/12/ACS-min.png'),
    ('pwc-logo.png', BASE + '2020/12/PWC-1-min.png'),
    ('brs-logo.webp', BASE + '2026/10/BRS-Final.webp'),
    ('inspire-me-logo.png', BASE + '2026/10/InspireMe-Logo-2024.png'),
    ('clients-hero.webp', BASE + '2019/08/OurClients1-min.jpeg'),
    ('tpmg-logo.png', BASE + '2019/08/Untitled-design-2.png'),
]
for index, card in enumerate(SOUP.select('.location-card'), 1):
    url = re.search(r"url\('([^']+)'\)", card['style'])[1]
    ASSETS.append((f'location-{index:02}.webp', url))

FONTS = [
    ('hind-regular.woff2', 'https://fonts.gstatic.com/s/hind/v18/5aU69_a8oxmIdGd4BA.woff2'),
    ('hind-bold.woff2', 'https://fonts.gstatic.com/s/hind/v18/5aU19_a8oxmIfNJdERKSjQ.woff2'),
    ('khand-bold.woff2', 'https://fonts.gstatic.com/s/khand/v22/TwMN-IINQlQQ0bLpd2E-bQc.woff2'),
]
ICONS = [(f'{name}.svg', f'https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/{name}.svg') for name in ('receipt-dollar', 'trending-up', 'settings-heart', 'building-community')]
ICONS.append(('LICENSE', 'https://raw.githubusercontent.com/tabler/tabler-icons/main/LICENSE'))

def fetch(item, folder):
    name, url = item
    dest = ROOT / 'assets' / folder / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req, timeout=45).read()
        if folder == 'images':
            im = Image.open(BytesIO(data))
            im = ImageOps.exif_transpose(im)
            im.thumbnail((2560, 1600) if name.startswith('original') else (1100, 900))
            if dest.suffix == '.webp':
                mode = 'RGBA' if im.mode == 'RGBA' or 'transparency' in im.info else 'RGB'
                im.convert(mode).save(dest, quality=86)
            else:
                im.save(dest, optimize=True)
        else:
            dest.write_bytes(data)
    return {'file': str(dest.relative_to(ROOT)).replace('\\', '/'), 'source': url}

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=6) as pool:
        images = list(pool.map(lambda item: fetch(item, 'images'), ASSETS))
        fonts = list(pool.map(lambda item: fetch(item, 'fonts'), FONTS))
        icons = list(pool.map(lambda item: fetch(item, 'icons'), ICONS))
    (ROOT / 'assets' / 'sources.json').write_text(json.dumps(images + fonts + icons, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(images)} images, {len(fonts)} self-hosted fonts, and {len(icons)-1} icons with their license.')
