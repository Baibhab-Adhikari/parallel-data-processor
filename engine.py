import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd


def serial_processing(df: pd.DataFrame, process_func) -> pd.DataFrame:
    print("Starting serial DF processing...")
    start_process = time.time()
    processed_df: pd.DataFrame = process_func(df)
    end_process = time.time()
    print(f"elapsed time: {end_process-start_process:.2f}seconds")
    return processed_df


def parallel_processing(df: pd.DataFrame, process_func) -> pd.DataFrame:
    num_workers = os.cpu_count() or 1
    num_workers = min(num_workers, max(1, len(df)))
    data_chunks = np.array_split(df, num_workers)
    start_parallel_processing = time.time()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        processed_chunks = list(executor.map(process_func, data_chunks))

    processed_final_df = pd.concat(objs=processed_chunks)
    end_parallel_processing = time.time()

    print(
        f"elapsed time: {end_parallel_processing-start_parallel_processing:.2f}seconds")
    return processed_final_df
