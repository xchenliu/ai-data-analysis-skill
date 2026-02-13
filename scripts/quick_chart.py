"""Quick chart generation with Chinese font support."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from find_chinese_font import find_chinese_font

import pandas as pd
import matplotlib.pyplot as plt


def create_bar_chart(df, x_col, y_col, title='', output='chart.png'):
    """Create a professional bar chart with optional Chinese font support."""
    chinese_font = find_chinese_font()

    plt.close('all')
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
              '#1ABC9C', '#E67E22', '#34495E']
    bar_colors = [colors[i % len(colors)] for i in range(len(df))]

    bars = ax.bar(df[x_col].astype(str), df[y_col], color=bar_colors,
                  edgecolor='white', linewidth=2, alpha=0.85)

    font_kwargs = {'fontproperties': chinese_font} if chinese_font else {}

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{height:,.0f}' if height == int(height) else f'{height:,.2f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                **font_kwargs)

    ax.set_xlabel(x_col, fontsize=12, fontweight='bold', **font_kwargs)
    ax.set_ylabel(y_col, fontsize=12, fontweight='bold', **font_kwargs)
    ax.set_title(title or f'{y_col} by {x_col}', fontsize=14, fontweight='bold',
                 **font_kwargs)

    if chinese_font:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(chinese_font)

    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, df[y_col].max() * 1.15)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output}")


def create_line_chart(df, x_col, y_col, title='', output='chart.png'):
    """Create a professional line chart with optional Chinese font support."""
    chinese_font = find_chinese_font()

    plt.close('all')
    fig, ax = plt.subplots(figsize=(12, 6))

    font_kwargs = {'fontproperties': chinese_font} if chinese_font else {}

    ax.plot(df[x_col].astype(str), df[y_col], marker='o', linewidth=2,
            color='#3498DB', markersize=6)

    ax.set_xlabel(x_col, fontsize=12, fontweight='bold', **font_kwargs)
    ax.set_ylabel(y_col, fontsize=12, fontweight='bold', **font_kwargs)
    ax.set_title(title or f'{y_col} Trend', fontsize=14, fontweight='bold',
                 **font_kwargs)

    if chinese_font:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(chinese_font)

    plt.xticks(rotation=45)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output}")


def create_pie_chart(df, label_col, value_col, title='', output='chart.png'):
    """Create a professional pie chart with optional Chinese font support."""
    chinese_font = find_chinese_font()

    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 8))

    colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
              '#1ABC9C', '#E67E22', '#34495E']

    wedges, texts, autotexts = ax.pie(
        df[value_col], labels=df[label_col], autopct='%1.1f%%',
        colors=colors[:len(df)], startangle=90, pctdistance=0.85
    )

    if chinese_font:
        for text in texts + autotexts:
            text.set_fontproperties(chinese_font)

    ax.set_title(title or f'{value_col} Distribution', fontsize=14,
                 fontweight='bold',
                 **(({'fontproperties': chinese_font} if chinese_font else {})))

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output}")
