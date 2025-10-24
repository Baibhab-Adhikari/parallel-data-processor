import pandas as pd


def categorize_trip(row):
    """
    A sample Python function that runs on every row.
    This is slow because it's pure Python logic, not optimized C code.
    """
    if row['passenger_count'] > 1 and row['trip_distance'] > 5:
        return "Group - Long"
    elif row['passenger_count'] > 1:
        return "Group - Short"
    elif row['trip_distance'] > 10:
        return "Solo - Long"
    else:
        return "Solo - Short"


def process(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the slow, row-by-row logic to the DataFrame chunk.
    """
    print(f"Processing chunk with shape: {df.shape}...")

    # df.apply(..., axis=1) is the classic single-core bottleneck
    df['trip_category'] = df.apply(categorize_trip, axis=1)

    print("...chunk processing complete.")
    return df
