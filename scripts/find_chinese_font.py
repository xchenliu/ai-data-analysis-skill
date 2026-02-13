"""Auto-detect and load a Chinese font for matplotlib on any OS."""

import os
import matplotlib.font_manager as fm


def find_chinese_font():
    """Find a Chinese font available on the current system.

    Returns:
        FontProperties object or None if no Chinese font found.
    """
    candidates = [
        # Windows
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/msyhbd.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/simsun.ttc',
        # Linux
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        # macOS
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
    ]

    for path in candidates:
        if os.path.exists(path):
            return fm.FontProperties(fname=path)

    # Fallback: search system fonts by keyword
    keywords = ['yahei', 'simhei', 'simsun', 'noto', 'pingfang', 'cjk',
                'wqy', 'heiti', 'songti', 'fangsong']
    for font_path in fm.findSystemFonts():
        if any(kw in font_path.lower() for kw in keywords):
            return fm.FontProperties(fname=font_path)

    return None


if __name__ == '__main__':
    font = find_chinese_font()
    if font:
        print(f"Found Chinese font: {font.get_file()}")
    else:
        print("No Chinese font found on this system.")
