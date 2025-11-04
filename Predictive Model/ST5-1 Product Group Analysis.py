import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap

# ==== 1) รวมข้อมูลระดับ Product Group ====
grp = (
    df.groupby("Product Group", dropna=False)
      .agg(Net_Sales=("Net Sales","sum"),
           BP_abs=("Business Profit","sum"),
           MKT_Expense=("MKT_Expense","sum"))
      .reset_index()
)

# BP% แบบถ่วงน้ำหนักด้วยยอดขาย
grp["BP_pct"] = np.where(grp["Net_Sales"]>0, grp["BP_abs"]/grp["Net_Sales"]*100, np.nan)

# ==== 2) เลือก Top-N ====
TOP_N = 20
SORT_BY = "Net_Sales"
grp_top = grp.sort_values(SORT_BY, ascending=False).head(TOP_N).copy()

# ย่อชื่อให้สั้นลง
def short_name(s, width=25):
    try:
        return textwrap.shorten(str(s), width=width, placeholder="…")
    except:
        return str(s)[:width]
grp_top["PG_short"] = grp_top["Product Group"].apply(short_name)

# แปลงหน่วย
grp_top["Net_Sales_B"] = grp_top["Net_Sales"] / 1e9

# ==== 3) Plot แนวนอน ====
fig, ax1 = plt.subplots(figsize=(10,7))

# Bar: Net Sales (แนวนอน)
ax1.barh(grp_top["PG_short"], grp_top["Net_Sales_B"], color='skyblue')
ax1.set_xlabel("Net Sales (bn)")
ax1.set_ylabel("Product Group")
ax1.invert_yaxis()  # ให้สินค้ายอดขายสูงอยู่ด้านบน

# Line: BP% (แกนบน)
ax2 = ax1.twiny()
ax2.plot(grp_top["BP_pct"], grp_top["PG_short"], marker='o', color='tab:blue', label="BP(%)")
ax2.set_xlabel("BP(%)", color='tab:blue')
ax2.tick_params(axis='x', labelcolor='tab:blue')

# เส้นเป้าหมาย
target_value = 10
ax2.axvline(x=target_value, linestyle="--", linewidth=1, color='red')
ax2.text(target_value+0.5, len(grp_top)-1, f"Target {target_value}%", color='red', va="bottom")

plt.title(f"Top {TOP_N} Product Groups — Net Sales vs BP(%) (Sort by {SORT_BY})")
plt.grid(True, axis='x', which='major', alpha=0.4)
plt.tight_layout()
plt.show()
