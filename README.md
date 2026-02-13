# AI Data Analysis Skill

A reusable **Claude Code Skill** for automated data analysis, EDA (Exploratory Data Analysis), and visualization. Designed for use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), Anthropic's official CLI tool.

> Supports bilingual (Chinese/English) data and outputs. Built-in Chinese font auto-detection for matplotlib charts.

## Features

- **Auto EDA** - One-command full exploratory data analysis with markdown report and charts
- **Multi-format Support** - CSV, Excel (.xlsx/.xls), JSON, Parquet with automatic encoding detection (UTF-8, GBK, GB2312, etc.)
- **Chinese Font Handling** - Cross-platform (Windows/Linux/macOS) Chinese font auto-detection for matplotlib
- **Professional Charts** - Bar, line, scatter, histogram, pie, box plot, grouped bar, correlation heatmap
- **Bilingual Reports** - Auto-generated insights in both Chinese and English
- **Outlier Detection** - IQR-based automatic outlier detection and reporting

## Project Structure

```
.
├── SKILL.md                          # Claude Code skill definition (core prompt)
├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── auto_eda.py                   # One-command full EDA pipeline (+ Word/PDF export)
│   ├── load_data.py                  # Multi-format data loader with encoding fallback
│   ├── quick_chart.py                # Quick bar/line/pie chart generation
│   └── find_chinese_font.py          # Cross-platform Chinese font detector
├── references/
│   ├── chart-patterns.md             # Chart type examples (line, scatter, histogram, pie, heatmap, etc.)
│   ├── chinese-font-guide.md         # Chinese font configuration guide for matplotlib
│   └── workflow-examples.md          # End-to-end workflow examples (sales, time series, correlation)
├── assets/
│   ├── chart_template.py             # Copy-and-modify chart template with full styling
│   └── color_palettes.json           # Pre-defined professional color palettes
├── examples/
│   ├── sample_jobinfo_1000.csv       # Real-world job listing dataset (1000 rows, 25 columns)
│   └── sample_output/                # Auto-generated EDA report + charts
└── LICENSE
```

## Example Output

Run `auto_eda.py` on a real-world Chinese job listing dataset (1000 rows, 25 columns) to see what you get:

### Top Job Titles
![Job Titles](examples/sample_output/images/bar_岗位名称.png)

### Salary Distribution
![Salary](examples/sample_output/images/bar_最高薪资.png)

### Geo Coordinate Distribution
![Longitude](examples/sample_output/images/hist_经度.png)

### Correlation Heatmap
![Heatmap](examples/sample_output/images/corr_heatmap.png)

### Auto-generated Report (excerpt)

> **Dataset**: 1000 rows x 25 columns (job listings with salary, location, requirements, etc.)
>
> | Insight | Detail |
> |---------|--------|
> | Missing 96% | 专业要求 (major requirement) mostly unfilled |
> | Missing 84.8% | 特殊要求 (special requirements) mostly unfilled |
> | 26.6% outliers | 经度 (longitude) - jobs spread across many cities |
> | Strong correlation | 经度 & 维度 = **0.848** (geographic clustering) |
>
> Top job title: **数据分析师** (Data Analyst) with 191 listings

Full example data and output are in the [`examples/`](examples/) directory. The complete dataset (5660 rows, 19MB) is available as a [Release download](https://github.com/xchenliu/ai-data-analysis-skill/releases/tag/v1.0.0).

## Quick Start

### As a Claude Code Skill

1. Copy this repository into your Claude Code skills directory:

   ```bash
   # Clone into your project's .claude/skills/ directory
   git clone https://github.com/xchenliu/ai-data-analysis-skill.git .claude/skills/data-analysis
   ```

2. Then in Claude Code, simply ask:
   - "Analyze this CSV file"
   - "Create a bar chart from sales.csv"
   - "Run EDA on my dataset"

### Standalone Usage

The scripts can also be used independently without Claude Code:

```bash
# Auto EDA - generates report + charts
python scripts/auto_eda.py your_data.csv --outdir eda_output

# Auto EDA + export to Word
python scripts/auto_eda.py your_data.csv --word

# Auto EDA + export to PDF
python scripts/auto_eda.py your_data.csv --pdf

# Load and inspect data
python scripts/load_data.py your_data.csv

# Find available Chinese font
python scripts/find_chinese_font.py
```

## Scripts Overview

### `auto_eda.py` - Automated EDA Pipeline

Runs a complete exploratory analysis on any dataset:
- Infers column types (numeric, categorical, datetime, id-like)
- Generates histograms for numeric columns
- Creates bar charts for top categories
- Plots time trends if datetime columns exist
- Builds correlation heatmap
- Detects outliers via IQR method
- Produces a bilingual markdown report with embedded charts
- Exports to Word (.docx) or PDF

```python
from scripts.auto_eda import run, export_to_word, export_to_pdf

# Generate markdown report + charts
report_path = run("sales.csv", outdir="eda_output")

# Export to Word
export_to_word(report_path, outdir="eda_output")

# Export to PDF (requires docx2pdf or LibreOffice)
export_to_pdf(report_path, outdir="eda_output")
```

### `load_data.py` - Smart Data Loader

Handles multiple file formats and encoding issues automatically:

```python
from scripts.load_data import load_data, inspect_data
df = load_data("data.csv")     # Auto-detects encoding (UTF-8, GBK, GB2312, etc.)
inspect_data(df)                # Prints shape, types, missing values, statistics
```

### `quick_chart.py` - One-Line Chart Generation

```python
from scripts.quick_chart import create_bar_chart, create_line_chart, create_pie_chart

create_bar_chart(df, x_col="category", y_col="sales", title="Sales by Category", output="bar.png")
create_line_chart(df, x_col="month", y_col="revenue", title="Monthly Revenue", output="line.png")
create_pie_chart(df, label_col="region", value_col="count", title="Region Distribution", output="pie.png")
```

### `find_chinese_font.py` - Chinese Font Detector

Automatically finds a suitable Chinese font on the current system:

```python
from scripts.find_chinese_font import find_chinese_font
font = find_chinese_font()  # Returns FontProperties or None
```

Searches common paths on Windows (`msyh.ttc`, `simhei.ttf`), Linux (`NotoSansCJK`), and macOS (`PingFang.ttc`).

## Color Palettes

Pre-defined palettes available in `assets/color_palettes.json`:

| Palette     | Colors                                                       |
|-------------|--------------------------------------------------------------|
| `vibrant`   | Red, Blue, Green, Orange, Purple                             |
| `warm`      | Red, Orange, Amber, Yellow                                   |
| `cool`      | Blue, Green, Teal, Dark Teal                                 |
| `corporate` | Dark Navy, Gray tones                                        |
| `pastel`    | Soft Pink, Green, Blue, Yellow, Purple                       |
| `ocean`     | Deep Blue, Turquoise, Cerulean                               |
| `earth`     | Brown, Tan, Beige tones                                      |

## Dependencies

```bash
pip install -r requirements.txt
```

Core: `pandas`, `matplotlib`, `seaborn`, `openpyxl`, `pyarrow`, `tabulate`

Optional for Word/PDF export: `python-docx`, `docx2pdf` (or LibreOffice)

## License

MIT License - see [LICENSE](LICENSE) for details.
