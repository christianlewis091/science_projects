import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Generate some example data
np.random.seed(42)
x = np.linspace(0, 10, 50)
y = 2.5 * x + 5 + np.random.normal(0, 5, size=len(x))  # Linear trend + noise

# Create DataFrame
df = pd.DataFrame({'x': x, 'y': y})

# Add a constant for the intercept
X = sm.add_constant(df['x'])  # adds a constant column to input x
model = sm.OLS(df['y'], X).fit()

# Predict values + get confidence intervals
predictions = model.get_prediction(X)
pred_summary = predictions.summary_frame(alpha=0.05)  # 95% CI


# Plot the data
plt.figure(figsize=(8, 6))
plt.scatter(df['x'], df['y'], label='Data', alpha=0.6)

# Plot the regression line
plt.plot(df['x'], pred_summary['mean'], color='red', label='Trendline')

# Plot the confidence interval
plt.fill_between(df['x'],
                 pred_summary['mean_ci_lower'],
                 pred_summary['mean_ci_upper'],
                 color='red', alpha=0.3, label='95% Confidence Interval')

# Label the plot
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regression with 95% Confidence Interval')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()






