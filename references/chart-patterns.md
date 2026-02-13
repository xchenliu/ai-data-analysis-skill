# Chart Patterns Reference

Complete chart type examples for data visualization. All examples assume `chinese_font` is already configured via `FontProperties`.

## Line Chart with Trend

```python
plt.close('all')
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['date'], df['value'], marker='o', linewidth=2, color='#3498DB')

for x, y in zip(df['date'], df['value']):
    ax.text(x, y, f'{int(y):,}', ha='center', va='bottom',
            fontproperties=chinese_font)

ax.set_xlabel('Date', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Value', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Trend Over Time', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

plt.xticks(rotation=45)
ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('line_chart.png', dpi=300, bbox_inches='tight')
```

## Scatter Plot with Correlation

```python
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 8))

scatter = ax.scatter(df['x'], df['y'], c=df['category'].astype('category').cat.codes,
                     cmap='viridis', alpha=0.7, edgecolors='white', s=80)

ax.set_xlabel('X Variable', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Y Variable', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Scatter Plot', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

ax.grid(True, alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('scatter_plot.png', dpi=300, bbox_inches='tight')
```

## Histogram with Distribution

```python
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 6))

n, bins, patches = ax.hist(df['value'], bins=20, color='#3498DB',
                            edgecolor='white', alpha=0.85)

ax.set_xlabel('Value Range', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Frequency', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Distribution', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('histogram.png', dpi=300, bbox_inches='tight')
```

## Pie Chart with Percentages

```python
plt.close('all')
fig, ax = plt.subplots(figsize=(8, 8))

colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
wedges, texts, autotexts = ax.pie(
    df['value'], labels=df['category'], autopct='%1.1f%%',
    colors=colors, startangle=90, pctdistance=0.85
)

for text in texts:
    text.set_fontproperties(chinese_font)
for autotext in autotexts:
    autotext.set_fontproperties(chinese_font)
    autotext.set_fontsize(10)

ax.set_title('Category Distribution', fontsize=14, fontweight='bold',
             fontproperties=chinese_font)

plt.tight_layout()
plt.savefig('pie_chart.png', dpi=300, bbox_inches='tight')
```

## Grouped Bar Chart

```python
import numpy as np

plt.close('all')
fig, ax = plt.subplots(figsize=(12, 6))

categories = df['category'].unique()
groups = df['group'].unique()
x = np.arange(len(categories))
width = 0.8 / len(groups)
colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']

for i, group in enumerate(groups):
    group_data = df[df['group'] == group]
    bars = ax.bar(x + i * width, group_data['value'], width,
                  label=group, color=colors[i % len(colors)],
                  edgecolor='white', linewidth=1.5)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=9, fontproperties=chinese_font)

ax.set_xlabel('Category', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Value', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Grouped Comparison', fontsize=14, fontweight='bold', fontproperties=chinese_font)
ax.set_xticks(x + width * (len(groups) - 1) / 2)
ax.set_xticklabels(categories)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

ax.legend(prop=chinese_font)
ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('grouped_bar.png', dpi=300, bbox_inches='tight')
```

## Box Plot

```python
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 6))

data_groups = [df[df['category'] == cat]['value'] for cat in df['category'].unique()]
bp = ax.boxplot(data_groups, labels=df['category'].unique(), patch_artist=True)

colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Category', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_ylabel('Value', fontsize=12, fontweight='bold', fontproperties=chinese_font)
ax.set_title('Box Plot Comparison', fontsize=14, fontweight='bold', fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('box_plot.png', dpi=300, bbox_inches='tight')
```

## Correlation Heatmap

```python
import seaborn as sns

plt.close('all')
fig, ax = plt.subplots(figsize=(10, 8))

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
corr_matrix = df[numerical_cols].corr()

sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax,
            fmt='.2f', linewidths=0.5)

ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold',
             fontproperties=chinese_font)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
```
