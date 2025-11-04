import re
import numpy as np
import pandas as pd

# 1) ตัวช่วยแปลง string -> number (รองรับ %, , และวงเล็บแปลว่าเลขติดลบ)
def to_number(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, str):
        s = x.strip()
        neg = False
        # วงเล็บ = ติดลบ
        if "(" in s and ")" in s:
            neg = True
            s = s.replace("(", "").replace(")", "")
        # ลบคอมมาและ %
        s = s.replace(",", "").replace("%", "").strip()
        # ถ้าบางทีมีตัวอักษรคั่น ให้ดึงเฉพาะส่วนที่เป็นตัวเลข/จุด/ลบ
        s = re.findall(r"-?\d+\.?\d*", s)
        if not s:
            return np.nan
        val = float(s[0])
        if neg:
            val = -val
        return val
    # ถ้าเป็นเลขอยู่แล้ว
    try:
        return float(x)
    except:
        return np.nan

# 2) ระบุคอลัมน์ที่ควรเป็นตัวเลข (มีแต่ชื่อหลัก ๆ ที่พบใน header ของคุณ)
num_like_cols = [
    "Sales Volume","Sales Unit Price","Sales","Sales Rebate","Net Sales",
    "Commission Received","Service Income","Total  Revenue","V-cost","Cost of Service",
    "COGS Sales Rebate","COGS - Excise Tax","Marginal Profit","MP(%)","F-cost","COGS",
    "COGS unit cost","Gross Profit","GP(%)","Sales Expense","Advertising","Sales Campaign",
    "Market Research Expense","Transportation","Damage","Royalty","Commission",
    "Other Marketing Expense","Personnel Cost (sales)","Depreciation (sales)","GA-Others (sales)",
    "R&D Expense","R & D","Lab Expenses","Personnel Cost (R&D)","Depreciation (R&D)",
    "GA-Others (R&D)","G&A Expense","Personnel Cost (other)","Depreciation (other)",
    "GA-Others (other)","Total Sales, R&D, G&A Expense","Business Profit","BP(%)",
    "MKT Expense","Other Expense"
]

# 3) แปลงทีละคอลัมน์ (เฉพาะที่มีอยู่จริงใน df)
for c in [c for c in num_like_cols if c in df.columns]:
    df[c] = df[c].apply(to_number)

# (ถ้าปี/เดือนเป็นข้อความ ลองแปลง)
if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
if "Month" in df.columns:
    # ถ้าเป็นชื่อเดือน ให้ลอง map เป็น 1-12 (ข้ามถ้าเป็นเลขอยู่แล้ว)
    if df["Month"].dtype == object:
        month_map = {
            'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
            'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12
        }
        df["Month_num"] = df["Month"].map(month_map)  # เก็บไว้อีกคอลัมน์
