"""
Auto EDA v2:
- infer column types
- summarize dataset + missingness
- auto charts
- correlations
- groupby summaries for categorical columns
- write a markdown report + save charts
"""

from __future__ import annotations
import os
import math
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load_data import load_data
from find_chinese_font import find_chinese_font


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def infer_column_roles(df: pd.DataFrame):
    """Infer column roles: numeric, categorical, datetime, id-like."""
    roles = {"numeric": [], "categorical": [], "datetime": [], "id_like": []}

    for col in df.columns:
        s = df[col]

        # Try datetime
        if s.dtype == "object":
            parsed = pd.to_datetime(s, errors="coerce", format="mixed")
            # treat as datetime if enough parse success
            if parsed.notna().mean() >= 0.7:
                roles["datetime"].append(col)
                continue

        # Numeric
        if pd.api.types.is_numeric_dtype(s):
            roles["numeric"].append(col)
            continue

        # Categorical vs id-like
        nunique = s.nunique(dropna=True)
        n = len(s)
        # Heuristic: id-like if unique ratio high
        if n > 0 and (nunique / n) > 0.9:
            roles["id_like"].append(col)
        else:
            roles["categorical"].append(col)

    return roles


def _set_chinese_font():
    chinese_font = find_chinese_font()
    if chinese_font:
        plt.rcParams["axes.unicode_minus"] = False
    return chinese_font


def save_hist(df, col, outpath, font=None):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(10, 6))
    s = df[col].dropna()
    ax.hist(s, bins=30)
    ax.set_title(f"分布直方图: {col}" if font else f"Histogram: {col}",
                 fontproperties=font)
    ax.set_xlabel(col, fontproperties=font)
    ax.set_ylabel("Count", fontproperties=font)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")


def save_bar_topk(df, col, outpath, k=20, font=None):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(12, 6))
    vc = df[col].astype(str).value_counts(dropna=True).head(k)
    ax.bar(vc.index, vc.values)
    ax.set_title(f"Top {k} 类别频数: {col}" if font else f"Top {k} categories: {col}",
                 fontproperties=font)
    ax.set_xlabel(col, fontproperties=font)
    ax.set_ylabel("Count", fontproperties=font)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")


def save_line(df, time_col, y_col, outpath, font=None):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(12, 6))
    d = df[[time_col, y_col]].copy()
    d[time_col] = pd.to_datetime(d[time_col], errors="coerce")
    d = d.dropna().sort_values(time_col)
    ax.plot(d[time_col], d[y_col])
    ax.set_title(f"时间趋势: {y_col} vs {time_col}" if font else f"Trend: {y_col} vs {time_col}",
                 fontproperties=font)
    ax.set_xlabel(time_col, fontproperties=font)
    ax.set_ylabel(y_col, fontproperties=font)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")


def save_corr_heatmap(df, numeric_cols, outpath, font=None):
    if len(numeric_cols) < 2:
        return False
    plt.close("all")
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df[numeric_cols].corr(numeric_only=True)
    im = ax.imshow(corr.values)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontproperties=font)
    ax.set_yticklabels(numeric_cols, fontproperties=font)
    ax.set_title("相关系数热力图" if font else "Correlation heatmap",
                 fontproperties=font)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    return True


def quick_outliers_iqr(df, col):
    s = df[col].dropna()
    if s.empty:
        return None
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr
    out = s[(s < lo) | (s > hi)]
    return {"q1": float(q1), "q3": float(q3), "iqr": float(iqr),
            "low": float(lo), "high": float(hi),
            "outlier_count": int(out.shape[0]),
            "outlier_ratio": float(out.shape[0] / max(1, s.shape[0]))}


