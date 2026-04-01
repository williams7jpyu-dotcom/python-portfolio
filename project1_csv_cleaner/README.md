# Sales CSV Cleaner / 売上CSVクレンジングツール

An automated data quality pipeline that cleanses sales CSV files by removing duplicates, null values, and invalid records, then exports summary charts.

売上データCSVに含まれる **重複行・欠損値・不正値** をPandasで一括クレンジングし、整形済みファイルとグラフを出力する業務自動化スクリプトです。

---

## Features / 機能

| Step | Description |
|------|-------------|
| Deduplication | Remove rows where all columns are identical |
| Null removal | Drop rows where `amount` cannot be parsed as a number |
| Invalid value filter | Exclude rows where `amount ≤ 0` |
| Normalization | Strip whitespace from `customer`; lowercase `category` |
| Column reorder | `order_id → date → customer → category → amount` |
| Date sort | Sort ascending by `date` |
| Visualization | Bar chart (sales by category) + line chart (daily trend) |

## Requirements / 動作環境

- Python 3.11+

## Setup / セットアップ

```bash
cd project1_csv_cleaner
pip install -r requirements.txt
```

## Usage / 使い方

```bash
# Cleanse CSV / CSVクレンジング
python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv

# Generate charts / グラフ生成
python src/visualize.py --input data/sales_cleaned.csv --output output/
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input CSV path | `data/sales_sample.csv` |
| `--output` | Output path | `data/sales_cleaned.csv` |

## Demo Output / 実行例

```
INFO: 読み込み完了: 8行
INFO: 重複削除: 2行削除
INFO: 欠損値(amount)除外後: 5行
INFO: 不正値除外: 1行削除
INFO: クレンジング完了: 4行

=== クレンジング結果サマリー ===
 order_id       date  customer   category  amount
      001 2024-01-10  田中太郎       food  1500.0
      005 2024-01-13  山田次郎   clothing  2800.0
      002 2024-01-11  鈴木花子  electronics  3200.0
      008 2024-01-15  伊藤四郎  electronics  4100.0
```

Charts saved to `output/`:
- `category_sales.png` — Bar chart of total sales per category
- `daily_sales.png`    — Line chart of daily sales trend

## Running Tests / テスト実行

```bash
pytest tests/ -v
```

## Directory Structure / ディレクトリ構成

```
project1_csv_cleaner/
├── data/
│   ├── sales_sample.csv     # Input sample (8 rows with quality issues)
│   └── sales_cleaned.csv    # Output (generated after running cleaner.py)
├── src/
│   ├── cleaner.py           # Cleansing pipeline
│   └── visualize.py         # Chart generation
├── tests/
│   └── test_cleaner.py      # 9 unit tests (pytest)
├── output/                  # Generated charts (.gitignored)
├── conftest.py
├── requirements.txt
└── README.md
```

## Implementation Notes / 実装のポイント

- `pd.to_numeric(errors="coerce")` で文字列混入にも安全に対応
- `str.strip()` と `str.lower()` で表記ゆれを正規化
- `argparse` でパスをCLI引数化し、ハードコーディングを排除
- `logging` で各ステップの削除件数を可視化
- `matplotlib.use("Agg")` でGUI不要のサーバー環境にも対応
