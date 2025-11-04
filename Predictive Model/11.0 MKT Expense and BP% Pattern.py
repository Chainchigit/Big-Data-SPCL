# คำนวณสัดส่วน (% ต่อ Net Sales)
df["MKT_Ratio"]   = (df["MKT_Expense"]   / df["Net Sales"] * 100).replace([np.inf,-np.inf], np.nan)
df["Other_Ratio"] = (df["Other_Expense"] / df["Net Sales"] * 100).replace([np.inf,-np.inf], np.nan)

# ==== 1) สร้าง X, y (ให้มี MKT_Ratio แน่ๆ) ====
base_feats = ["Sales Volume","Sales Unit Price","COGS unit cost","MKT_Ratio","Other_Ratio"]
base_feats = [c for c in base_feats if c in df.columns]
assert "MKT_Ratio" in base_feats, "ยังไม่มี MKT_Ratio ใน df — เช็กชื่อคอลัมน์"

X = df[base_feats].copy()

# seasonality (ถ้ามี Month_num)
if "Month_num" in df.columns:
    X = X.join(pd.get_dummies(df["Month_num"], prefix="m", drop_first=True))

# ล้างข้อมูล และจัด y ให้ตรง index
X = X.replace([np.inf,-np.inf], np.nan).dropna()
y = df.loc[X.index, "BP(%)"]

# ==== 2) ฝึกโมเดล (Ridge + TimeSeries CV) ====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

tscv = TimeSeriesSplit(n_splits=5)
model = RidgeCV(alphas=np.logspace(-3,3,20))
for tr, te in tscv.split(X_scaled):
    model.fit(X_scaled[tr], y.iloc[tr])          # fit หลายสปลิต; ตัวสุดท้ายคือโมเดลที่ใช้ต่อ

# ==== 3) helper predict + baseline ====
def _predict_with(model, scaler, X_like_X, X_columns):
    X_like_X = X_like_X[X_columns]               # คงลำดับ/คอลัมน์เดิม
    return model.predict(scaler.transform(X_like_X))

y_pred_base = _predict_with(model, scaler, X, X.columns)

# ==== 4) SIMULATE: ลด MKT_Ratio 5–30% ====
levels = [0.95, 0.90, 0.85, 0.80, 0.70]  # ลด 5,10,15,20,30%
rows = []
for lv in levels:
    X_lv = X.copy()
    X_lv["MKT_Ratio"] = (X_lv["MKT_Ratio"] * lv).clip(lower=0)
    y_pred_lv = _predict_with(model, scaler, X_lv, X.columns)
    rows.append({
        "Reduce %": int((1-lv)*100),
        "Avg BP Uplift (pts)": float((y_pred_lv - y_pred_base).mean()),
        "Median BP Uplift (pts)": float(np.median(y_pred_lv - y_pred_base)),
    })

uplift_curve = pd.DataFrame(rows)
display(uplift_curve)

# ==== 5) กราฟ ====
plt.figure(figsize=(6,4))
plt.plot(uplift_curve["Reduce %"], uplift_curve["Avg BP Uplift (pts)"], marker="o")
plt.title("BP Uplift vs % Reduction in MKT_Ratio")
plt.xlabel("% reduction in MKT_Ratio"); plt.ylabel("Avg BP uplift (pts)")
plt.grid(True, alpha=.4)
plt.show()
