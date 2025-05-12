from playwright.sync_api import sync_playwright
from custom_parser import extract_elements
from save_utils import save_as_parquet

def scrape(url, headless=True, delay=3):
    try:
        with sync_playwright() as p:
            print("start rendering")
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
                viewport={"width": 1920, "height": 1080},
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded")

            # Load dynamic content
            for _ in range(6):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(2000)
            print('end rendering start extracting')
            elements = extract_elements(page)
            print('end extracting and stt parqueting')
            save_as_parquet(elements, url)
            print('end parqueting')

            context.close()
            browser.close()

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
