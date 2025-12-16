def build_filtered_df():
    df = df_all.copy()
    if selected_batter is None:
        return pd.DataFrame()
    df = df[df["bat"].astype(str) == str(selected_batter)]

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
            ints = [int(x) for x in selected_inns if x != "All"]
            if len(ints) > 0:
                df = df[df["inns"].isin(ints)]
        except Exception:
            pass

    if "over" in df.columns:
        df = df[(pd.to_numeric(df["over"], errors="coerce") >= over_range[0]) &
                (pd.to_numeric(df["over"], errors="coerce") <= over_range[1])]
    if "cur_bat_bf" in df.columns:
        df = df[(pd.to_numeric(df["cur_bat_bf"], errors="coerce") >= balls_faced[0]) &
                (pd.to_numeric(df["cur_bat_bf"], errors="coerce") <= balls_faced[1])]

    if sel_date_range is not None and "date" in df.columns:
        try:
            start_d, end_d = sel_date_range
            df = df[(df["date"] >= start_d) & (df["date"] <= end_d)]
        except Exception:
            pass

    return df