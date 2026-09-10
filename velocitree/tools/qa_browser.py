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
            menu = page.locator('#vtsMobileMenu')
            toggle = page.locator('#vtsMenuToggle')
            toggle.click()
            assert menu.get_attribute('open') is not None
            assert page.locator('.vts-mobile-nav').is_visible()
            if js:
                page.wait_for_function('document.querySelector("#vtsMenuToggle").getAttribute("aria-expanded") === "true"')
                page.keyboard.press('Escape')
                assert menu.get_attribute('open') is None
                assert toggle.evaluate('(e)=>e===document.activeElement')
                toggle.click()
                nav_bounds = page.locator('.vts-mobile-nav').bounding_box()
                page.mouse.click(5, nav_bounds['y'] + nav_bounds['height'] + 15)
                assert menu.get_attribute('open') is None
            else:
                toggle.click()
                assert menu.get_attribute('open') is None
            first = page.locator('main details').first
            prior = first.get_attribute('open') is not None
            first.locator('summary').click()
            assert (first.get_attribute('open') is not None) != prior
            report['checks'].append(f'{name}: native menu and disclosures pass with JS {js}')
            if js:
                toggle.click()
                page.locator('.vts-mobile-nav [data-nav="contact"]').click()
                page.wait_for_url('**/velocitree-contact-preview.html')
                assert page.locator('#vtsMobileMenu').get_attribute('open') is None
                assert page.locator('a[href="tel:+19095618661"]').count() >= 1
                assert page.locator('a[href^="mailto:velocitreesolutions@outlook.com"]').count() >= 1
                report['checks'].append(f'{name}: contact navigation closes menu and reaches contact page')
        assert not errors, errors
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
