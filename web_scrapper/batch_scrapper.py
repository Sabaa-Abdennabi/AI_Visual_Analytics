import pandas as pd
from multiprocessing import Pool
from scraper import scrape

def process_url(url):
    try:
        scrape(url)
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

if __name__ == "__main__":
    df = pd.read_csv("urls.csv")
    urls = df["PageURL"].dropna().unique().tolist()

    with Pool(3) as pool:
        pool.map(process_url, urls)
