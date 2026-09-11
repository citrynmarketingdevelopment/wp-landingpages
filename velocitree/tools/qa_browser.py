"""Optional local browser QA. Requires Playwright and an installed Chrome browser.

Install once: python -m pip install playwright
Run: python velocitree/tools/qa_browser.py
"""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CHROME = Path(os.environ.get('PROGRAMFILES', 'C:/Program Files')) / 'Google/Chrome/Application/chrome.exe'
report = {'status': 'running', 'checks': [], 'scope': 'Local previews; live WordPress is not configured'}
# Number of line boxes the element's contents actually render on.
LINE_COUNT = '(e) => { const r = document.createRange(); r.selectNodeContents(e); return r.getClientRects().length; }'


def navigate(page, name):
    page.goto((ROOT / f'preview/velocitree-{name}-preview.html').as_uri())
    page.evaluate('document.fonts.ready')
    # Force deferred images to load for the asset check and full-page captures.
    page.evaluate('''async () => { await Promise.all([...document.images].map(async i => { i.loading='eager'; await i.decode(); })); }''')


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=str(CHROME), headless=True)
    for js in (True, False):
        context = browser.new_context(java_script_enabled=js, device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for name in ('home', 'contact'):
            for width in (320, 390, 768, 1024, 1440):
                page.set_viewport_size({'width': width, 'height': 900})
                navigate(page, name)
                stats = page.evaluate('''() => ({ width:innerWidth, contentWidth:document.documentElement.scrollWidth, images:[...document.images].filter(i=>!i.complete || !i.naturalWidth).map(i=>i.src), main:document.querySelectorAll('main').length, header:document.querySelectorAll('header').length, footer:document.querySelectorAll('footer').length, font:document.fonts.check('600 16px "VTS Sans"') })''')
                assert stats['contentWidth'] <= width, (name, js, stats)
                assert not stats['images'], (name, stats)
                assert (stats['main'], stats['header'], stats['footer']) == (1, 1, 1)
                assert stats['font']
                report['checks'].append(f'{name}: {width}px, JS {js}: no overflow; images, fonts and shell OK')
            page.set_viewport_size({'width': 390, 'height': 844})
            navigate(page, name)
            # No hamburger anywhere: the bar is the brand plus one call to action.
            assert page.locator('#vtsMobileMenu').count() == 0
            assert page.locator('summary', has_text='Menu').count() == 0
            assert page.locator('#siteHeader details').count() == 0
            cta = page.locator('#siteHeader .vts-header-cta')
            assert cta.count() == 1 and cta.is_visible()
            # One line: count the rendered line boxes of the label rather than trusting height,
            # which the button's min-height floor would mask.
            assert cta.evaluate(LINE_COUNT) == 1, cta.inner_text()
            assert cta.locator('span, svg').count() == 0
            assert cta.inner_text().strip() == "Let's connect"

            assert cta.evaluate('(e)=>e.scrollWidth <= e.clientWidth + 1')
            # The bar stays pinned while the page scrolls.
            page.evaluate('window.scrollTo(0, 1200)')
            assert page.locator('#siteHeader').evaluate('(e)=>getComputedStyle(e).position') == 'fixed'
            assert round(page.locator('#siteHeader').bounding_box()['y']) == 0
            report['checks'].append(f'{name}: mobile bar stays pinned; CTA replaces the menu on one line with JS {js}')
            page.evaluate('window.scrollTo(0, 0)')
            first = page.locator('main details').first
            prior = first.get_attribute('open') is not None
            first.locator('summary').click()
            assert (first.get_attribute('open') is not None) != prior
            report['checks'].append(f'{name}: native menu and disclosures pass with JS {js}')
            if js:
                page.locator('#siteHeader .vts-header-cta').click()
                page.wait_for_url('**/velocitree-contact-preview.html')
                assert page.locator('a[href="tel:+19095618661"]').count() >= 1
                assert page.locator('a[href^="mailto:ed@velocitreegroup.com"]').count() >= 1
                assert page.locator('.vts-contact-button[href="#inquiry"]').count() == 1
                report['checks'].append(f'{name}: header call to action reaches the contact page')
        assert not errors, errors
        context.close()
    # The live WordPress theme outranks plain class selectors with ID-scoped and !important
    # rules, and resets summary display, which is what shrank the menu text and brought back
    # the disclosure triangle. Re-run the mobile menu under those rules.
    HOSTILE_THEME_CSS = '''
    #page-container a, body #page-container .et_pb_section a { font-size: 14px; font-weight: 400; line-height: 1.7; }
    body a { font-size: 15px !important; }
    body summary { display: list-item !important; list-style: disclosure-closed !important; }
    body details > summary { list-style-type: disclosure-closed; }
    '''
    context = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    page = context.new_page()
    for name in ('home', 'contact'):
        for width in (320, 360, 390, 430):
            page.set_viewport_size({'width': width, 'height': 844})
            navigate(page, name)
            page.add_style_tag(content=HOSTILE_THEME_CSS)
            cta = page.locator('#siteHeader .vts-header-cta')
            assert cta.evaluate(LINE_COUNT) == 1, (name, width, cta.inner_text())
            assert cta.evaluate('(e)=>e.scrollWidth <= e.clientWidth + 1'), (name, width)
            assert page.evaluate('document.documentElement.scrollWidth') <= width, (name, width)
        report['checks'].append(f'{name}: header CTA stays on one line from 320 to 430px under theme overrides')
    context.close()

    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1, reduced_motion='reduce')
    page = context.new_page()
    navigate(page, 'home')
    for area in ('leadership', 'financial', 'operations', 'safety', 'contracts', 'technology'):
        page.locator(f'.vts-overview__item[href$="#{area}"]').click()
        page.wait_for_function('(id) => document.getElementById(id).open', arg=area)
        assert page.locator(f'#{area} p').is_visible()
    report['checks'].append('home: all six service links reveal their matching expertise descriptions')
    page.goto((ROOT / 'preview/velocitree-home-preview.html').as_uri() + '#technology')
    page.wait_for_function('document.getElementById("technology").open')
    report['checks'].append('home: direct expertise anchor opens on initial load')

    # Responsive art: phones take the pre-cropped portrait frame, wider screens the width ladder,
    # and the emblem steps up by device pixel ratio.
    for label, vp, dpr, expect_hero, expect_emblem in (
        ('phone', {'width': 390, 'height': 844}, 3, 'vts-hero-mobile.webp', 'vts-emblem-3x.webp'),
        ('phone-2x', {'width': 430, 'height': 932}, 2, 'vts-hero-mobile.webp', 'vts-emblem-2x.webp'),
        ('tablet', {'width': 768, 'height': 1024}, 2, 'vts-hero-1672.webp', 'vts-emblem-2x.webp'),
        ('desktop', {'width': 1440, 'height': 900}, 1, 'vts-hero-1672.webp', 'vts-emblem.webp'),
    ):
        art = browser.new_context(viewport=vp, device_scale_factor=dpr)
        art_page = art.new_page()
        navigate(art_page, 'home')
        hero = art_page.locator('.vts-hero__image')
        emblem = art_page.locator('.vts-brand-emblem img')
        assert hero.evaluate('(e)=>e.currentSrc').endswith(expect_hero), (label, hero.evaluate('(e)=>e.currentSrc'))
        assert emblem.evaluate('(e)=>e.currentSrc').endswith(expect_emblem), (label, emblem.evaluate('(e)=>e.currentSrc'))
        assert hero.evaluate('(e)=>e.complete && e.naturalWidth > 0')
        # The portrait crop is already framed, so it must not be re-offset.
        pos = hero.evaluate('(e)=>getComputedStyle(e).objectPosition')
        assert pos == ('50% 50%' if expect_hero == 'vts-hero-mobile.webp' else '50% 43%'), (label, pos)
        # The emblem keys to transparency; a stray opaque field would break the dark bar.
        assert emblem.evaluate('(e)=>e.naturalWidth') <= 156
        report['checks'].append(f'{label}: hero serves {expect_hero} and the emblem serves {expect_emblem}')
        art.close()
    assert '[fluentform id="1"]' in (ROOT / 'contact.html').read_text(encoding='utf-8')
    navigate(page, 'contact')
    assert page.locator('.vts-contact-form .vts-form-preview').is_visible()
    assert page.locator('.vts-contact-form form').count() == 0
    report['checks'].append('contact: real shortcode in source; clearly labeled preview without simulated submission')
    for name in ('home', 'contact'):
        navigate(page, name)
        page.screenshot(path=str(ROOT / f'preview/{name}-desktop.png'), full_page=True)
        if name == 'home':
            page.screenshot(path=str(ROOT / 'preview/home-first-screen.png'))
        page.keyboard.press('Tab')
        assert page.locator('.vts-skip-link').evaluate('(e)=>e===document.activeElement')
        page.keyboard.press('Enter')
        assert page.evaluate('location.hash') == '#main-content'
        page.set_viewport_size({'width': 390, 'height': 844})
        navigate(page, name)
        page.screenshot(path=str(ROOT / f'preview/{name}-mobile.png'), full_page=True)
        if name == 'home':
            page.screenshot(path=str(ROOT / 'preview/home-mobile-first-screen.png'))
        page.set_viewport_size({'width': 1440, 'height': 1000})
        report['checks'].append(f'{name}: keyboard skip link and reduced-motion rendering pass')
    browser.close()

report['status'] = 'passed'
(ROOT / 'preview/qa-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(f"PASS: {len(report['checks'])} browser checks. Screenshots and qa-report.json saved in preview/.")
