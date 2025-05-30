import pandas as pd
from merge_parquet import enrich_parquet_with_session_data


## run this script after fully scripping the urls
## this script is used to merge the session data with the scraped data
## the session data is in the urls.csv file, and the scraped data is in the scraped_parquet folder

session_df = pd.read_csv("urls_removed.csv")
for _, session in session_df.iterrows():
    enrich_parquet_with_session_data(session)
