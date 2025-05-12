import pandas as pd
import json
import hashlib
import os

def enrich_parquet_with_session_data(session: pd.Series, parquet_dir="scraped_parquet", output_dir="merged_parquet"):
    """
    Enriches the DOM .parquet file of a URL with interaction data from a user session.
    Adds: was_viewed, view_duration, was_clicked, time_on_site, session_id, page_url.
    Saves result to output_dir using the same hashed name.
    """
    url = session["PageURL"]
    url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
    input_path = os.path.join(parquet_dir, f"{url_hash}.parquet")
    output_path = os.path.join(output_dir, f"{url_hash}.parquet")

    if not os.path.exists(input_path):
        print(f"❌ Parquet file not found for URL: {url}")
        return

    # Load DOM snapshot
    dom_df = pd.read_parquet(input_path)

    # Parse viewed sections
    viewed_dict = json.loads(session["Sections Viewed"])

        # Safe get_view_data function
    def get_view_data(row):
        try:
            for key, duration in viewed_dict.items():
                if key in str(row.get("sectionViewedElement", "")):
                    return True, duration
            return False, 0
        except Exception:
            return False, 0

    # Apply and expand manually
    view_data = dom_df.apply(get_view_data, axis=1)
    view_data_df = pd.DataFrame(view_data.tolist(), columns=["was_viewed", "view_duration"])
    dom_df = pd.concat([dom_df, view_data_df], axis=1)

    # Parse clicked elements
    try:
        clicked_elements = json.loads(session["Click Count"])  # this should be a JSON list of dicts
        clicked_selectors = [e["element"] for e in clicked_elements]
    except Exception:
        clicked_selectors = []

    def get_clicked(row):
        try:
            for sel in clicked_selectors:
                if isinstance(row.get("clickElement", ""), str) and sel in row["clickElement"]:
                    return True
            return False
        except Exception:
            return False


    dom_df["was_clicked"] = dom_df.apply(get_clicked, axis=1)

    # Add time on site
    dom_df["time_on_site"] = pd.to_timedelta(session['TotalTime ( H:M:S)']).total_seconds() if isinstance(session['TotalTime ( H:M:S)'], str) else None

    # Add session metadata
    dom_df["session_id"] = session["SessionId"]
    dom_df["page_url"] = url

    # Save enriched file
    os.makedirs(output_dir, exist_ok=True)
    dom_df.to_parquet(output_path, index=False)
    print(f"✅ Saved enriched data to {output_path}")