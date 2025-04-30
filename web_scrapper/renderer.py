#websrcaper/renderer.py
from playwright.sync_api import sync_playwright

def render_page(url, headless=True, delay=3):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")  # <--- FIXED
    page.wait_for_timeout(delay * 1000)  # Delay after load to stabilize dynamic content
    return browser, page
