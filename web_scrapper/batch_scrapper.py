import pandas as pd
from multiprocessing import Pool
from scraper import scrape

## run this script in order to scrappe the urls in the dataset 
## ajust the 3 number to the cores number of ur cpu -1  
## ater this run the merge.py folder to merge the session data with the scraped data
def process_url(url):
    try:
        scrape(url)
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

if __name__ == "__main__":
    df = pd.read_csv("urls_removed.csv")
    urls = df["PageURL"].dropna().unique().tolist()

    with Pool(10) as pool:
        pool.map(process_url, urls)
