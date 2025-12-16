import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Trying from Scratch", layout = "centered")

st.title("Trying")

data = pd.read_parquet("t20_bbb.parquet")

st.dataframe(data.head())

