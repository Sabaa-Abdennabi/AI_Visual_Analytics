import hashlib
import os
import pandas as pd
import joblib
from web_scrapper.scraper import scrape
from heatmap.generate_heatmap import generate_heatmap
from backend.preprocessing import preprocess_dataframe
from backend.preprocessingHeatmap import preprocess_heatmap
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
def Moyenne_Duration(df):
    if "view_duration" in df:
        return df["view_duration"].mean()
    return 0

def run_pipeline(url):
    # 1. Scrape the URL (saves .parquet in scraped_parquet)
    path=scrape(url)
    if not os.path.exists(path):
        raise FileNotFoundError("No scraped .parquet file found for this URL.")
    
    df = pd.read_parquet(path)

    df["time_on_site"] = 0
    df["session_id"] = "dummy_session"
    df["page_url"] = url
    df2=df.copy()
    df["view_duration"] = 0
    df= preprocess_dataframe(df)

    backend_dir = os.path.dirname(__file__)
    model1 = joblib.load(os.path.join(backend_dir, "model_view_xgb_noscale.pkl"))
    model2 = joblib.load(os.path.join(backend_dir, "model_click.pkl"))
    feature_names = model2.feature_names_in_
    df_model = df[feature_names]
    predictions1 = model1.predict(df_model)
    df["was_viewed"] = predictions1
    predictions2 = model2.predict(df_model)
    df["was_clicked"] = predictions2

    metrics = extract_metrics(df)
    df2= preprocess_heatmap(df2)
    modelHeatMap = joblib.load(os.path.join(backend_dir, "modele_random_forest2.pkl"))
    scaler_y = joblib.load(os.path.join(backend_dir, "scaler_y.pkl"))
    scaler_x = joblib.load(os.path.join(backend_dir, "scaler_x.pkl"))
    feature_namesHeatmap = modelHeatMap.feature_names_in_
    df_modelHeatmap = df2[feature_namesHeatmap]
    predictions = modelHeatMap.predict(df_modelHeatmap)
    df2["view_duration"] = predictions
    df2["view_duration"] = scaler_y.inverse_transform(df2[["view_duration"]])
    df2['x'] = df2['x'] * scaler_x.scale_[0] + scaler_x.mean_[0]
    df2['y'] = df2['y'] * scaler_x.scale_[1] + scaler_x.mean_[1]

    df_valid = df2.dropna(subset=["x", "y", "view_duration"])
    df_valid = df_valid[df_valid["view_duration"] > 0]
    raw_points = [
        [float(row["x"]), float(row["y"]), float(row["view_duration"])]
        for _, row in df_valid.iterrows()
    ]
    mean_duration = Moyenne_Duration(df2)
    # 7. Call generate_heatmap
    heatmapPath=generate_heatmap(url,raw_points)
    return metrics,mean_duration,heatmapPath

if __name__ == "__main__":
     # Example usage
     url = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
     run_pipeline(url)