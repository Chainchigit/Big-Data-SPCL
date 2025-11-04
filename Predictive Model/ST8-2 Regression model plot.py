plt.figure(figsize=(8,5))
colors = ['green' if v > 0 else 'red' for v in coef]
coef.sort_values().plot(kind="barh", color=colors)
plt.title("Feature Impact on BP(%) — Ridge Regression (TimeSeries CV)")
plt.xlabel("Coefficient (Standardized Scale)")
plt.axvline(0, color='black', linewidth=1)
plt.grid(True, axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
