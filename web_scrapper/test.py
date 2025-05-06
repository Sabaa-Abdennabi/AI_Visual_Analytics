import pandas as pd

df = pd.read_parquet("./scraped_parquet/1c2cc07030.parquet")
print(df.head())  # Show the first 5 rows
print(df.columns)       # List all column names
print(df.shape)         # (rows, columns)
print(df.sample(10))    # Random sample
