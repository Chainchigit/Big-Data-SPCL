# STEP 1: อ่านไฟล์จาก output_name
ext = os.path.splitext(output_name)[1].lower()

if ext == ".csv":
    df = None
    for enc in ["utf-8-sig", "utf-8", "cp874", "latin1"]:
        try:
            df = pd.read_csv(output_name, encoding=enc)
            break
        except Exception:
            pass
    if df is None:
        raise RuntimeError("อ่าน CSV ไม่สำเร็จในทุก encoding")
elif ext in [".xlsx", ".xls"]:
    df = pd.read_excel(output_name, engine="openpyxl")
else:
    raise ValueError("ไฟล์ไม่ใช่ .csv หรือ .xlsx/.xls")

# STEP 2: ตัวช่วยแปลงเลขแบบยืดหยุ่น
import re
def to_numeric_smart(s):
    if pd.isna(s):
        return pd.NA
    if isinstance(s, str):
        s = s.strip()
        if re.fullmatch(r'\(.*\)', s):  # (123) -> -123
            s = '-' + s[1:-1]
        s = s.replace(',', '')
    return pd.to_numeric(s, errors='coerce')

# STEP 3: รวมคอลัมน์แบบปลอดภัย
def safe_sum(df, cols, new_col):
    exist = [c for c in cols if c in df.columns]
    if not exist:
        df[new_col] = 0.0
        print(f"ไม่พบคอลัมน์ในชุด {new_col}: {cols}")
        return
    nums = df[exist].applymap(to_numeric_smart).fillna(0)
    df[new_col] = nums.sum(axis=1)

# STEP 4: สร้างคอลัมน์ที่ต้องการ
mkt_cols   = ['35','36','37','41','42']
other_cols = ['46','52']

safe_sum(df, mkt_cols,   "MKT Expense")
safe_sum(df, other_cols, "Other")

# STEP 5: ปรับแถวแรกให้เป็นชื่อคอลัมน์
df.loc[0, "MKT Expense"] = "MKT Expense"
df.loc[0, "Other"] = "Other"

# STEP 6: เปลี่ยนชื่อ header
df = df.rename(columns={"MKT Expense": "59", "Other": "60"})

# (ตัวเลือก) ให้ข้อมูลไปอยู่ Excel แถวที่ 2
add_blank_top_row = True   # ถ้าไม่ต้องการให้เป็นแถวที่ 2 ให้เปลี่ยนเป็น False
if add_blank_top_row:
    df_out = pd.concat([pd.DataFrame([{c: pd.NA for c in df.columns}]), df], ignore_index=True)
else:
    df_out = df

# STEP 7: แสดงผลตรวจสอบ
print("=== ตัวอย่างข้อมูล ===")
print(df_out.head(5)[["59", "60"]])

# STEP 8: บันทึกเป็น Excel
output_filename = "Cleansing_Summary.xlsx"
df_out.to_excel(output_filename, index=False)
print(f"\nสร้างไฟล์เรียบร้อย: {output_filename}")

# STEP 9: ดาวน์โหลดอัตโนมัติ (Colab)
try:
    from google.colab import files
    files.download(output_filename)
except Exception:
    pass
