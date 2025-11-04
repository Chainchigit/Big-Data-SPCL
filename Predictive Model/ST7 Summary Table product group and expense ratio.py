# หา product group ที่ MKT สูงแต่ BP ต่ำ
grp_filtered["MKT_Ratio"] = grp_filtered["MKT_Expense"] / grp_filtered["Net_Sales"] * 100
low_bp_high_mkt = grp_filtered[(grp_filtered["MKT_Ratio"] > 10) & (grp_filtered["BP_pct"] < 0)]
display(low_bp_high_mkt[["Product Group", "MKT_Ratio", "BP_pct"]].sort_values("MKT_Ratio", ascending=False))
