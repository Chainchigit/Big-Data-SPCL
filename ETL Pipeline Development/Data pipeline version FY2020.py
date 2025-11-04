
# STEP 1) Install libs (Colab)
!pip -q install pandas openpyxl pyxlsb

# STEP 2) Upload file
from google.colab import files
uploaded = files.upload()   # เลือกไฟล์ .xlsb / .xlsx / .xlsm
FILENAME = list(uploaded.keys())[0]
print("Uploaded:", FILENAME)

# STEP 3) Utilities (auto-engine)
import os, pandas as pd
from datetime import datetime, timedelta

def _detect_engine(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsb":
        return "pyxlsb"
    elif ext in (".xlsx", ".xlsm"):
        return "openpyxl"
    elif ext == ".xls":
        raise ValueError("ไฟล์ .xls (เก่า) ยังไม่รองรับในสคริปต์นี้ กรุณาแปลงเป็น .xlsx/.xlsm หรือ .xlsb")
    else:
        raise ValueError(f"ไม่รองรับไฟล์นามสกุล: {ext}")

def read_all_sheets_auto(path: str, header=0) -> dict:
    eng = _detect_engine(path)
    xfile = pd.ExcelFile(path, engine=eng)
    sheets = xfile.sheet_names
    data = {}
    for s in sheets:
        # อ่านทุกชีทแบบไม่บังคับ dtype เพื่อให้จับ format ได้อัตโนมัติ
        data[s] = pd.read_excel(path, sheet_name=s, header=header, engine=eng)
    return data

# STEP 4) Helper: แปลง Excel Serial Date
def excel_serial_to_date(x):
    """ตรวจสอบและแปลงเลข Serial ของ Excel ให้เป็นวันที่ (YYYY-MM-DD)"""
    try:
        if isinstance(x, (int, float)) and 30000 < x < 50000:
            return (datetime(1899, 12, 30) + timedelta(days=int(x))).strftime("%Y-%m-%d")
        else:
            return x
    except:
        return x

def convert_excel_dates(df):
    """แปลงทุก cell ที่เป็น serial date ใน DataFrame"""
    return df.applymap(excel_serial_to_date)

# STEP 5) Combine function
def combine_excel_sheets(
    input_path: str,
    output_excel: str = "combined_output.xlsx",
    output_csv: str   = "combined_output.csv",
    include_sheets: list | None = None,
    exclude_sheets: list | None = None,
    header: int | None = 0,
    transpose_first: bool = True,
    add_sheet_column: bool = True,
    max_rows: int | None = 14,
    max_cols: int | None = 60,
    skip_blank: bool = True
):
    xls_dict = read_all_sheets_auto(input_path, header=header)
    frames, total_sheets = [], len(xls_dict)

    for sheet_name, df in xls_dict.items():
        if include_sheets is not None and sheet_name not in include_sheets:
            continue
        if exclude_sheets is not None and sheet_name in exclude_sheets:
            continue

        df = df.dropna(how="all").dropna(axis=1, how="all")
        if skip_blank and df.empty:
            continue

        if transpose_first:
            df = df.T.reset_index(drop=True)

        df = df.dropna(how="all")
        if skip_blank and df.empty:
            continue

        if max_cols is not None:
            df = df.iloc[:, :max_cols]
        if max_rows is not None:
            df = df.head(max_rows)

        # แปลง serial date เป็นวันที่จริง
        df = convert_excel_dates(df)

        if add_sheet_column:
            df.insert(0, "source_sheet", sheet_name)

        frames.append(df)

    if not frames:
        raise ValueError("ไม่พบข้อมูลหลังการกรอง/ทำความสะอาด—โปรดตรวจชื่อชีทหรือพารามิเตอร์")

    combined = pd.concat(frames, ignore_index=True)
    combined.to_excel(output_excel, index=False)
    combined.to_csv(output_csv, index=False, encoding="utf-8-sig")

    print(f"รวมข้อมูลจาก {len(frames)}/{total_sheets} ชีท → {len(combined)} แถว")
    print("Saved:", output_excel, "|", output_csv)
    return combined

# STEP 6) Run
exclude_sheets = ["Summary", "Seasoning", "QN", "S&I"]
combined_df = combine_excel_sheets(
    FILENAME,
    include_sheets=None,          # None = ดึงทุกชีท
    exclude_sheets=exclude_sheets,# ข้ามชีทตามรายการ
    header=0,
    transpose_first=True,
    add_sheet_column=True,
    max_rows=14,
    max_cols=60,
    skip_blank=True
)

# STEP 7) Download result
from google.colab import files
files.download("combined_output.csv")
# files.download("combined_output.xlsx")
