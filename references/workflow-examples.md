# Workflow Examples

Complete end-to-end data analysis workflow examples.

## Workflow 1: Sales Data Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. Load data
try:
    df = pd.read_csv('sales.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('sales.csv', encoding='gbk')

# 2. Inspect
print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.dtypes}")
print(f"\nSummary:\n{df.describe()}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# 3. Aggregate by category
sales_by_category = df.groupby('category')['sales'].sum().sort_values(ascending=False)

# 4. Visualize
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(sales_by_category.index, sales_by_category.values, color='#E74C3C',
              edgecolor='white', linewidth=2, alpha=0.85)

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h, f'{int(h):,}',
            ha='center', va='bottom', fontproperties=chinese_font)

ax.set_xlabel('Category', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Sales Amount', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Sales by Category', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('sales_by_category.png', dpi=300, bbox_inches='tight')
```

## Workflow 2: Time Series Trend Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. Load and parse dates
df = pd.read_csv('timeseries.csv', encoding='utf-8')
df['date'] = pd.to_datetime(df['date'])

# 2. Aggregate by month
monthly = df.groupby(df['date'].dt.to_period('M'))['value'].sum()

# 3. Plot trend
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
plt.close('all')
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(monthly.index.astype(str), monthly.values,
        marker='o', linewidth=2, color='#3498DB')

for x, y in zip(monthly.index.astype(str), monthly.values):
    ax.text(x, y, f'{int(y):,}', ha='center', va='bottom',
            fontproperties=chinese_font)

ax.set_xlabel('Month', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Value', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Monthly Trend', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

plt.xticks(rotation=45)
ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('monthly_trend.png', dpi=300, bbox_inches='tight')
```

## Workflow 3: Correlation and Distribution Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 1. Load data
df = pd.read_csv('dataset.csv', encoding='utf-8')

# 2. Correlation matrix
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
corr_matrix = df[numerical_cols].corr()
print("Correlation matrix:")
print(corr_matrix)

# 3. Visualize correlation heatmap
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax,
            fmt='.2f', linewidths=0.5)

ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold',
             fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')

# 4. Distribution analysis
plt.close('all')
fig, axes = plt.subplots(1, len(numerical_cols), figsize=(5 * len(numerical_cols), 5))
if len(numerical_cols) == 1:
    axes = [axes]

for ax, col in zip(axes, numerical_cols):
    ax.hist(df[col].dropna(), bins=20, color='#3498DB', edgecolor='white', alpha=0.85)
    ax.set_title(col, fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_xlabel('Value', fontproperties=chinese_font)
    ax.set_ylabel('Frequency', fontproperties=chinese_font)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(chinese_font)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
```

## Workflow 4: Data Cleaning and Transformation

```python
import pandas as pd

# 1. Load data
df = pd.read_csv('raw_data.csv', encoding='utf-8')

# 2. Inspect data quality
print(f"Shape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# 3. Remove duplicates
df = df.drop_duplicates()

# 4. Handle missing values
# Numerical: fill with median
for col in df.select_dtypes(include=['int64', 'float64']).columns:
    df[col].fillna(df[col].median(), inplace=True)

# Categorical: fill with mode
for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# 5. Detect outliers using IQR
for col in df.select_dtypes(include=['int64', 'float64']).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    if len(outliers) > 0:
        print(f"\n{col}: {len(outliers)} outliers detected (range: {lower:.2f} - {upper:.2f})")

# 6. Create derived columns
df['derived_ratio'] = df['column_a'] / df['column_b']

# 7. Save cleaned data
df.to_csv('cleaned_data.csv', index=False, encoding='utf-8')
print(f"\nCleaned data saved. Final shape: {df.shape}")
```

## Workflow 5: Group-By Aggregation Report

```python
import pandas as pd

# 1. Load data
df = pd.read_csv('data.csv', encoding='utf-8')

# 2. Multi-level aggregation
summary = df.groupby(['region', 'category']).agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    order_count=('order_id', 'count'),
    avg_price=('price', 'mean')
).round(2)

print("Summary by Region and Category:")
print(summary)

# 3. Pivot table
pivot = df.pivot_table(
    values='sales',
    index='region',
    columns='category',
    aggfunc='sum',
    fill_value=0
)

print("\nPivot Table (Sales by Region x Category):")
print(pivot)

# 4. Top N analysis
top_products = df.groupby('product')['sales'].sum().nlargest(10)
print(f"\nTop 10 Products by Sales:")
print(top_products)
```
