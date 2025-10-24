import pandas as pd

from engine import parallel_processing, serial_processing
from user_task import process


def main() -> None:
    path: str = "data/yellow_tripdata.parquet"
    df: pd.DataFrame = pd.read_parquet(path)

    print("Serial execution:")
    serial_processing(df, process_func=process)
    print("-"*50)
    print("Parallel execution")
    parallel_processing(df, process_func=process)


if __name__ == '__main__':
    main()
