"""Responsive, route and interaction checks against the local GitPress preview."""

from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "routes.json").read_text(encoding="utf-8"))
BASE = "http://127.0.0.1:8765"
WIDTHS = [(1440, 900), (1024, 768), (820, 1180), (768, 1024), (390, 844), (375, 812)]
BOUNDARIES = [1100, 981, 980, 767, 480, 479]
ROUTES = list(MANIFEST["pages"]) + list(MANIFEST["archives"])
SHOT_ROUTES = {"/", "/recommended-charities/", "/contact-us/"}
SHOT_WIDTHS = {1440, 820, 390}


def main() -> None:
    (ROOT / "qa" / "screenshots").mkdir(parents=True, exist_ok=True)
    outcomes = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for route in ROUTES:
            for width, height in WIDTHS:
                page = browser.new_page(viewport={"width": width, "height": height})
                response = page.goto(BASE + route, wait_until="domcontentloaded", timeout=30000)
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(100)
                result = {
                    "route": route,
                    "width": width,
                    "status": response.status if response else None,
                    "header": page.locator(".dgs-managed-header #siteHeader").count(),
                    "footer": page.locator(".dgs-managed-footer .amicus-footer").count(),
                    "horizontal_overflow": page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                    "content_characters": len(page.locator(".amicus-page").inner_text()) if page.locator(".amicus-page").count() else 0,
                    "media_elements": page.locator(".amicus-page img, .amicus-page video, .amicus-page iframe").count(),
                }
                if route in SHOT_ROUTES and width in SHOT_WIDTHS:
                    name = (route.strip("/").replace("/", "-") or "home") + f"-{width}.png"
                    page.screenshot(path=str(ROOT / "qa" / "screenshots" / name))
                outcomes.append(result)
                page.close()
        # The theme menu interaction is supplied by GitPress on WordPress and
        # by the same behavior in the standalone preview fallback.
        menu = browser.new_page(viewport={"width": 820, "height": 1000})
        menu.goto(BASE + "/", wait_until="domcontentloaded")
        menu.locator("#hamburger").click()
        menu_open = menu.evaluate("document.body.classList.contains('menu-open')")
        menu.locator("#mobileSheet .menu-item-has-children > a").first.click()
        submenu_open = menu.locator("#mobileSheet .menu-item-has-children.is-expanded").count() > 0
        menu.keyboard.press("Escape")
        menu_closed = not menu.evaluate("document.body.classList.contains('menu-open')")
        menu.close()
        slider = browser.new_page(viewport={"width": 1440, "height": 900})
        slider.goto(BASE + "/", wait_until="domcontentloaded")
        slider.locator(".et_pb_slider").first.locator(".amicus-slide-controls button[aria-label='Next slide']").click()
        slide_advanced = slider.locator(".et_pb_slider").first.locator(".et_pb_slide.is-active").count() == 1 and slider.locator(".et_pb_slider").first.locator(".et_pb_slide").nth(1).get_attribute("aria-hidden") == "false"
        toggle = slider.locator("details.amicus-toggle").first
        was_open = toggle.get_attribute("open") is not None
        toggle.locator("summary").click()
        accordion_toggled = (toggle.get_attribute("open") is not None) != was_open
        slider.wait_for_timeout(1850)
        counter_finishes = slider.locator(".et_pb_number_counter_0 .percent-value").first.inner_text() == "58M+"
        slider.close()
        reduced = browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        reduced.goto(BASE + "/", wait_until="domcontentloaded")
        reduced_motion_final = reduced.locator(".et_pb_number_counter_0 .percent-value").first.inner_text() == "58M+"
        reduced.close()
        no_js = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
        no_js_page = no_js.new_page()
        no_js_page.goto(BASE + "/", wait_until="domcontentloaded")
        no_js_content = no_js_page.locator(".amicus-page h1, .amicus-page h2").count() > 0
        no_js.close()
        boundary_results = []
        for width in BOUNDARIES:
            boundary = browser.new_page(viewport={"width": width, "height": 900})
            boundary.goto(BASE + "/", wait_until="domcontentloaded")
            boundary_results.append({
                "width": width,
                "overflow": boundary.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                "mobile_menu_visible": boundary.locator("#hamburger").is_visible(),
                "expected_mobile_menu": width <= 980,
            })
            boundary.close()
        browser.close()
    failed = [x for x in outcomes if x["status"] != 200 or x["header"] != 1 or x["footer"] != 1 or x["horizontal_overflow"] > 0 or (x["content_characters"] < 1 and x["media_elements"] < 1)]
    interactions = {"menu_open": menu_open, "submenu_open": submenu_open, "menu_closed_with_escape": menu_closed, "slider_advanced": slide_advanced, "accordion_toggled": accordion_toggled, "counter_finishes": counter_finishes, "reduced_motion_final": reduced_motion_final, "content_without_js": no_js_content}
    boundary_failures = [item for item in boundary_results if item["overflow"] > 0 or item["mobile_menu_visible"] != item["expected_mobile_menu"]]
    report = {"routes": len(ROUTES), "widths": [w for w, _ in WIDTHS], "checks": len(outcomes), "failures": failed, "boundaries": boundary_results, "boundary_failures": boundary_failures, "interactions": interactions}
    (ROOT / "qa" / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(outcomes), "failures": len(failed), "boundary_failures": len(boundary_failures), "interactions": interactions}, indent=2))
    if failed or boundary_failures or not all(interactions.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
