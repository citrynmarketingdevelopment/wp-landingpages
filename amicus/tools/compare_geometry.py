"""Print a few source/preview bounds to guide visual review."""

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width in (1440, 1024, 390):
        for label, url in (("source", "https://amicusfoundation.com/"), ("preview", "http://127.0.0.1:8765/")):
            page = browser.new_page(viewport={"width": width, "height": 900})
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.evaluate("document.fonts.ready")
            print(label, width, page.evaluate("""() => {
              const boxes = {};
              for (const [name, selector] of Object.entries({
                header: '.dgs-managed-header, header.et-l--header',
                headline: '.et_pb_cta_0 h2',
                description: '.et_pb_cta_0 .et_pb_promo_description p:last-child',
                firstButton: '.et_pb_button_0',
                counters: '.et_pb_row_inner_2',
              })) {
                const el = document.querySelector(selector);
                if (el) {
                  const r = el.getBoundingClientRect();
                  const cs = getComputedStyle(el);
                  boxes[name] = [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height), cs.fontFamily, cs.fontSize, cs.fontWeight, el.scrollWidth];
                }
              }
              return boxes;
            }"""))
            page.close()
    browser.close()
