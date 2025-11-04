# ===== 0) Imports
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score

# ===== 1) ตั้งคอลัมน์พื้นฐานที่คาดว่าจะมี
COL_VOL   = "Sales Volume"
COL_PRICE = "Sales Unit Price"
COL_COGS  = "COGS unit cost"
COL_MKT   = "MKT_Ratio"
COL_OTH   = "Other_Ratio"
COL_BP    = "BP(%)"         # target
COL_MNUM  = "Month_num"     # 1..12 (ถ้ามี)

# ===== 2) เลือกเฉพาะคอลัมน์ที่มีจริง
have = [c for c in [COL_VOL,COL_PRICE,COL_COGS,COL_MKT,COL_OTH,COL_BP,COL_MNUM] if c in df.columns]
data = df[have].copy().replace([np.inf,-np.inf], np.nan)

# ===== 3) ฟีเจอร์เชิงธุรกิจ
# spread (ส่วนต่างราคา-ต้นทุน) + margin ratio (ถ้าคูณเสถียร)
if COL_PRICE in data and COL_COGS in data:
    data["price_cost_spread"] = data[COL_PRICE] - data[COL_COGS]
    data["price_cost_ratio"]  = np.where(data[COL_COGS]!=0, data[COL_PRICE]/data[COL_COGS], np.nan)

# interaction เชิงพฤติกรรม
if set([COL_VOL,COL_PRICE]).issubset(data.columns):
    data["vol_x_price"] = data[COL_VOL] * data[COL_PRICE]
if set([COL_VOL,COL_MKT]).issubset(data.columns):
    data["vol_x_mkt"]   = data[COL_VOL] * data[COL_MKT]

# seasonality (ต่อเนื่องกว่า one-hot)
if COL_MNUM in data:
    m = data[COL_MNUM].astype(float)
    data["month_sin"] = np.sin(2*np.pi*m/12)
    data["month_cos"] = np.cos(2*np.pi*m/12)

# ===== 4) สร้าง lag & rolling ให้ฟีเจอร์หลัก + target lag/MA
def add_lag_ma(df_in, cols, lags=[1], mas=[3]):
    out = df_in.copy()
    for c in cols:
        if c in df_in:
            for L in lags:
                out[f"{c}_lag{L}"] = df_in[c].shift(L)
            for W in mas:
                out[f"{c}_ma{W}"]  = df_in[c].shift(1).rolling(W, min_periods=1).mean()
    return out

key_feats = [c for c in [COL_VOL,COL_PRICE,COL_COGS,COL_MKT,COL_OTH,"price_cost_spread","price_cost_ratio","vol_x_price","vol_x_mkt","month_sin","month_cos"] if c in data.columns]
data = add_lag_ma(data, key_feats, lags=[1], mas=[3])

# target smoothing (ลด noise) + target lag ให้ใช้ค่าจริงเดือนก่อนช่วยพยากรณ์
if COL_BP in data:
    data["BP_ma3"]   = data[COL_BP].rolling(3, min_periods=1).mean()
    data["BP_lag1"]  = data[COL_BP].shift(1)

# ===== 5) เตรียม X,y และกำจัด NaN ที่เกิดจากการ shift
# y ใช้ BP_ma3 เพื่อความนิ่ง (ยังสามารถเปลี่ยนกลับเป็น BP% ได้)
data_clean = data.dropna(axis=0)
y = data_clean["BP_ma3"] if "BP_ma3" in data_clean else data_clean[COL_BP]

# ฟีเจอร์ทั้งหมด = ทุกอย่างยกเว้นคอลัมน์ target ต้นฉบับ
drop_cols = [COL_BP, "BP_ma3"] if "BP_ma3" in data_clean else [COL_BP]
X = data_clean.drop(columns=[c for c in drop_cols if c in data_clean])

# ===== 6) แยก train/test ตาม "เวลา" (ถือ 20% สุดท้ายเป็น holdout)
N = len(X)
split = int(N*0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# ===== 7) โมเดล 1: ElasticNetCV (จับความเชิงเส้น + เลือกฟีเจอร์บางส่วนอัตโนมัติ)
enet = Pipeline([
    ("scaler", StandardScaler()),
    ("mdl", ElasticNetCV(l1_ratio=[.1,.3,.5,.7,.9,.95,1.0], alphas=np.logspace(-3,2,30),
                         max_iter=5000, cv=5, n_jobs=-1))
])
enet.fit(X_train, y_train)
pred_enet = enet.predict(X_test)
r2_enet   = r2_score(y_test, pred_enet)

# ===== 8) โมเดล 2: GradientBoosting (ไม่เชิงเส้น/จับ interaction อัตโนมัติ)
gbr = GradientBoostingRegressor(
    n_estimators=800, learning_rate=0.03, max_depth=3,
    subsample=0.9, random_state=42
)
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

# เทรน/พยากรณ์ GradientBoosting
gbr.fit(X_train, y_train)
pred_gbr = gbr.predict(X_test)

def report(y_true, y_pred, name):
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f"[{name}] R²={r2:.3f} | MAE={mae:.3f} | RMSE={rmse:.3f}")
    return r2

print("=== Holdout metrics ===")
r2_e = report(y_test, pred_enet, "ElasticNet")
r2_g = report(y_test, pred_gbr,  "GradientBoosting")

best_name, best_pred = ("GradientBoosting", pred_gbr) if r2_g > r2_e else ("ElasticNet", pred_enet)
print(f">>> ใช้โมเดลที่ดีที่สุด: {best_name}")

