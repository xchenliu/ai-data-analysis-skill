"""Load data files with automatic encoding detection and format handling."""

import pandas as pd


def load_data(filepath):
    """Load a data file into a DataFrame with automatic format and encoding detection.

    Supports: CSV, Excel (.xlsx/.xls), JSON, Parquet.

    Args:
        filepath: Path to the data file.

    Returns:
        pandas DataFrame.

    Raises:
        ValueError: If file format is not supported.
    """
    ext = filepath.rsplit('.', 1)[-1].lower()

    if ext == 'csv':
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']
        for enc in encodings:
            try:
                return pd.read_csv(filepath, encoding=enc)
            except (UnicodeDecodeError, UnicodeError):
                continue
        raise ValueError(f"Cannot decode CSV file with encodings: {encodings}")

    elif ext in ('xlsx', 'xls'):
        return pd.read_excel(filepath)

    elif ext == 'json':
        encodings = ['utf-8', 'gbk']
        for enc in encodings:
            try:
                return pd.read_json(filepath, encoding=enc)
            except (UnicodeDecodeError, ValueError):
                continue
        raise ValueError("Cannot decode JSON file.")

    elif ext == 'parquet':
        return pd.read_parquet(filepath)

    else:
        raise ValueError(f"Unsupported file format: .{ext}")


def inspect_data(df):
    """Print a concise summary of the DataFrame."""
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nColumn types:\n{df.dtypes}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python load_data.py <filepath>")
        sys.exit(1)
    df = load_data(sys.argv[1])
    inspect_data(df)
