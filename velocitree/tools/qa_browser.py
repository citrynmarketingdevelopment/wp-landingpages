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
            # The panel is a full-screen overlay: it spans the viewport and clears the fixed bar.
            nav_bounds = page.locator('.vts-mobile-nav').bounding_box()
            header_height = page.locator('#siteHeader').bounding_box()['height']
            assert nav_bounds['width'] == 390, nav_bounds
            assert round(nav_bounds['y']) == round(header_height), (nav_bounds, header_height)
            assert round(nav_bounds['y'] + nav_bounds['height']) == 844, nav_bounds
            assert page.locator('#main-content').evaluate('(e)=>e.getBoundingClientRect().top') >= header_height - 0.5
            link = page.locator('.vts-mobile-nav > a').first
            link_bounds = link.bounding_box()
            assert float(link.evaluate('(e)=>getComputedStyle(e).fontSize')[:-2]) >= 26
            assert abs((link_bounds['x'] + link_bounds['width'] / 2) - 195) < 1, link_bounds
            assert page.locator('#vtsMenuToggle').bounding_box()['width'] <= 46
            # Open state: the toggle sits at the overlay's top-left and keeps a 44px tap target.
            toggle_box = page.locator('#vtsMenuToggle').bounding_box()
            assert toggle_box['x'] == 20 and toggle_box['y'] >= header_height, toggle_box
            assert min(toggle_box['width'], toggle_box['height']) >= 44, toggle_box
            assert toggle_box['y'] + toggle_box['height'] <= link_bounds['y'], (toggle_box, link_bounds)
            assert '157, 182, 77' in page.locator('.vts-mobile-nav > .vts-header-cta').evaluate('(e)=>getComputedStyle(e).boxShadow')
            if js:
                page.wait_for_function('document.querySelector("#vtsMenuToggle").getAttribute("aria-expanded") === "true"')
                assert page.evaluate('getComputedStyle(document.body).overflow') == 'hidden'
                page.keyboard.press('Escape')
                assert menu.get_attribute('open') is None
                assert page.evaluate('getComputedStyle(document.body).overflow') != 'hidden'
                assert toggle.evaluate('(e)=>e===document.activeElement')
                toggle.click()
                # Empty space in the bar itself is outside the menu, so it dismisses.
                page.mouse.click(200, 36)
                assert menu.get_attribute('open') is None
            else:
                toggle.click()
                assert menu.get_attribute('open') is None
            page.evaluate('window.scrollTo(0, 1200)')
            assert page.locator('#siteHeader').evaluate('(e)=>getComputedStyle(e).position') == 'fixed'
            assert round(page.locator('#siteHeader').bounding_box()['y']) == 0
            report['checks'].append(f'{name}: mobile bar stays pinned and the menu opens full screen with JS {js}')
            page.evaluate('window.scrollTo(0, 0)')
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
                assert page.locator('a[href^="mailto:ed@velocitreegroup.com"]').count() >= 1
                assert page.locator('.vts-contact-button[href="#inquiry"]').count() == 1
                report['checks'].append(f'{name}: contact navigation closes menu and reaches contact page')
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
        navigate(page, name)
        page.add_style_tag(content=HOSTILE_THEME_CSS)
        toggle = page.locator('#vtsMenuToggle')
        assert toggle.evaluate('(e)=>getComputedStyle(e).display') == 'flex'
        assert toggle.evaluate('(e)=>getComputedStyle(e).listStyleType') == 'none'
        assert toggle.evaluate("(e)=>getComputedStyle(e, '::marker').content") in ('""', 'none')
        assert toggle.bounding_box()['width'] <= 46
        toggle.click()
        link = page.locator('.vts-mobile-nav > a').first
        assert float(link.evaluate('(e)=>getComputedStyle(e).fontSize')[:-2]) >= 26
        assert float(link.evaluate('(e)=>getComputedStyle(e).minHeight')[:-2]) >= 60
        cta = page.locator('.vts-mobile-nav > .vts-header-cta')
        assert float(cta.evaluate('(e)=>getComputedStyle(e).fontSize')[:-2]) >= 17
        report['checks'].append(f'{name}: menu keeps its size and hides the triangle under theme overrides')
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
