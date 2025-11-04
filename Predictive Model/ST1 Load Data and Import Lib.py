# STEP 1: ติดตั้งไลบรารีพื้นฐาน (ถ้ายังไม่มี)
!pip install pandas matplotlib seaborn --quiet

# STEP 2: อัปโหลดไฟล์ CSV จากเครื่อง
from google.colab import files
uploaded = files.upload()  # กดปุ่มเลือกไฟล์ .csv ได้เลย

# STEP 3: โหลดไฟล์เข้ามาเป็น DataFrame
import io
import pandas as pd

filename = list(uploaded.keys())[0]
print(f"Uploaded file: {filename}")

df = pd.read_csv(io.BytesIO(uploaded[filename]), encoding='utf-8-sig')

# STEP 4: ทำความสะอาดชื่อคอลัมน์
df.columns = df.columns.str.strip()

# STEP 5: ดูข้อมูลเบื้องต้น
print("\n ข้อมูลเบื้องต้น ")
df.info()
display(df.describe(include='all').T)

# STEP 6: ดู 5 แถวแรก
display(df.head())
