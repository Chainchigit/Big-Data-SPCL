import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# สร้างตาราง correlation
corr = df[[
    "Net Sales", "COGS", "MKT_Expense", "Other_Expense",
    "Gross Profit", "Business Profit", "BP(%)"
]].corr()

# วาด heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation with BP(%)")
plt.show()
