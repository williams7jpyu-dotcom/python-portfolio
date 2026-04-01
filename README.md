# Python Portfolio

A collection of three practical Python automation tools built for real-world data workflows.

| Project | Description | Stack |
|---------|-------------|-------|
| [Sales CSV Cleaner](project1_csv_cleaner/) | Data quality pipeline for sales records | pandas, matplotlib |
| [PDF Text Extractor](project2_pdf_extractor/) | Keyword-based line extraction from PDF files | pdfplumber, openpyxl |
| [Hacker News Scraper](project3_scraper/) | CLI web scraper with keyword filtering | requests, BeautifulSoup4 |

## Requirements

- Python 3.11+

## Quick Start

```bash
# Project 1 — Sales CSV Cleaner
cd project1_csv_cleaner
pip install -r requirements.txt
python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv
python src/visualize.py --input data/sales_cleaned.csv --output output/

# Project 2 — PDF Text Extractor
cd project2_pdf_extractor
pip install -r requirements.txt
python src/extractor.py --pdf data/sample.pdf --keyword ERROR --output data/result.xlsx

# Project 3 — Hacker News Scraper
cd project3_scraper
pip install -r requirements.txt
python src/scraper.py --keyword python --pages 2
```

## Running Tests

Each project ships with unit tests. Run them from the respective project directory:

```bash
cd project1_csv_cleaner && pytest tests/ -v
cd project2_pdf_extractor && pytest tests/ -v
cd project3_scraper && pytest tests/ -v
```

---

# Python ポートフォリオ

実務で活用できる3つのPython自動化ツールをまとめたポートフォリオです。

| プロジェクト | 概要 | 使用技術 |
|------------|------|---------|
| [売上CSVクレンジング](project1_csv_cleaner/) | 売上データの品質管理パイプライン | pandas, matplotlib |
| [PDFテキスト抽出](project2_pdf_extractor/) | PDFからキーワード行を抽出しExcelへ出力 | pdfplumber, openpyxl |
| [Hacker Newsスクレイパー](project3_scraper/) | キーワードフィルタ付きWebスクレイパー | requests, BeautifulSoup4 |

## 動作環境

- Python 3.11+

## セットアップ & 実行

```bash
# プロジェクト1 — 売上CSVクレンジング
cd project1_csv_cleaner
pip install -r requirements.txt
python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv
python src/visualize.py --input data/sales_cleaned.csv --output output/

# プロジェクト2 — PDFテキスト抽出
cd project2_pdf_extractor
pip install -r requirements.txt
python src/extractor.py --pdf data/sample.pdf --keyword エラー --output data/result.xlsx

# プロジェクト3 — Hacker Newsスクレイパー
cd project3_scraper
pip install -r requirements.txt
python src/scraper.py --keyword python --pages 2
```

## テスト実行

各プロジェクトディレクトリ内で実行してください:

```bash
cd project1_csv_cleaner && pytest tests/ -v
cd project2_pdf_extractor && pytest tests/ -v
cd project3_scraper && pytest tests/ -v
```
