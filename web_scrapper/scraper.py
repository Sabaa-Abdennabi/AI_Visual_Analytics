## orchestrator
# webscraper/scraper.py
from renderer import render_page
from custom_parser import extract_elements

def scrape(url):
    print("bch nabdou rendering")
    browser, page = render_page(url, headless=False, delay=5)
    print("kamalna rendering")
    try:
        print("bch nabdou l extraction")
        elements = extract_elements(page)
        print("kamalna l extraction")
    finally:
        browser.close()  # Close the browser
    return elements
