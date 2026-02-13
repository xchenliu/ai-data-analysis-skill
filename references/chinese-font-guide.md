# Chinese Font Configuration Guide

Comprehensive guide for displaying Chinese characters correctly in matplotlib charts.

## Problem

Chinese characters display as boxes or garbled text in matplotlib when no Chinese font is configured.

## Solution: FontProperties (Recommended)

Use `FontProperties` to explicitly load a Chinese font file. This is the most reliable method.

### Linux Font Path

```python
import matplotlib.font_manager as fm
chinese_font = fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
```

### Windows Font Paths

```python
# Microsoft YaHei (most common)
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

# SimSun
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc')

# SimHei
chinese_font = fm.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')
```

### macOS Font Paths

```python
# PingFang SC
chinese_font = fm.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

# Hiragino Sans GB
chinese_font = fm.FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')
```

## Applying Font to ALL Text Elements

Every text element must have `fontproperties` set explicitly:

```python
# Axis labels
ax.set_xlabel('X轴标签', fontproperties=chinese_font)
ax.set_ylabel('Y轴标签', fontproperties=chinese_font)

# Title
ax.set_title('图表标题', fontproperties=chinese_font)

# Tick labels (often forgotten!)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(chinese_font)

# Legend
ax.legend(prop=chinese_font)

# Text annotations
ax.text(x, y, '注释文字', fontproperties=chinese_font)

# Pie chart labels
for text in texts + autotexts:
    text.set_fontproperties(chinese_font)
```

## Alternative: Global Font Setting

Less reliable but simpler for quick use:

```python
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

**Note:** This method may not work in all environments. Prefer `FontProperties` for reliable results.

## Auto-Detect Font Path

Detect available Chinese fonts on the current system:

```python
import matplotlib.font_manager as fm
import os

def find_chinese_font():
    """Find a Chinese font on the current system."""
    candidates = [
        # Linux
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        # Windows
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/simsun.ttc',
        # macOS
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
    ]
    for path in candidates:
        if os.path.exists(path):
            return fm.FontProperties(fname=path)
    # Fallback: search system fonts
    for font in fm.findSystemFonts():
        if any(name in font.lower() for name in ['yahei', 'simhei', 'simsun', 'noto', 'pingfang', 'cjk']):
            return fm.FontProperties(fname=font)
    return None

chinese_font = find_chinese_font()
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Forgot tick labels | Always set `fontproperties` on `get_xticklabels()` and `get_yticklabels()` |
| Minus sign displays incorrectly | Set `plt.rcParams['axes.unicode_minus'] = False` |
| Font file not found | Use `find_chinese_font()` auto-detection function |
| Pie chart text garbled | Apply font to both `texts` and `autotexts` from `ax.pie()` |
| Legend text garbled | Use `prop=chinese_font` in `ax.legend()` |
