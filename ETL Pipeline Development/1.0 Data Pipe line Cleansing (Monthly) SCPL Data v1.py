# STEP 1: ฟังก์ชันรวมทุกชีท (มี exclude_sheets)
def combine_excel_sheets(
    input_path,
    include_sheets=None,
    exclude_sheets=None,
    header=0,
    transpose_first=True,
    add_sheet_column=True,
    max_rows=14,
    max_cols=50,
    skip_blank=True
):
    xls_dict = pd.read_excel(input_path, sheet_name=None, header=header, engine="openpyxl")
    frames = []
    total_sheets = len(xls_dict)

    for sheet_name, df in xls_dict.items():
        if exclude_sheets and sheet_name in exclude_sheets:
            continue
        if include_sheets and sheet_name not in include_sheets:
            continue

        df = df.dropna(how="all").dropna(axis=1, how="all")
        if skip_blank and df.empty:
            continue

        if transpose_first:
            df = df.T.reset_index(drop=True)

        if max_cols:
            df = df.iloc[:, :max_cols]
        if max_rows:
            df = df.head(max_rows)

        if add_sheet_column:
            df.insert(0, "source_sheet", sheet_name)

        frames.append(df)

    if not frames:
        raise ValueError("ไม่มีข้อมูลที่เข้าเงื่อนไข")

    combined = pd.concat(frames, ignore_index=True)
    print(f"รวมข้อมูลสำเร็จจาก {len(frames)}/{total_sheets} ชีท")
    return combined

# STEP 2: ระบุชีทที่ต้องการ "ข้าม"
exclude_sheets = ["Summary", "Seasoning", "QN", "S&I","SND","BSP","Other","SVB Total"]

# STEP 3: รัน combine
combined_df = combine_excel_sheets(
    filename,
    exclude_sheets=exclude_sheets,
    include_sheets=None,
    max_rows=14,
    max_cols=50
)

# STEP 4: แสดงผล DataFrame พร้อมชื่อไฟล์
from IPython.display import display, HTML

print(f"\nแสดงตัวอย่างข้อมูลจากไฟล์: {filename}\n")
display(combined_df.head(5))

# STEP 5: บันทึกผลรวมเป็นไฟล์ใหม่
output_name_ST1 = f"combined_{os.path.splitext(filename)[0]}.xlsx"
combined_df.to_excel(output_name_ST1, index=False)
print(f"บันทึกไฟล์เรียบร้อย: {output_name_ST1}")
