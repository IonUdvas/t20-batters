import pandas as pd
import numpy as np

def get_sorted_unique(df, col):
    if col in df.columns:
        return sorted(df[col].dropna().unique().tolist())
    return []


def apply_multifilter(df, col, selected):
    if col not in df.columns or not selected or "All" in selected:
        return df
    return df[df[col].isin(selected)]


def build_filtered_df(
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
):
    if selected_batter is None:
        return pd.DataFrame()

    df = df_all[df_all["bat"].astype(str) == str(selected_batter)].copy()

    df = apply_multifilter(df, "team_bat", selected_team_bat)
    df = apply_multifilter(df, "bowl_kind", selected_bowltype)
    df = apply_multifilter(df, "team_bowl", selected_opposition)
    df = apply_multifilter(df, "country", selected_host)
    df = apply_multifilter(df, "bowl", selected_bowler)
    df = apply_multifilter(df, "ground", selected_ground)
    df = apply_multifilter(df, "bowl_style", selected_bowlstyle)
    df = apply_multifilter(df, "competition", selected_tournament)

    if selected_inns and "All" not in selected_inns and "inns" in df.columns:
        try:
            df = df[df["inns"].isin([int(x) for x in selected_inns])]
        except Exception:
            pass

    if "over" in df.columns:
        df = df[
            df["over"].between(over_range[0], over_range[1], inclusive="both")
        ]

    if "cur_bat_bf" in df.columns:
        df = df[
            df["cur_bat_bf"].between(balls_faced[0], balls_faced[1], inclusive="both")
        ]

    if sel_date_range and "date" in df.columns:
        try:
            start_d, end_d = sel_date_range
            df = df[(df["date"] >= start_d) & (df["date"] <= end_d)]
        except Exception:
            pass

    return df