import os
import time
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Tuple

import numpy as np
import pandas as pd


def serial_processing(df: pd.DataFrame, process_func: Callable) -> Tuple[pd.DataFrame, float]:
    """
    Runs the processing function on a single core and returns the
    processed DataFrame and the elapsed time.
    """
    print("Starting serial DF processing...")
    start_process = time.time()

    processed_df: pd.DataFrame = process_func(df)

    end_process = time.time()
    elapsed_time = end_process - start_process

    print(f"Serial elapsed time: {elapsed_time:.2f}seconds")
    # Return both the result and the time
    return processed_df, elapsed_time


def parallel_processing(df: pd.DataFrame, process_func: Callable) -> Tuple[pd.DataFrame, float]:
    """
    Runs the processing function in parallel across all cores and returns
    the processed DataFrame and the elapsed time.
    """
    print("Starting parallel DF processing...")

    # get worker process count (fallback to 1 if os.cpu_count() returns None)
    num_workers = os.cpu_count() or 1
    # Ensure we don't try to use more workers than we have rows
    num_workers = min(num_workers, max(1, len(df)))
    print(
        f"Splitting data into {num_workers} chunks for parallel processing...")

    data_chunks = np.array_split(df, num_workers)

    start_parallel_processing = time.time()

    # but the ProcessPoolExecutor is safe to be called from this function.
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # This will run the 'process' function on each chunk in parallel
        processed_chunks = list(executor.map(process_func, data_chunks))

    # Merge the processed chunks back into one DataFrame
    processed_final_df = pd.concat(objs=processed_chunks)

    end_parallel_processing = time.time()
    elapsed_time = end_parallel_processing - start_parallel_processing

    print(f"Parallel elapsed time: {elapsed_time:.2f}seconds")
    # Return both the result and the time
    return processed_final_df, elapsed_time
