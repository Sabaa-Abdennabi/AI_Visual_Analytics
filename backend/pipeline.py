import hashlib
import os
import pandas as pd
import joblib
from web_scrapper.scraper import scrape
from heatmap.generate_heatmap import generate_heatmap
from backend.preprocessing import preprocess_dataframe
from LLM.request import generate_recommandations


def url_to_hash(url):
    return hashlib.md5(url.encode()).hexdigest()[:10]


def extract_metrics(df):
    total_elements = len(df)
    clicked_elements = df["was_clicked"].sum() if "was_clicked" in df else 0
    viewed_elements = df["was_viewed"].sum() if "was_viewed" in df else 0

    percent_clicked = (clicked_elements / total_elements) * \
        100 if total_elements else 0
    percent_viewed = (viewed_elements / total_elements) * \
        100 if total_elements else 0

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
    path = scrape(url)

    if not os.path.exists(path):
        raise FileNotFoundError("No scraped .parquet file found for this URL.")

    df = pd.read_parquet(path)
    df["view_duration"] = 0
    df["time_on_site"] = 0
    df["session_id"] = "dummy_session"
    df["page_url"] = url
    df = preprocess_dataframe(df)

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
    # generate recommendations with LLM

    metrics = extract_metrics(df)
    metrics_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])

    feature_cols = [col for col in df.columns if col not in [
        "was_viewed", "was_clicked"]]
    df_features = df[feature_cols]
    summary = df_features.describe().loc[["mean", "std", "min", "max"]].to_string()

    sample = df.head(5).to_string(index=False)

    message = (
        f"The website at {url} was scraped and analyzed.\n\n"
        f"Metrics summary:\n{metrics_str}\n\n"
        "Dataframe feature summary (excluding targets):\n"
        f"{summary}\n\n"
        "Sample of the first 10 elements with their features and predicted interactions (was_viewed, was_clicked):\n"
        f"{sample}\n\n"
        "Please provide UI/UX recommendations based on the heatmap, the metrics, the dataframe summary, and the element details above."
    )

    recommendations = generate_recommandations(
        image_path="smooth_heatmap.png",
        message=message
    )
    metrics["recommendations"] = recommendations
    return metrics

# if __name__ == "__main__":
# #     # Example usage
#     url = "https://www.ikea.com/fr/fr/p/friheten-convertible-3-places-skiftebo-gris-fonce-50341148/"
#     metrics =run_pipeline(url)
#     print(metrics)
