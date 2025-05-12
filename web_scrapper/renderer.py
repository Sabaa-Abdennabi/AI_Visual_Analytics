# renderer.py
from playwright.sync_api import sync_playwright

def render_page(url, headless=True, delay=3):
    with sync_playwright() as p:  # <--- scoped inside each scrape
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 ...",
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(delay * 1000)
        return page.content(), url  # just return the content (DOM), don't pass browser or page objects between processes
