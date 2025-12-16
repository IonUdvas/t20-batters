import streamlit as st
import pandas as pd

from helpers import load_data
from helpers import get_bg_colors

DATA_PATH = "t20_bbb.parquet"

st.set_page_config(page_title="Men's T20s: Batters' Analysis", layout="wide")

base_css = f"""
<style>
body {{ background-color: {get_bg_colors('dark')['page_bg']}; color: {get_bg_colors('dark')['text_col']}; font-family: Helvetica, Arial, sans-serif; }}
.sidebar .css-1d391kg {{ background-color: #232326 !important; border-radius: 8px; padding: 12px; }}
.main-panel-white {{ background-color: #FFFFFF !important; color: #111111 !important; }}
.custom-note {{ color: {get_bg_colors('dark')['note_col']}; font-size:15px; line-height:1.4; }}
.btn-primary {{ background-color: #00E5FF !important; color: #4a4a4a !important; }}

/* Navigation button styles */
.nav-button {{
    display: inline-block;
    padding: 12px 24px;
    margin: 4px;
    background: linear-gradient(135deg, #FFFFFF 0%, #FFE5E5 100%);
    border: 2px solid #CC0000;
    border-radius: 8px;
    color: #CC0000;
    font-weight: bold;
    font-size: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
}}

.nav-button:hover {{
    background: linear-gradient(135deg, #FFE5E5 0%, #FFCCCC 100%);
    border-color: #990000;
    color: #990000;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}}

.nav-button-active {{
    background: linear-gradient(135deg, #CC0000 0%, #990000 100%);
    color: #FFFFFF;
    border-color: #CC0000;
}}

.nav-button-active:hover {{
    background: linear-gradient(135deg, #990000 0%, #770000 100%);
    color: #FFFFFF;
}}
.svtable-wrapper {{ overflow-x:auto; }}
.svtable-wrapper table {{ width:100%; table-layout:auto; border-collapse:collapse; }}
.svtable-wrapper th, .svtable-wrapper td {{ padding:6px 8px; border:1px solid #eee; text-align:left; vertical-align:top; }}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)

st.title("Men's T20s: Batters' Analysis")

df_all = load_data()

st.dataframe(df_all.head())

