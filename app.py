import streamlit as st
import pandas as pd
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Parallel Data Processor ⚙️",
    page_icon="💽",
    layout="wide"
)

# --- Main App ---
st.title("Parallel Data Processor ⚙️")

st.write("""
Upload your large dataset (CSV, Parquet, Excel, or JSON), and we'll process it 
using Python's multiprocessing to demonstrate the speed-up.
""")

# --- 1. File Uploader ---
# Added 'xlsx', 'xls', and 'json' to the allowed types
uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "parquet", "xlsx", "xls", "json"]
)

# --- 2. Load Data ---
if uploaded_file is not None:
    # Get the file extension
    # Use os.path.splitext to reliably get the extension
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    file_extension = file_extension.lower()  # ensure it's lowercase

    df = None  # Initialize df

    with st.spinner(f"Loading {uploaded_file.name}..."):
        try:
            start_load = time.time()

            # Updated logic to handle more file types
            if file_extension == ".csv":
                df = pd.read_csv(uploaded_file)
            elif file_extension == ".parquet":
                df = pd.read_parquet(uploaded_file)
            elif file_extension in [".xls", ".xlsx"]:
                # This requires the 'openpyxl' library to be installed
                df = pd.read_excel(uploaded_file)
            elif file_extension == ".json":
                df = pd.read_json(uploaded_file)

            end_load = time.time()

            if df is not None:
                st.success(
                    f"File loaded in {end_load - start_load:.2f} seconds.")

                # --- 3. Display Preview ---
                st.subheader("Data Preview (First 5 Rows):")
                st.dataframe(df.head())

                st.subheader("Data Shape:")
                st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            else:
                st.error(
                    f"Could not read file. Unsupported extension: {file_extension}")

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.warning("Note: Excel files require the 'openpyxl' library. "
                       "You can install it with: pip install openpyxl")
