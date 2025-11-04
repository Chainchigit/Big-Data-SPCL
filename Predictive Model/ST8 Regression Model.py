from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

# ฟีเจอร์ที่ "ตัดสินใจได้ก่อนหน้า" และไม่ใช่นิยามตรงของ BP%
feats = [
    "Sales Volume", "Sales Unit Price", "COGS unit cost",
    "MKT_Ratio", "Other_Ratio"  # สัดส่วนค่าใช้จ่ายที่เราคุมได้
]
feats = [c for c in feats if c in df.columns]
X = df[feats].replace([np.inf,-np.inf], np.nan).dropna()
y = df.loc[X.index, "BP(%)"]

# สร้าง seasonality
if "Month_num" in df.columns:
    X = X.join(pd.get_dummies(df.loc[X.index, "Month_num"], prefix="m", drop_first=True))

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ใช้ TimeSeriesSplit กันข้อมูลไหลย้อนอดีต
tscv = TimeSeriesSplit(n_splits=5)
model = RidgeCV(alphas=np.logspace(-3,3,20))
scores = []
for tr, te in tscv.split(X_scaled):
    model.fit(X_scaled[tr], y.iloc[tr])
    scores.append(model.score(X_scaled[te], y.iloc[te]))
print("R² (TimeSeries CV):", np.round(scores,3), " | mean:", np.mean(scores).round(3))

# ค่าสัมประสิทธิ์ (บนสเกล standardized → เปรียบเทียบอิทธิพลได้)
coef = pd.Series(model.coef_, index=X.columns).sort_values()
print(coef)
