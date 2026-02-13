---
name: data-analysis
description: This skill should be used when the user asks to "analyze data", "explore a dataset", "create a chart", "visualize data", "generate statistics", "clean data", "load CSV file", "load Excel file", "plot a graph", "show data distribution", "calculate correlation", or mentions data profiling, EDA, data transformation, or working with CSV, Excel, JSON, or Parquet files. Supports bilingual (Chinese/English) data and outputs.
allowed-tools: Read, Bash, Write, Edit, Glob, Grep
---

# Data Analysis Skill

Comprehensive data analysis capability for exploratory data analysis (EDA), visualization, statistical analysis, and data transformation. Supports CSV, Excel, JSON, and Parquet formats with bilingual (Chinese/English) output.

## Core Workflow (v2 Auto Mode)

When the user provides a dataset (CSV/Excel/JSON/Parquet) and asks for analysis/EDA/report:

1) Use `scripts/load_data.py` to load.
2) Run `scripts/auto_eda.py` to produce:
   - `eda_output/report.md`
   - `eda_output/images/*.png`
3) Summarize the top insights in Chinese:
   - missingness (top 5)
   - numeric distributions (skew/outliers)
   - strongest correlations (top 5)
   - any notable group differences (top 3)
4) If the user requests, export report to Word/PDF (optional extension).

### Step 1: Load and Inspect Data

Load data with encoding fallback for Chinese content:

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

try:
    df = pd.read_csv(filepath, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(filepath, encoding='gbk')

print(f"Data shape: {df.shape}")
print(f"\nColumn info:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
```

For Excel files, use `pd.read_excel(filepath)`. For JSON, use `pd.read_json(filepath)`. For Parquet, use `pd.read_parquet(filepath)`.

### Step 2: Exploratory Analysis

Generate summary statistics and inspect distributions:

```python
print(df.describe())

categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"\n{col} unique values:")
    print(df[col].value_counts())
```

### Step 3: Create Visualizations

#### Chinese Font Configuration (MANDATORY)

Apply `FontProperties` to ALL text elements to prevent garbled Chinese characters:

```python
chinese_font = fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
```

On Windows, use a system Chinese font path instead:

```python
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')  # Microsoft YaHei
```

Apply the font to every text element: titles, axis labels, tick labels, legends, and annotations. See `references/chinese-font-guide.md` for complete font configuration details.

#### Standard Chart Pattern

```python
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(df['category'], df['value'], color='#E74C3C',
              edgecolor='white', linewidth=2, alpha=0.85)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{int(height)}', ha='center', va='bottom',
            fontsize=12, fontweight='bold', fontproperties=chinese_font)

ax.set_xlabel('Category', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Value', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Chart Title', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('output_chart.png', dpi=300, bbox_inches='tight')
```

For additional chart types (line, scatter, histogram, pie, heatmap), see `references/chart-patterns.md`.

### Step 4: Statistical Analysis

```python
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
correlation = df[numerical_cols].corr()
print("Correlation matrix:")
print(correlation)

grouped = df.groupby('category')['value'].agg(['mean', 'median', 'std', 'count'])
print("\nGroup statistics:")
print(grouped)
```

### Step 5: Data Transformation

```python
# Filtering
filtered_df = df.query("sales > 10000 and region == 'East'")

# Derived columns
df['profit'] = df['sales'] - df['cost']
df['margin'] = df['profit'] / df['sales']

# Handle missing values
df['column'].fillna(df['column'].mean(), inplace=True)
```

## Professional Chart Formatting Checklist

1. Data labels on bars/points
2. Clear axis labels with units
3. Descriptive title
4. Appropriate color scheme
5. Subtle grid lines (Y-axis only)
6. Remove top and right borders
7. High resolution output (dpi=300)
8. Use `plt.tight_layout()` before saving

## Color Palettes

```python
VIBRANT  = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
WARM     = ['#E74C3C', '#E67E22', '#F39C12', '#F1C40F']
COOL     = ['#3498DB', '#2ECC71', '#1ABC9C', '#16A085']
CORPORATE = ['#2C3E50', '#34495E', '#7F8C8D', '#95A5A6']
```

## Critical Rules

- **Never** use `plt.show()` in non-interactive environments; always use `plt.savefig()`.
- **Always** call `plt.close('all')` before creating new plots.
- **Always** apply `fontproperties=chinese_font` to ALL Chinese text elements.
- **Never** assume UTF-8 encoding; try multiple encodings for Chinese data.
- **Never** print entire large dataframes; use `.head()`, `.tail()`, or `.sample()`.
- For large datasets (>100K rows), sample first for exploration.

## Dependencies

Required Python packages:

```bash
pip install pandas matplotlib openpyxl pyarrow seaborn
```

## Additional Resources

### Scripts

Reusable automation scripts for common operations:
- **`scripts/find_chinese_font.py`** - Auto-detect Chinese fonts across Windows/Linux/macOS
- **`scripts/load_data.py`** - Load CSV/Excel/JSON/Parquet with automatic encoding detection
- **`scripts/quick_chart.py`** - Generate bar, line, and pie charts with one function call
- **`scripts/auto_eda.py`** - One-command full EDA: histograms, bar charts, correlation heatmap, outlier detection, and markdown report

### Reference Files

For detailed patterns and techniques, consult:
- **`references/chart-patterns.md`** - Complete chart type examples (line, scatter, histogram, pie, heatmap, grouped bar)
- **`references/chinese-font-guide.md`** - Comprehensive Chinese font configuration for matplotlib
- **`references/workflow-examples.md`** - Full workflow examples (sales analysis, time series, correlation analysis)

### Assets

Templates and static resources for quick start:
- **`assets/chart_template.py`** - Copy-and-modify chart template with full styling
- **`assets/color_palettes.json`** - Pre-defined professional color palettes

## Response Guidelines

1. Explain what each analysis step accomplishes and why
2. Interpret results with actionable insights, not just raw output
3. Use bilingual (Chinese/English) labels where data contains Chinese content
4. Ask clarifying questions when the analysis request is ambiguous
5. Suggest follow-up analyses that might provide additional value
