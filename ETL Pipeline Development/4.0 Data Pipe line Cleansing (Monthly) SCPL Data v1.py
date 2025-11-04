colE = df.columns[5]

# STEP 1 ดึงเฉพาะเลข 4 หลัก เช่น FY2025 → 2025
df[colE] = (
    df[colE].astype(str)
             .str.replace('\n', ' ', regex=False)
             .str.extract(r'((?:19|20)\d{2})', expand=False)
)

# STEP 2 แปลงเป็นตัวเลข
df[colE] = pd.to_numeric(df[colE], errors='coerce').astype('Int64')

# STEP 3 เติมค่าปีให้เต็มทั้งคอลัมน์ (ถ้ามี NaN)
df[colE] = df[colE].ffill().bfill()

# STEP 4 Save + Download
df.to_csv(output_name_ST3, index=False)

# STEP 5 แสดงผลในตาราง (สวยกว่า print ธรรมดา)
from IPython.display import display
display(df.head(5))
