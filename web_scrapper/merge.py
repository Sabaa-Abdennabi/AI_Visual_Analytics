import pandas as pd
from merge_parquet import enrich_parquet_with_session_data

session_df = pd.read_csv("urls.csv")

for _, session in session_df.iterrows():
    enrich_parquet_with_session_data(session)
