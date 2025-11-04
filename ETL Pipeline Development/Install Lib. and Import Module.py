# STEP 1: ติดตั้งไลบรารี
!pip -q install pandas openpyxl

# STEP 2: อัปโหลดไฟล์ Excel
from google.colab import files
uploaded = files.upload()
filename = list(uploaded.keys())[0]
print("Uploaded file:", filename)

# STEP 3: Import Module
import pandas as pd
import re, os, glob
from IPython.display import display
