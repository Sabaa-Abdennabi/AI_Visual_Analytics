import hashlib
import os
import pandas as pd
import joblib
from web_scrapper.scraper import scrape
from heatmap.generate_heatmap import generate_heatmap
from backend.preprocessing import preprocess_dataframe

def url_to_hash(url):
    return hashlib.md5(url.encode()).hexdigest()[:10]

def extract_metrics(df):
    total_elements = len(df)
    clicked_elements = df["was_clicked"].sum() if "was_clicked" in df else 0
    viewed_elements = df["was_viewed"].sum() if "was_viewed" in df else 0

    percent_clicked = (clicked_elements / total_elements) * 100 if total_elements else 0
    percent_viewed = (viewed_elements / total_elements) * 100 if total_elements else 0

    print(f"Total elements: {total_elements}")
    print(f"Clicked elements: ({percent_clicked:.2f}%)")
    print(f"Viewed elements: ({percent_viewed:.2f}%)")

    # Add more metrics as needed, for example:
    if "view_duration" in df:
        avg_view_duration = df["view_duration"].mean()
        print(f"Average view duration: {avg_view_duration:.2f}")

    if "area" in df:
        avg_area = df["area"].mean()
        print(f"Average element area: {avg_area:.2f}")

    # Return as dict if you want to use it elsewhere
    return {
        "total_elements": total_elements,
        "percent_clicked": percent_clicked,
        "percent_viewed": percent_viewed,
        "avg_area": float(df["area"].mean()) if "area" in df else None,
    }

def run_pipeline(url):
    # 1. Scrape the URL (saves .parquet in scraped_parquet)
    path=scrape(url)

    if not os.path.exists(path):
        raise FileNotFoundError("No scraped .parquet file found for this URL.")

    df = pd.read_parquet(path)
    df["view_duration"] = 0
    df["time_on_site"] = 0
    df["session_id"] = "dummy_session"
    df["page_url"] = url
    df= preprocess_dataframe(df)

    backend_dir = os.path.dirname(__file__)
    model1 = joblib.load(os.path.join(backend_dir, "model_view.pkl"))
    model2 = joblib.load(os.path.join(backend_dir, "model_click.pkl"))
    feature_names = model1.feature_names_in_
    df_model = df[feature_names]
    predictions1 = model1.predict(df_model)
    df["was_viewed"] = predictions1
    predictions2 = model2.predict(df_model)
    df["was_clicked"] = predictions2

    print(df.head())
    # 7. Call generate_heatmap
    generate_heatmap(url, df)
    metrics = extract_metrics(df)
    return metrics

# if __name__ == "__main__":
#     # Example usage
#     url = "https://www.ikea.com/fr/fr/p/friheten-convertible-3-places-skiftebo-gris-fonce-50341148/"
#     run_pipeline(url)