import streamlit as st
import pandas as pd
import time
import os
import json
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Parallel Dataset Processing Benchmark ",
    page_icon="📊",
    layout="wide"
)

# --- Main App ---
st.title("Parallel Processor Benchmark 📊")

DATA_PATH = "data/yellow_tripdata.parquet"
RESULTS_PATH = "data/benchmark_results.json"

st.write(f"""
This app displays the benchmark results of a parallel processing engine.
The benchmark runs a slow, CPU-heavy task (`df.apply`) on a large dataset
serially (1 core) vs. in parallel (all cores).
""")

# --- New Workflow Box ---
st.info("""
**To run the benchmark:**
1.  Stop this server.
2.  Run **`python main.py`** in your terminal. This does the heavy lifting.
3.  Run **`streamlit run app.py`** to view the results here.
""")

# --- 1. Load and Display Benchmark Results ---
st.header("Benchmark Results")

try:
    # Load the results from the JSON file created by main.py
    with open(RESULTS_PATH, "r") as f:
        results = json.load(f)

    serial_time = results.get("serial_time", 0)
    parallel_time = results.get("parallel_time", 0)
    speedup = results.get("speedup", 0)
    cores = results.get("cores", "N/A")
    rows = results.get("rows", 0)
    data_size_mb = results.get("data_size_mb", 0)

    st.write(
        f"Results from processing **{rows:,} rows** on a **{data_size_mb} MB** dataset:")

    # Use columns for a side-by-side comparison
    col1, col2, col3 = st.columns(3)
    col1.metric("Serial Time (1 Core)", f"{serial_time:.2f} s")
    col2.metric(f"Parallel Time ({cores} Cores)", f"{parallel_time:.2f} s")
    col3.metric("Speed-up", f"{speedup:.2f}x")

    # --- Plotly Chart Section ---
    st.subheader("Performance Comparison")

    # Create the bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Serial (1 Core)', f'Parallel ({cores} Cores)'],
        y=[serial_time, parallel_time],
        text=[f'{serial_time:.2f}s', f'{parallel_time:.2f}s'],
        textposition='auto',
        marker_color=['#EF553B', '#636EFA']
    ))

    fig.update_layout(
        title=f'Serial vs. Parallel Processing Time ({rows:,} Rows)',
        yaxis_title='Processing Time (seconds)',
        xaxis_title='Processing Method',
        # Use Streamlit's built-in theme for a consistent look
        template="streamlit",
        font=dict(family="Arial, sans-serif", size=14)
    )

    # Use st.plotly_chart to display the figure
    st.plotly_chart(fig, use_container_width=True)


except FileNotFoundError:
    st.error(f"{RESULTS_PATH} not found!")
    st.warning(
        "Please run **`python main.py`** from your terminal to generate the benchmark results file.")
except Exception as e:
    st.error(f"An error occurred while reading results: {e}")

st.divider()

# --- 2. Load and Display EDA (This is safe) ---
st.header("Exploratory Data Analysis (EDA)")
st.write("A quick analysis of the benchmark dataset.")

# Initialize variables to satisfy type checker
df = None
start_load: float = 0.0
end_load: float = 0.0

with st.spinner(f"Loading benchmark dataset ({DATA_PATH}) for EDA..."):
    try:
        start_load = time.time()
        df = pd.read_parquet(DATA_PATH)

        # --- FIX for PyArrow Error (from previous step) ---
        if 'tpep_pickup_datetime' in df.columns:
            df['tpep_pickup_datetime'] = pd.to_datetime(
                df['tpep_pickup_datetime'])
        if 'tpep_dropoff_datetime' in df.columns:
            df['tpep_dropoff_datetime'] = pd.to_datetime(
                df['tpep_dropoff_datetime'])

        end_load = time.time()
        st.success(f"EDA data loaded in {end_load - start_load:.2f} seconds.")

    except Exception as e:
        st.error(f"Error loading file for EDA: {e}")
        # Use st.stop() to halt execution if the main data file can't be loaded
        st.stop()

# --- 3. Display Data (IF loading was successful) ---
if df is not None:
    st.subheader("Data Preview (First 5 Rows):")
    st.dataframe(df.head())

    st.subheader("Data Shape:")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Use tabs to keep the UI clean
    tab1, tab2, tab3 = st.tabs(
        ["Numeric Statistics", "Categorical Statistics", "Missing Values"])

    with tab1:
        st.write("Descriptive statistics for all numeric columns:")
        st.dataframe(df.describe())

    with tab2:
        st.write("Descriptive statistics for all categorical (object) columns:")
        try:
            # include 'object' and 'category' for text-based columns
            st.dataframe(df.describe(include=['object', 'category']))
        except Exception as e:
            st.warning(
                "Could not generate categorical stats. All columns might be numeric.")

    with tab3:
        st.write(
            "Count of missing values per column (only showing columns with missing data):")
        missing_values = df.isnull().sum().reset_index().rename(
            columns={'index': 'Column', 0: 'Null Count'})
        missing_values = missing_values[missing_values['Null Count'] > 0]
        if missing_values.empty:
            st.success("No missing values found!")
        else:
            st.dataframe(missing_values)
