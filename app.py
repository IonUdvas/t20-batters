import streamlit as st
import pandas as pd

from helpers import (
    load_data,
    get_bg_colors,
)

from data_helpers import (
    get_sorted_unique,
    build_filtered_df,
)

DATA_PATH = "t20_bbb.parquet"

# -------------------------
# STREAMLIT UI
# -------------------------
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
if df_all.shape[0] == 0:
    st.error(f"Could not find data at '{DATA_PATH}'. Place your CSV there.")
    st.stop()



# -------------------------
# Sidebar filters setup
# -------------------------
batters = get_sorted_unique(df_all, "bat")
team_bat_choices = ["All"] + get_sorted_unique(df_all, "team_bat")
team_choices = ["All"] + get_sorted_unique(df_all, "team_bowl")
bowl_kind_choices = ["All"] + get_sorted_unique(df_all, "bowl_kind")
bowler_choices = ["All"] + get_sorted_unique(df_all, "bowl")
ground_choices = ["All"] + get_sorted_unique(df_all, "ground")
bowlstyle_choices = ["All"] + get_sorted_unique(df_all, "bowl_style")
country_choices = ["All"] + get_sorted_unique(df_all, "country")
tournament_choices = ["All"] + get_sorted_unique(df_all, "competition")
inns_choices = ["All"] + [str(x) for x in sorted(df_all["inns"].dropna().astype(int).unique())]

min_date, max_date = df_all["date"].min(), df_all["date"].max()
min_bf, max_bf = int(df_all["cur_bat_bf"].min()), int(df_all["cur_bat_bf"].max())

with st.sidebar:
    st.header("Filters")

    selected_batter = st.selectbox("Select Batter", batters)
    selected_team_bat = st.multiselect("For Team", team_bat_choices, ["All"])
    selected_opposition = st.multiselect("Opposition", team_choices, ["All"])
    selected_bowltype = st.multiselect("Bowler Type", bowl_kind_choices, ["All"])
    selected_bowler = st.multiselect("Bowler", bowler_choices, ["All"])
    selected_tournament = st.multiselect("Tournament", tournament_choices, ["All"])
    selected_host = st.multiselect("Host Country", country_choices, ["All"])
    selected_ground = st.multiselect("Ground", ground_choices, ["All"])

    sel_date_range = st.date_input(
        "Date Range", (min_date, max_date), min_value=min_date, max_value=max_date
    )

    st.markdown("### Advanced filters")

    selected_bowlstyle = st.multiselect("Bowling Style", bowlstyle_choices, ["All"])
    selected_inns = st.multiselect("Innings", inns_choices, ["All"])
    balls_faced = st.slider("Balls faced", min_bf, max_bf, (min_bf, max_bf))
    over_range = st.slider("Over range", 1, 20, (1, 20))

    sr_window = st.slider("SR rolling window (balls)", 1, 30, 10)
    bd_window = st.slider("Boundaries/Dots window (balls)", 1, 12, 6)

    run_btn = st.button("Generate")

if run_btn:
    df_filtered = build_filtered_df(
        df_all,
        selected_batter,
        selected_team_bat,
        selected_bowltype,
        selected_opposition,
        selected_host,
        selected_bowler,
        selected_ground,
        selected_bowlstyle,
        selected_tournament,
        selected_inns,
        over_range,
        balls_faced,
        sel_date_range,
    )


