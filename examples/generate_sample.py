"""Generate a sample sales dataset for demo purposes."""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 200

regions = np.random.choice(["华东", "华北", "华南", "西南", "西北"], n, p=[0.3, 0.25, 0.2, 0.15, 0.1])
categories = np.random.choice(["电子产品", "服装", "食品", "家居", "办公用品"], n)
dates = pd.date_range("2024-01-01", periods=n, freq="D")

sales = np.round(np.random.lognormal(mean=8, sigma=1, size=n), 2)
cost = np.round(sales * np.random.uniform(0.4, 0.8, n), 2)
quantity = np.random.randint(1, 100, n)

# Add some missing values
sales_with_na = sales.copy()
sales_with_na[np.random.choice(n, 5, replace=False)] = np.nan
cost_with_na = cost.copy()
cost_with_na[np.random.choice(n, 8, replace=False)] = np.nan

df = pd.DataFrame({
    "日期": dates,
    "地区": regions,
    "品类": categories,
    "销售额": sales_with_na,
    "成本": cost_with_na,
    "数量": quantity,
})

out = os.path.join(os.path.dirname(__file__), "sample_sales.csv")
df.to_csv(out, index=False, encoding="utf-8")
print(f"Sample data saved: {out} ({len(df)} rows)")
