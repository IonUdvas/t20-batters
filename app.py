import streamlit as st
import pandas as pd

from helpers import load_data
from helpers import get_bg_colors

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
def get_sorted_unique(col):
    if col in df_all.columns:
        vals = df_all[col].dropna().unique().tolist()
        vals_sorted = sorted(vals)
        return vals_sorted
    return []

batters = get_sorted_unique("bat")
bowl_kind_choices = ["All"] + get_sorted_unique("bowl_kind")
team_choices = ["All"] + get_sorted_unique("team_bowl")
country_choices = ["All"] + get_sorted_unique("country")
bowler_choices = ["All"] + get_sorted_unique("bowl")
ground_choices = ["All"] + get_sorted_unique("ground")
bowlstyle_choices = ["All"] + get_sorted_unique("bowl_style")
inns_choices = ["All"] + [str(x) for x in sorted(df_all["inns"].dropna().unique().astype(int))] if "inns" in df_all.columns else ["All"]
team_bat_choices = ["All"] + get_sorted_unique("team_bat")
tournament_choices = ["All"] + get_sorted_unique("competition")

min_date = df_all["date"].min() if "date" in df_all.columns else None
max_date = df_all["date"].max() if "date" in df_all.columns else None

min_over = 1
max_over = 20
default_over = (min_over, max_over)
min_bf = int(df_all["cur_bat_bf"].dropna().min()) if "cur_bat_bf" in df_all.columns else 1
max_bf = int(df_all["cur_bat_bf"].dropna().max()) if "cur_bat_bf" in df_all.columns else 120
default_bf = (min_bf, max_bf)

with st.sidebar:
    st.header("Filters")
    selected_batter = st.selectbox("Select Batter:", options=batters)
    selected_team_bat = st.multiselect("For Team:", options=team_bat_choices, default=["All"])
    selected_opposition = st.multiselect("Opposition:", options=team_choices, default=["All"])
    selected_bowltype = st.multiselect("Bowler Type:", options=bowl_kind_choices, default=["All"])
    selected_bowler = st.multiselect("Bowler:", options=bowler_choices, default=["All"])
    selected_tournament = st.multiselect("Tournament:", options=tournament_choices, default=["All"])
    selected_host = st.multiselect("Host Country:", options=country_choices, default=["All"])
    selected_ground = st.multiselect("Ground:", options=ground_choices, default=["All"])

    if min_date is not None and max_date is not None:
        sel_date_range = st.date_input("Select Date Range:", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    else:
        sel_date_range = None

    st.markdown("---")
    st.markdown("### Advanced filters")
    selected_bowlstyle = st.multiselect("Bowling Style:", options=bowlstyle_choices, default=["All"])
    selected_inns = st.multiselect("Innings:", options=inns_choices, default=["All"])
    balls_faced = st.slider("Balls faced:", min_bf, max_bf, value=default_bf)
    over_range = st.slider("Over range:", min_over, max_over, value=default_over)

    # add these two lines into the sidebar block (after over_range or where appropriate)
    sr_window = st.slider("SR rolling window (balls): For Inns progression", 1, 30, 10, help="Window size (in balls) used for rolling strike-rate")
    bd_window = st.slider("Boundaries/Dots window (balls): For Inns progression", 1, 12, 6, help="Window (in balls) used to compute rolling boundary/dot counts")


    run_btn = st.button("Generate")

if "run_pressed" not in st.session_state:
    st.session_state["run_pressed"] = False
if run_btn:
    st.session_state["run_pressed"] = True

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Pitchmaps"


