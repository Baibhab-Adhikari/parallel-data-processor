import pandas as pd
import time


def convert(path: str) -> None:
    """
    Reads a large CSV file and saves it as a more efficient Parquet file.
    """
    print("Starting CSV load...")
    start_load = time.time()

    csv_df: pd.DataFrame = pd.read_csv(path)

    end_load = time.time()
    print(f"CSV loading complete in {end_load - start_load:.2f} seconds.")

    print("Starting Parquet save...")
    start_save = time.time()

    # Save the DataFrame to a Parquet file.
    csv_df.to_parquet("data/yellow_tripdata.parquet")

    end_save = time.time()
    print(f"Parquet file saved in {end_save - start_save:.2f} seconds.")


def main() -> None:
    CSV_PATH: str = "data/yellow_tripdata_2016-01.csv"
    convert(CSV_PATH)


if __name__ == '__main__':
    main()
