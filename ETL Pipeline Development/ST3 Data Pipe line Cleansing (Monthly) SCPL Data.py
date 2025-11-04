# STEP 1 อ่านไฟล์จาก output_name_ST2
ext = os.path.splitext(output_name_ST2)[1].lower()
if ext == ".csv":
    df = pd.read_csv(output_name_ST2)
elif ext in [".xlsx", ".xls"]:
    df = pd.read_excel(output_name_ST2, engine="openpyxl")
else:
    raise ValueError("ไฟล์ไม่ใช่ .csv หรือ .xlsx")

# STEP 2 ฟังก์ชัน mapping เดือน
month_map = {
    'january': 'Jan', 'february': 'Feb', 'march': 'Mar', 'april': 'Apr',
    'may': 'May', 'june': 'Jun', 'july': 'Jul', 'august': 'Aug',
    'september': 'Sep', 'october': 'Oct', 'november': 'Nov', 'december': 'Dec'
}

def clean_month(text):
    if not isinstance(text, str):
        return pd.NA
    s = re.sub(r'\(.*?\)', '', text.replace("\r", " ").replace("\n", " "))
    s = re.sub(r'\s+', ' ', s).strip()
    for m in month_map:
        if re.search(m, s, re.IGNORECASE):
            return month_map[m]
    return pd.NA

# STEP 3 ทำการ fixed คอลัมน์ G
df.iloc[:, 6] = df.iloc[:, 6].apply(clean_month)

# STEP 4 แสดงผล
display(df.head(12))

# STEP 5 ตั้งชื่อไฟล์และบันทึก
base = os.path.splitext(output_name_ST2)[0]
output_name_ST3 = f"{base}_month_short.csv"
df.to_csv(output_name_ST3, index=False, encoding="utf-8-sig")
print(f"เขียนไฟล์ใหม่เรียบร้อย: {output_name_ST3}")
