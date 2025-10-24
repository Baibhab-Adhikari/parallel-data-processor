# Parallel Processor Benchmark 📊

This project is an interactive Streamlit dashboard that benchmarks the performance of a CPU-bound data processing task when run on a single core (serially) versus on all available CPU cores (in parallel).

The core of the project is a decoupled processing engine that uses Python's multiprocessing library to dramatically speed up slow, row-by-row pandas operations.

## 🚀 Project Goal & "Why"

In data science, it's common to have a large DataFrame (millions of rows) and need to apply a complex, custom Python function to every single row. The standard way to do this, `df.apply(..., axis=1)`, is notoriously slow because it's single-threaded and can't take advantage of modern multi-core CPUs.

This project was built to move beyond the theory of multiprocessing and provide a hands-on, practical demonstration of:

- **Identifying a Bottleneck**: We use a df.apply() task that takes over 70 seconds to run serially.
- **Implementing a Solution**: We build a generic processing "engine" using `concurrent.futures.ProcessPoolExecutor` to split the DataFrame into chunks and process them simultaneously on all available CPU cores.
- **Measuring the Gains**: The dashboard clearly visualizes the speed-up (e.g., 71.7s vs. 40.6s), proving the concept.
- **Understanding "Parallel Overhead"**: The speed-up isn't a perfect 8x on an 8-core machine. This project highlights the real-world costs of serialization (pickling), inter-process communication (IPC), and result merging (`pd.concat`) that are crucial to understanding parallel systems.
- **Stable Architecture**: The app is built with a decoupled "factory" and "dashboard" model. The heavy-lifting (main.py) and the visualization (app.py) are separate processes that communicate via a JSON file. This is a robust, production-safe pattern that prevents the Streamlit server from being overloaded or crashed by the multiprocessing calls.

## ✨ Key Features

- **Decoupled Engine**: The engine.py file contains clean, reusable functions for serial_processing and parallel_processing.
- **Benchmark Runner**: main.py is the "factory." It runs the benchmark and saves the results to benchmark_results.json.
- **Safe Dashboard**: app.py is the "viewer." It is a 100% safe Streamlit app that never runs the heavy task, only reads the JSON results and visualizes them.
- **Dynamic EDA**: The dashboard performs a full Exploratory Data Analysis on the benchmark dataset, including numeric/categorical stats and a missing value analysis.
- **Interactive Visualization**: Uses Plotly to create a clean, interactive bar chart of the performance comparison.

## 💻 Tech Stack

- **Core**: Python 3.9+
- **Data Processing**: pandas, numpy
- **Parallelism**: multiprocessing (via concurrent.futures)
- **Dashboard**: streamlit
- **Visualization**: plotly
- **File I/O**: pyarrow (for Parquet), openpyxl (for Excel)

## 🔧 How to Benchmark Your Own Dataset

This project is built as a template. You can easily benchmark your own data and processing tasks.

### 1. Place Your Data

Add your dataset (e.g., `my_data.parquet` or `my_data.csv`) to the `data/` folder.

### 2. Define Your Task

Open `user_task.py`. This file contains a single `process(df)` function.

Modify this function to perform your slow, CPU-bound task. The only requirement is that the function must accept a DataFrame and return a DataFrame.

```python
# In user_task.py
import pandas as pd

def process(df: pd.DataFrame) -> pd.DataFrame:
    """
    REPLACE THIS with your own slow, CPU-bound task.
    e.g., a complex df.apply(), a slow string operation, etc.
    """
    
    def my_slow_function(row):
        # Your custom logic here
        return row['col_a'] * 100 + row['col_b']

    df['new_column'] = df.apply(my_slow_function, axis=1)
    return df
```

### 3. Update the Benchmark Runner

Open `main.py` and change the `DATA_PATH` variable to point to your new file.

```python
# In main.py
...
def main() -> None:
    # Point this to your dataset
    DATA_PATH = "data/my_data.parquet" 
    
    # You may also need to change the read function if using CSV
    df: pd.DataFrame = pd.read_parquet(DATA_PATH)
    ...
```

### 4. Run the Benchmark

From your terminal, run the "factory" script. This will do all the heavy lifting and can take several minutes.

```bash
python main.py
```

This will generate a new `benchmark_results.json` file based on your data and your task.

### 5. View Your Results

Now, run the dashboard to see your custom results.

```bash
streamlit run app.py
```

The dashboard will automatically load your new JSON file and display your benchmark, speed-up, and EDA.

## 🛠️ Setup & Installation

Clone the repository:

```bash
git clone https://github.com/your-username/parallel-data-processor.git
cd parallel-data-processor
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the initial benchmark:
(This will use the default NYC Taxi dataset)

```bash
python main.py
```

Run the Streamlit app:

```bash
streamlit run app.py
```
