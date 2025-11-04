import matplotlib.pyplot as plt

plt.figure(figsize=(8,4))
plt.plot(y_test.values, label='Actual BP%', color='black', marker='o')
plt.plot(pred_gbr if best_model is gbr else pred_enet, label='Predicted BP%', color='red', linestyle='--', marker='x')
plt.title('Actual vs Predicted BP%')
plt.xlabel('Time (Holdout Period)')
plt.ylabel('BP(%)')
plt.legend()
plt.grid(True)
plt.show()
