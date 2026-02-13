"""Reusable chart template. Copy and modify for specific needs."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import sys

# --- Configuration ---
DATA_FILE = 'your_data.csv'
OUTPUT_FILE = 'output_chart.png'
CHART_TITLE = 'Chart Title'
X_COLUMN = 'x_column_name'
Y_COLUMN = 'y_column_name'

# --- Font Setup ---
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from find_chinese_font import find_chinese_font
chinese_font = find_chinese_font()
font_kw = {'fontproperties': chinese_font} if chinese_font else {}

# --- Load Data ---
try:
    df = pd.read_csv(DATA_FILE, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(DATA_FILE, encoding='gbk')

# --- Create Chart ---
plt.close('all')
fig, ax = plt.subplots(figsize=(10, 6))

# TODO: Replace with desired chart type
bars = ax.bar(df[X_COLUMN], df[Y_COLUMN], color='#E74C3C',
              edgecolor='white', linewidth=2, alpha=0.85)

# Value labels
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2., h,
            f'{h:,.0f}', ha='center', va='bottom',
            fontsize=10, fontweight='bold', **font_kw)

# Labels and title
ax.set_xlabel(X_COLUMN, fontsize=12, fontweight='bold', **font_kw)
ax.set_ylabel(Y_COLUMN, fontsize=12, fontweight='bold', **font_kw)
ax.set_title(CHART_TITLE, fontsize=14, fontweight='bold', **font_kw)

if chinese_font:
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(chinese_font)

# Styling
ax.grid(True, axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save
plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
print(f"Chart saved to: {OUTPUT_FILE}")
