# STEP 1: อ่านไฟล์
df = pd.read_csv(output_name_ST3)

# STEP 4: ตัด col C–D
if df.shape[1] >= 1:
    df = df.drop(df.columns[0], axis=1)


# STEP 6: ตั้งชื่อไฟล์ผลลัพธ์
base_name = os.path.splitext(filename)[0]
output_name_ST4 = f"{base_name}_cleansed.csv"

# STEP 7: บันทึกและดาวน์โหลด
df.to_csv(output_name_ST4, index=False)

# แสดงผลในตาราง (สวยกว่า print ธรรมดา)
from IPython.display import display
display(df.head(5))
