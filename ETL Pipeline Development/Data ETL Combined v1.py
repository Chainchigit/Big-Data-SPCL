# STEP 1) Install libraries (Colab)
!pip -q install pandas

# STEP 2) Upload multiple CSV files

from google.colab import files
uploaded = files.upload()  # เลือกหลายไฟล์ CSV ได้พร้อมกัน
file_list = list(uploaded.keys())
print(f"Uploaded {len(file_list)} files:", file_list)

# STEP 3) Combine all CSV files (no row/col limits)
import pandas as pd
import os

def read_csv_safely(path: str):
    """อ่าน CSV เป็นข้อความทั้งหมด โดยตรวจจับ encoding อัตโนมัติ"""
    encodings_try = ["utf-8-sig", "utf-8", "tis-620", "cp874"]
    for enc in encodings_try:
        try:
            return pd.read_csv(path, dtype=str, encoding=enc)
        except Exception:
            continue
    raise ValueError(f"อ่านไฟล์ {path} ไม่ได้")

def combine_all_csvs(files: list, output_csv="combined_all.csv", output_excel="combined_all.xlsx"):
    frames = []

    for f in files:
        df = read_csv_safely(f)

        # เพิ่มชื่อไฟล์ไว้เป็นคอลัมน์ใหม่
        df.insert(0, "source_file", os.path.basename(f))

        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    # บันทึกผลลัพธ์ออก (ไม่มีการจำกัด row/col)
    combined.to_csv(output_csv, index=False, encoding="utf-8-sig")
    combined.to_excel(output_excel, index=False)

    print(f"รวมสำเร็จทั้งหมด {len(files)} ไฟล์ → {len(combined)} แถว x {len(combined.columns)} คอลัมน์")
    print("บันทึกไฟล์:", output_csv, "|", output_excel)
    return combined

# STEP 4) Run combine
combined_df = combine_all_csvs(file_list)

# STEP 5) Download results
files.download("combined_all.csv")
# files.download("combined_all.xlsx")
