import streamlit as st
import pandas as pd

from helpers import load_data
# from helpers import get_bg_colors

DATA_PATH = "t20_bbb.parquet"

st.set_page_config(page_title="Men's T20s: Batters' Analysis", layout="wide")

st.title("Men's T20s: Batters' Analysis")

df_all = load_data()

st.dataframe(df_all.head())

