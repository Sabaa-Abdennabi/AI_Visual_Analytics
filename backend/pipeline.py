import hashlib
import os
import pandas as pd
import joblib
from web_scrapper.scraper import scrape
from heatmap.generate_heatmap import generate_heatmap

def url_to_hash(url):
    return hashlib.md5(url.encode()).hexdigest()[:10]

def run_pipeline(url):
    # 1. Scrape the URL (saves .parquet in scraped_parquet)
    scrape(url)

    # 2. Get the .parquet file name
    url_hash = url_to_hash(url)
    scraped_path = f"web_scrapper/scraped_parquet/{url_hash}.parquet"
    #merged_path = f"web_scrapper/merged_parquet/{url_hash}.parquet"

    if not os.path.exists(scraped_path):
        raise FileNotFoundError("No scraped .parquet file found for this URL.")

    # 3. Load DataFrame and add required columns
    df = pd.read_parquet(scraped_path)
    df["view_duration"] = 0
    df["time_on_site"] = 0
    df["session_id"] = "dummy_session"
    df["page_url"] = url

    # 4. Save enriched DataFrame to merged_parquet
    os.makedirs("web_scrapper/merged_parquet", exist_ok=True)

    #5. Predict was_viewed and was_clicked

    #nloadou model l views
    model1 = joblib.load("path/to/model_viewed.pkl")
    predictions1 = model1.predict(df)
    df["was_viewed"] = predictions1

    #nloadou model l clicks
    model2 = joblib.load("path/to/model_viewed.pkl")
    predictions2 = model2.predict(df)
    df["was_clicked"] = predictions2


    # 7. Call generate_heatmap
    generate_heatmap(url, df)