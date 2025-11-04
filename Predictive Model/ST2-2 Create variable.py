# รวมค่าใช้จ่ายทางการตลาด
df["MKT_Expense"] = (
    df["Advertising"]
    + df["Sales Campaign"]
    + df["Market Research Expense"]
    + df["Royalty"]
    + df["Commission"]
    + df["Other Marketing Expense"]
    + df["Personnel Cost (sales)"]
)

# รวมค่าใช้จ่ายอื่น ๆ
df["Other_Expense"] = (
    df["R&D Expense"]
    + df["G&A Expense"]
    + df["F-cost"]
    + df["GA-Others (sales)"]
    + df["GA-Others (R&D)"]
    + df["GA-Others (other)"]
    + df["Depreciation (sales)"]
    + df["Depreciation (R&D)"]
    + df["Depreciation (other)"]
    + df["Transportation"]
)
