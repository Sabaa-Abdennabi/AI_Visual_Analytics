import pandas as pd

def convert_parquet_to_csv(parquet_file_path, csv_file_path):
    """
    Converts a Parquet file to a CSV file.

    :param parquet_file_path: Path to the input Parquet file
    :param csv_file_path: Path to the output CSV file
    """
    try:
        # Read the Parquet file
        df = pd.read_parquet(parquet_file_path)

        # Write the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)
        print(f"Successfully converted {parquet_file_path} to {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# Replace 'input.parquet' and 'output.csv' with your file paths
convert_parquet_to_csv('./merged_parquet/ffe51de7af.parquet', 'test.csv')