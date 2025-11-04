# ==== ตั้งค่าเกณฑ์กลุ่ม (แก้ได้) ====
LOW_MKT_MAX = 12        # %  -> ต่ำกว่าเท่านี้ถือว่า MKT ต่ำ
MID_MKT_MAX = 20        # %  -> <= เท่านี้ถือว่า MKT ปานกลาง (ระหว่าง LOW_MKT_MAX..MID_MKT_MAX)
HIGH_BP_MIN = 10        # %  -> BP สูง ถ้า > ค่านี้
NEAR_ZERO_BP = 5        # %  -> BP ใกล้ศูนย์ คือ -NEAR_ZERO_BP..+NEAR_ZERO_BP

# ==== กรอง outlier เหมือนเดิม ====
grp_filtered = grp[(grp["Net_Sales"] > 0) & (grp["MKT_Expense"]/grp["Net_Sales"]*100 < 200)].copy()
x = grp_filtered["MKT_Expense"] / grp_filtered["Net_Sales"] * 100
y = grp_filtered["BP_pct"]

# ==== จัดกลุ่ม + สี ====
labels = []
colors = []

for mkt_ratio, bp in zip(x, y):
    if (mkt_ratio < LOW_MKT_MAX) and (bp > HIGH_BP_MIN):
        # 🟢 กลุ่มซ้าย: MKT ต่ำ, BP สูง
        labels.append("Low MKT, High BP")
        colors.append("#2ecc71")   # green
    elif (LOW_MKT_MAX <= mkt_ratio <= MID_MKT_MAX) and (abs(bp) <= NEAR_ZERO_BP):
        # 🟠 กลุ่มกลาง: MKT ปานกลาง, BP ใกล้ศูนย์
        labels.append("Mid MKT, BP≈0")
        colors.append("#f39c12")   # orange
    elif (mkt_ratio > MID_MKT_MAX) and (bp < 0):
        # 🔴 กลุ่มขวา: MKT สูง, BP ติดลบ
        labels.append("High MKT, Negative BP")
        colors.append("#e74c3c")   # red
    else:
        # จุดที่ไม่เข้า 3 เงื่อนไขหลัก — ใส่เป็นสีเทา
        labels.append("Others")
        colors.append("#95a5a6")   # gray

grp_filtered = grp_filtered.assign(
    MKT_ratio_pct = x.values,
    BP_pct_val    = y.values,
    seg_label     = labels,
    seg_color     = colors
)

# ==== วาดกราฟ ====
import matplotlib.pyplot as plt
plt.figure(figsize=(7,5))

# วาดทีละกลุ่มเพื่อให้ legend สวย
for lab, sub in grp_filtered.groupby("seg_label"):
    plt.scatter(sub["MKT_ratio_pct"], sub["BP_pct_val"], s=30,
                c=sub["seg_color"], label=lab, edgecolors="none")

plt.axhline(0, linestyle="--", color="gray")
plt.axvline(x.median(), linestyle=":", color="gray")
plt.xlabel("MKT Expense / Net Sales (%)")
plt.ylabel("BP(%)")
plt.title("Product Groups — MKT Ratio vs BP(%) (Trimmed <200%)")
plt.grid(True)
plt.legend(title="Segments", loc="best")
plt.tight_layout()
plt.show()
