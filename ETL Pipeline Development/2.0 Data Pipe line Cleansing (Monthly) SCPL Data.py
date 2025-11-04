
# STEP 1: ใช้ไฟล์จากตัวแปร output_name_ST1 (หรือหาไฟล์ combined_*.xlsx ล่าสุด)
if 'output_name_ST1' in locals() and os.path.exists(output_name_ST1):
    files_to_use = [output_name_ST1]
else:
    candidates = sorted(glob.glob("combined_*.xlsx"), key=os.path.getmtime, reverse=True)
    if candidates:
        output_name_ST1 = candidates[0]
        files_to_use = [output_name_ST1]
        print(f"[fallback] ใช้ไฟล์ล่าสุดที่พบ: {output_name_ST1}")
    else:
        raise RuntimeError("ไม่พบตัวแปร/ไฟล์ 'output_name_ST1' และไม่พบ combined_*.xlsx ในโฟลเดอร์นี้")

print("ใช้ไฟล์:", files_to_use)

# STEP 2: ฟังก์ชันล้างคอลัมน์ A
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'^\s*[\d.]+\s*', '', text).strip()
    return text

# STEP 3: รวมข้อมูลทั้งหมดเป็น DataFrame เดียว
frames = []
for fname in files_to_use:
    ext = os.path.splitext(fname)[1].lower()

    if ext == ".csv":
        df = None
        for enc in ["utf-8-sig", "utf-8", "cp874", "latin1"]:
            try:
                df = pd.read_csv(fname, encoding=enc)
                break
            except Exception:
                df = None
        if df is None:
            print(f"เปิด CSV ไม่ได้: {fname} (ข้าม)")
            continue
        if not df.empty and df.shape[1] > 0:
            df = df.copy()
            df.iloc[:, 0] = df.iloc[:, 0].apply(clean_text)
        df.insert(0, "source", fname)
        frames.append(df)

    elif ext == ".xlsx":
        xls = pd.read_excel(fname, sheet_name=None, engine="openpyxl")
        for sheet_name, sdf in xls.items():
            if not sdf.empty and sdf.shape[1] > 0:
                sdf = sdf.copy()
                sdf.iloc[:, 0] = sdf.iloc[:, 0].apply(clean_text)
            sdf.insert(0, "source", f"{fname} [{sheet_name}]")
            frames.append(sdf)

    elif ext == ".xls":
        xls = pd.read_excel(fname, sheet_name=None, engine="xlrd")
        for sheet_name, sdf in xls.items():
            if not sdf.empty and sdf.shape[1] > 0:
                sdf = sdf.copy()
                sdf.iloc[:, 0] = sdf.iloc[:, 0].apply(clean_text)
            sdf.insert(0, "source", f"{fname} [{sheet_name}]")
            frames.append(sdf)

    else:
        print(f"ข้ามไฟล์ที่ไม่รองรับ: {fname}")

if not frames:
    raise RuntimeError("ไม่มีข้อมูลให้แสดงหลังประมวลผล")

combined_df = pd.concat(frames, ignore_index=True)

print("\nCleaning complete — only column A was modified")
print(f"รวมทั้งหมด: {len(frames)} ชุด | รูปทรง: {combined_df.shape}")
print("แสดงตัวอย่างข้อมูล (10 แถวแรก):")
display(combined_df.tail(10))

# STEP 4: บันทึกผลรวมเป็นไฟล์ใหม่
base = os.path.splitext(output_name_ST1)[0]
output_name_ST2 = f"{base}_cleanA.xlsx"   # ตั้งชื่อให้ชัดว่า clean แล้ว
combined_df.to_excel(output_name_ST2, index=False)
print(f"บันทึกไฟล์เรียบร้อย: {output_name_ST2}")