def write_report_md(
    df: pd.DataFrame,
    roles: dict,
    charts: list[tuple[str, str]],
    outliers: dict,
    group_summaries: list[str],
    outpath: str,
):
    lines = []
    lines.append("# 自动数据分析报告 (Auto EDA v2)\n")
    lines.append(f"- 行数: **{df.shape[0]}**\n")
    lines.append(f"- 列数: **{df.shape[1]}**\n")

    # Missingness
    miss = df.isna().mean().sort_values(ascending=False)
    lines.append("\n## 缺失值概览\n")
    lines.append("|列名|缺失率|\n|---|---|\n")
    for col, r in miss.head(30).items():
        lines.append(f"|{col}|{r:.2%}|\n")

    # Column roles
    lines.append("\n## 字段类型推断\n")
    for k in ["datetime", "numeric", "categorical", "id_like"]:
        lines.append(f"- **{k}**: {', '.join(roles[k]) if roles[k] else '(无)'}\n")

    # Numeric summary
    if roles["numeric"]:
        lines.append("\n## 数值字段统计摘要\n")
        desc = df[roles["numeric"]].describe(percentiles=[0.25, 0.5, 0.75]).T
        # Keep it small
        keep = desc[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]].head(30)
        lines.append(keep.to_markdown())

        lines.append("\n\n## 异常值（IQR 快速检测）\n")
        lines.append("|字段|异常数|异常比例|下界|上界|\n|---|---:|---:|---:|---:|\n")
        for col, info in outliers.items():
            if not info:
                continue
            lines.append(
                f"|{col}|{info['outlier_count']}|{info['outlier_ratio']:.2%}|"
                f"{info['low']:.3g}|{info['high']:.3g}|\n"
            )

    # Group summaries
    if group_summaries:
        lines.append("\n## 分组洞察（类别字段 → 数值字段均值）\n")
        lines.extend(group_summaries)

    # Charts
    if charts:
        lines.append("\n## 自动生成图表\n")
        for title, rel in charts:
            lines.append(f"### {title}\n\n![]({rel})\n")

    # Append bilingual insights
    lines.extend(generate_bilingual_insights(df, roles, outliers))

    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def run(filepath: str, outdir: str = "eda_output", max_numeric_hists=6, max_cat_bars=4):
    df = load_data(filepath)

    _ensure_dir(outdir)
    imgdir = os.path.join(outdir, "images")
    _ensure_dir(imgdir)

    font = _set_chinese_font()
    roles = infer_column_roles(df)

    charts = []
    outliers = {}

    # Numeric hists
    for col in roles["numeric"][:max_numeric_hists]:
        out = os.path.join(imgdir, f"hist_{col}.png")
        save_hist(df, col, out, font=font)
        charts.append((f"直方图：{col}", os.path.relpath(out, outdir)))
        outliers[col] = quick_outliers_iqr(df, col)

    # Categorical bar top-k
    for col in roles["categorical"][:max_cat_bars]:
        out = os.path.join(imgdir, f"bar_{col}.png")
        save_bar_topk(df, col, out, k=20, font=font)
        charts.append((f"Top 类别：{col}", os.path.relpath(out, outdir)))

    # Time trend: pick first datetime + first numeric
    if roles["datetime"] and roles["numeric"]:
        tcol = roles["datetime"][0]
        ycol = roles["numeric"][0]
        out = os.path.join(imgdir, f"trend_{ycol}_by_{tcol}.png")
        save_line(df, tcol, ycol, out, font=font)
        charts.append((f"趋势图：{ycol} vs {tcol}", os.path.relpath(out, outdir)))

    # Corr heatmap
    if roles["numeric"]:
        out = os.path.join(imgdir, "corr_heatmap.png")
        ok = save_corr_heatmap(df, roles["numeric"][:12], out, font=font)
        if ok:
            charts.append(("相关性热力图（前 12 个数值列）", os.path.relpath(out, outdir)))

    # Group summaries: for first 2 categorical, group by and show mean of first 2 numeric
    group_summaries = []
    if roles["categorical"] and roles["numeric"]:
        num_cols = roles["numeric"][:2]
        for ccol in roles["categorical"][:2]:
            g = df.groupby(ccol)[num_cols].mean(numeric_only=True).sort_values(num_cols[0], ascending=False).head(15)
            group_summaries.append(f"\n### 按 {ccol} 分组（Top 15）\n")
            group_summaries.append(g.to_markdown())
            group_summaries.append("\n")

    report_path = os.path.join(outdir, "report.md")
    write_report_md(df, roles, charts, outliers, group_summaries, report_path)

    return report_path

def generate_bilingual_insights(df, roles, outliers):
    lines = []
    lines.append("\n## 核心洞察 | Key Insights\n")

    # 1. Missingness
    miss = df.isna().mean().sort_values(ascending=False)
    top_miss = miss.head(3)

    lines.append("### 1️⃣ 缺失值情况 | Missingness\n")
    for col, r in top_miss.items():
        lines.append(
            f"- 【{col}】缺失率为 {r:.2%}。"
            f" (Column '{col}' has a missing rate of {r:.2%}).\n"
        )

    # 2. Numeric outliers
    if outliers:
        lines.append("\n### 2️⃣ 异常值检测 | Outliers\n")
        for col, info in list(outliers.items())[:3]:
            if not info:
                continue
            lines.append(
                f"- 【{col}】存在 {info['outlier_count']} 个异常值，"
                f"占比 {info['outlier_ratio']:.2%}。"
                f" (Column '{col}' has {info['outlier_count']} outliers, "
                f"ratio {info['outlier_ratio']:.2%}).\n"
            )

    # 3. Correlation insight
    if len(roles["numeric"]) >= 2:
        corr = df[roles["numeric"]].corr(numeric_only=True)
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        pairs = upper.unstack().dropna().sort_values(ascending=False)
        if not pairs.empty:
            top_pair = pairs.index[0]
            val = pairs.iloc[0]
            lines.append("\n### 3️⃣ 强相关变量 | Strong Correlation\n")
            lines.append(
                f"- 【{top_pair[0]}】与【{top_pair[1]}】相关系数为 {val:.3f}。"
                f" (Correlation between '{top_pair[0]}' and "
                f"'{top_pair[1]}' is {val:.3f}).\n"
            )

    # 4. Recommendations
    lines.append("\n## 下一步建议 | Next Steps\n")
    lines.append("- 建议进行进一步特征工程或异常值处理。"
                 " (Consider feature engineering or outlier treatment.)\n")
    lines.append("- 若目标变量存在，可进行回归或分类建模。"
                 " (If a target variable exists, build regression or classification models.)\n")
    lines.append("- 可进行更细粒度分组分析。"
                 " (Perform deeper group-based analysis.)\n")

    return lines


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("filepath", help="Path to CSV/Excel/JSON/Parquet")
    p.add_argument("--outdir", default="eda_output")
    args = p.parse_args()
    rp = run(args.filepath, args.outdir)
    print(f"[OK] Report saved: {rp}")
