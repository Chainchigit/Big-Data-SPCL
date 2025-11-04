df["MKT_to_Sales"] = df["MKT_Expense"] / df["Net Sales"] * 100
df["COGS_to_Sales"] = df["COGS"] / df["Net Sales"] * 100
df["Other_to_Sales"] = df["Other_Expense"] / df["Net Sales"] * 100

ratios = df[["Year","Month","BP(%)","MKT_to_Sales","COGS_to_Sales","Other_to_Sales"]].groupby(["Year","Month"]).mean()

ratios.plot(figsize=(10,6), marker="o")
plt.title("Expense Ratio vs BP(%) Trend")
plt.grid(True)
plt.show()
