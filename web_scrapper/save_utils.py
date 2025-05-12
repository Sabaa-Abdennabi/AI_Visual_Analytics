# save_utils.py
import pandas as pd
import hashlib
import os

def save_as_parquet(elements, url, output_dir="scraped_parquet"):
    os.makedirs(output_dir, exist_ok=True)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
    filename = f"{url_hash}.parquet"
    path = os.path.join(output_dir, filename)
    
    df = pd.DataFrame(elements)
    df["source_url"] = url
    df.to_parquet(path, index=False)
