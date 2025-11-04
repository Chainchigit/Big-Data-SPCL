# STEP 1: แก้ค่าที่แถวแรก
df.loc[0, 'source_sheet'] = 'Product Group'
df.loc[0, '13'] = 'Year'
df.loc[0, '14'] = 'Month'
df = df.dropna(subset=['14'])

# STEP 2: ตัดคอลัมน์ '61' ออก (ถ้ามีอยู่จริง)
if '61' in df.columns:
    df = df.drop(columns=['61'])
else:
    print("ไม่มีคอลัมน์ชื่อ '61' ในตาราง")

# STEP 3: แสดงผลตรวจสอบ
from IPython.display import display
display(df.head(12))

# STEP 4: บันทึกไฟล์กลับ
output_name = "cleaned_step4_no_col61.csv"
df.to_csv(output_name, index=False, encoding="utf-8-sig")
print(f"ลบคอลัมน์ '61' และแก้ค่า row 0 เรียบร้อย -> {output_name}")
