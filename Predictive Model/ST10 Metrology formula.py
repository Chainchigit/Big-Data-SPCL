# ===== แสดง “สมการที่ได้” จาก ElasticNet =====
import numpy as np
import pandas as pd

def show_elasticnet_equation(pipeline, feature_names):
    """
    แปลงค่าสัมประสิทธิ์จากสเกล standardized กลับเป็นสเกลเดิมของข้อมูล
    และพิมพ์สมการในรูป y = b0 + b1*x1 + ...
    """
    if not hasattr(pipeline, "named_steps") or "mdl" not in pipeline.named_steps:
        print("ไม่พบโมเดล ElasticNet ใน pipeline")
        return

    scaler = pipeline.named_steps.get("scaler", None)
    mdl    = pipeline.named_steps["mdl"]

    if scaler is None:
        # ไม่ได้ใช้ StandardScaler ใน pipeline
        coefs_orig = pd.Series(mdl.coef_, index=feature_names)
        intercept_orig = mdl.intercept_
    else:
        # ใช้ StandardScaler → ต้องแปลงกลับสเกลเดิม
        means  = scaler.mean_
        scales = scaler.scale_

        beta_scaled = np.asarray(mdl.coef_)
        beta_orig   = beta_scaled / scales
        intercept_orig = mdl.intercept_ - np.sum(beta_scaled * (means / scales))

        coefs_orig = pd.Series(beta_orig, index=feature_names)

    # เรียงลำดับตามอิทธิพล (ค่าสัมบูรณ์)
    coefs_sorted = coefs_orig.reindex(coefs_orig.abs().sort_values(ascending=False).index)

    print("\n=== สมการเชิงเส้น (ElasticNet) บนสเกลเดิม ===")
    print(f"Intercept (b0) = {intercept_orig:,.6f}")
    for name, val in coefs_sorted.items():
        print(f"{name:>30s} : {val:,.6f}")

    # (ทางเลือก) สร้างสมการสั้น ๆ เฉพาะ top-k ตัวแปร
    k = 8
    parts = [f"{intercept_orig:,.4f}"]
    for name, val in coefs_sorted.head(k).items():
        sign = "+" if val >= 0 else "-"
        parts.append(f" {sign} {abs(val):,.4f}*{name}")
    eqn = "BP_hat = " + "".join(parts)
    print("\nสมการย่อ (top {} ตัวแปร):\n{}".format(k, eqn))

# เรียกใช้ (สมมติใช้ ElasticNet เป็นโมเดลที่ดีที่สุด)
feature_names = list(X_train.columns)
show_elasticnet_equation(enet, feature_names)
