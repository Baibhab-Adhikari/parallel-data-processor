import json
import os

import pandas as pd

from engine import parallel_processing, serial_processing
from user_task import process


def main() -> None:
    """
    This is now your main "benchmark runner" script.
    Run this from your terminal to perform the heavy processing
    and save the results to a JSON file.
    """

    # --- 1. Load Data ---
    print("Loading benchmark data...")
    path: str = "data/yellow_tripdata.parquet"
    df: pd.DataFrame = pd.read_parquet(path)
    print(f"Data loaded: {df.shape[0]} rows.")

    # --- 2. Run Serial ---
    print("\n--- Starting Serial execution ---")
    # We now capture the returned DataFrame and time
    serial_df, serial_time = serial_processing(df, process_func=process)

    # --- 3. Run Parallel ---
    print("\n--- Starting Parallel execution ---")
    # We now capture the returned DataFrame and time
    parallel_df, parallel_time = parallel_processing(df, process_func=process)

    # --- 4. Calculate and Save Results ---
    print("\n--- Saving benchmark results to JSON ---")

    cores = os.cpu_count() or 1
    speedup = 0.0
    if parallel_time > 0:
        speedup = serial_time / parallel_time

    results = {
        "serial_time": serial_time,
        "parallel_time": parallel_time,
        "speedup": speedup,
        "cores": cores,
        "rows": int(df.shape[0]),
        "data_size_mb": round(os.path.getsize(path) / (1024*1024), 1)
    }

    # Save the results dictionary to a file
    results_path = "data/benchmark_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {results_path}")
    print("Benchmark complete. You can now run 'streamlit run app.py'.")


if __name__ == '__main__':
    # This __name__ check is critical for multiprocessing to work safely!
    main()
