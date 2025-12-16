import streamlit as st
import time
import pandas as pd
import numpy as np

DATA_PATH = "t20_bbb.parquet"

@st.cache_data(show_spinner="Loading 1M+ T20 deliveries... (first load may take some while)")
def load_data(path=DATA_PATH):
    for attempt in range(3):
        try:
            with st.spinner(f"Downloading full dataset... (attempt {attempt+1}/3)"):
                df = pd.read_parquet(path)
            st.success(f"Loaded {len(df):,} deliveries!")
            df.columns = [c.strip() for c in df.columns]
            for c in df.select_dtypes(include=["object"]).columns:
                df[c] = df[c].replace("", np.nan)
            if "date" in df.columns:
                try:
                    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
                except:
                    pass
            return df
        except Exception as e:
            st.warning(f"Attempt {attempt+1} failed: {str(e)[:100]}")
            time.sleep(5)
    st.error("Could not load data after 3 attempts. Running with empty dataset.")
    return pd.DataFrame()