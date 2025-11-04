import seaborn as sns

sns.lmplot(
    x="MKT_Expense",
    y="BP_pct",
    data=grp_filtered.assign(MKT_Expense=grp_filtered["MKT_Expense"]/grp_filtered["Net_Sales"]*100),
    height=5, aspect=1.2, scatter_kws={'alpha':0.7}
)
plt.title("MKT Ratio vs BP(%) — Trend Line (Outlier Trimmed)")
plt.xlabel("MKT Expense / Net Sales (%)")
plt.ylabel("BP(%)")
plt.show()
