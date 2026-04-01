# How to Run This Portfolio / 動かし方ガイド

This guide walks you through running each project step by step — no prior Python experience needed.

Pythonの経験がなくても迷わず動かせるよう、コマンドをそのままコピー＆ペーストできる形式で書いています。

---

## Table of Contents / 目次

1. [Prerequisites / 事前確認](#1-prerequisites--事前確認)
2. [Project 1 — Sales CSV Cleaner](#2-project-1--sales-csv-cleaner)
3. [Project 2 — PDF Text Extractor](#3-project-2--pdf-text-extractor)
4. [Project 3 — Hacker News Scraper](#4-project-3--hacker-news-scraper)
5. [Running Tests / テスト実行](#5-running-tests--テスト実行)
6. [Troubleshooting / よくあるエラー](#6-troubleshooting--よくあるエラー)

---

## 1. Prerequisites / 事前確認

### Open a terminal / ターミナルを開く

**Windows:** `Windows キー + R` → `cmd` と入力 → Enter

**Mac / Linux:** アプリケーション一覧から「ターミナル」を開く

---

### Check Python version / Pythonのバージョン確認

```bash
python --version
```

`Python 3.11` 以上が表示されれば OK です。

> Mac / Linux では `python3 --version` を使ってください。

---

## 2. Project 1 — Sales CSV Cleaner

### What it does / 何をするか

`data/sales_sample.csv`（8行の問題あり売上データ）を読み込み、重複・欠損・不正値を自動除去してクレンジング済みCSVを出力します。さらにグラフ画像も生成します。

### Move to the project folder / フォルダに移動

```bash
cd project1_csv_cleaner
```

> はじめてこのリポジトリを開いた場合は、先にルートフォルダへ移動してください。
> ```bash
> cd path/to/python_portfolio
> ```

### Install dependencies / ライブラリのインストール

```bash
pip install -r requirements.txt
```

> 「Already satisfied」と出ても問題ありません（すでにインストール済みの意味）。

### Step 1: Run the cleaner / クレンジング実行

```bash
python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv
```

**Expected output / 実行例:**
```
INFO: 読み込み完了: 8行
INFO: 重複削除: 2行削除
INFO: 欠損値(amount)除外後: 5行
INFO: 不正値除外: 1行削除
INFO: クレンジング完了: 4行

=== クレンジング結果サマリー ===
 order_id       date  customer   category  amount
      001 2024-01-10   田中太郎       food  1500.0
      ...
```

`data/sales_cleaned.csv` が生成されていれば成功です。

### Step 2: Generate charts / グラフ生成

```bash
python src/visualize.py --input data/sales_cleaned.csv --output output/
```

**Expected output / 実行例:**
```
INFO: 棒グラフ保存: output\category_sales.png
INFO: 折れ線グラフ保存: output\daily_sales.png
完了: グラフを output/ に保存しました。
```

`output/` フォルダに以下の2ファイルが生成されます。

| ファイル | 内容 |
|---------|------|
| `category_sales.png` | カテゴリ別売上合計の棒グラフ |
| `daily_sales.png` | 日別売上推移の折れ線グラフ |

---

## 3. Project 2 — PDF Text Extractor

### What it does / 何をするか

PDFファイルを読み込み、指定したキーワードを含む行を抽出して、ページ番号・行番号・テキストをExcel（`.xlsx`）に出力します。

### Move to the project folder / フォルダに移動

```bash
cd ../project2_pdf_extractor
```

> はじめてこのリポジトリを開いた場合:
> ```bash
> cd path/to/python_portfolio/project2_pdf_extractor
> ```

### Install dependencies / ライブラリのインストール

```bash
pip install -r requirements.txt
```

### Run the extractor / 抽出を実行

#### Single keyword / 単一キーワード

```bash
python src/extractor.py --pdf data/sample.pdf --keyword ERROR --output data/result.xlsx
```

#### Multiple keywords (OR search) / 複数キーワード（スペース区切り）

```bash
python src/extractor.py --pdf data/sample.pdf --keyword ERROR WARNING --output data/result.xlsx
```

**Expected output / 実行例:**
```
INFO: ページ数: 2
INFO: マッチ行数: 4
INFO: Excel出力完了: data/result.xlsx
完了: 4行を data/result.xlsx に保存しました。
```

`data/result.xlsx` をExcelで開くと以下の形式で結果が確認できます。

| page | line_num | text |
|------|----------|------|
| 1 | 4 | `ERROR  Connection timeout: api.example.com` |
| 2 | 2 | `ERROR  File not found: /data/input/sales_2024.csv` |
| ... | ... | ... |

### Use your own PDF / 自分のPDFで試す

```bash
python src/extractor.py --pdf (PDFのパス) --keyword (キーワード) --output data/result.xlsx
```

**Example:**
```bash
python src/extractor.py --pdf ~/Documents/report.pdf --keyword 売上 --output data/result.xlsx
```

> **Note:** テキストを含まないスキャンPDF（画像PDF）は抽出できません。

---

## 4. Project 3 — Hacker News Scraper

### What it does / 何をするか

海外技術ニュースサイト [Hacker News](https://news.ycombinator.com) のトップ記事（タイトル・URL・スコア）をリアルタイムで取得し、CSVファイルに保存します。

> **Note:** インターネット接続が必要です。

### Move to the project folder / フォルダに移動

```bash
cd ../project3_scraper
```

### Install dependencies / ライブラリのインストール

```bash
pip install -r requirements.txt
```

### Run the scraper / スクレイピング実行

#### Fetch all articles (1 page, ~30 items) / 全記事を1ページ取得

```bash
python src/scraper.py
```

#### Filter by keyword / キーワードで絞り込む

```bash
python src/scraper.py --keyword python
```

#### Fetch multiple pages / 複数ページ取得

```bash
python src/scraper.py --pages 3
```

#### All options combined / オプション組み合わせ例

```bash
python src/scraper.py --keyword python --pages 2 --output output/python_news.csv
```

**Expected output / 実行例:**
```
INFO: 取得中: https://news.ycombinator.com
INFO:   → 30件取得
INFO: CSV出力完了: output/hn_articles.csv (30件)
INFO: 合計: 1ページから 30件取得
完了: 30件を output/hn_articles.csv に保存しました。
```

`output/hn_articles.csv` をExcelやメモ帳で開くと記事一覧が確認できます。

| title | url | score | scraped_at |
|-------|-----|-------|------------|
| 記事タイトル | https://... | 312 | 2024-01-15 12:00:00 |

### Options / オプション一覧

| Option | Description | Default |
|--------|-------------|---------|
| `--keyword` | Filter keyword (case-insensitive) | *(none — fetch all)* |
| `--pages` | Number of pages to fetch | `1` |
| `--output` | Output CSV path | `output/hn_articles.csv` |

---

## 5. Running Tests / テスト実行

各プロジェクトに自動テストが含まれています。以下のコマンドでコードが正しく動くかを確認できます。

```bash
# Project 1
cd project1_csv_cleaner
python -m pytest tests/ -v

# Project 2
cd ../project2_pdf_extractor
python -m pytest tests/ -v

# Project 3
cd ../project3_scraper
python -m pytest tests/ -v
```

**Successful output / 正常な実行例:**
```
============================= test session starts ==============================
collected 9 items

tests/test_cleaner.py::test_drop_duplicates          PASSED   [ 11%]
tests/test_cleaner.py::test_remove_nan_amount        PASSED   [ 22%]
tests/test_cleaner.py::test_remove_negative_amount   PASSED   [ 33%]
...

============================== 9 passed in 2.00s ==============================
```

`passed` がすべて緑色で表示されれば正常です。`FAILED` が表示された場合はコードに問題があります。

---

## 6. Troubleshooting / よくあるエラー

---

### `python` が認識されない

```
'python' は、内部コマンドまたは外部コマンドとして認識されていません。
```

→ `python3` に置き換えて実行してください。それでもダメな場合は Python がインストールされていません。[python.org](https://www.python.org/downloads/) からインストールしてください。

---

### `No module named '...'`

```
ModuleNotFoundError: No module named 'pandas'
```

→ そのプロジェクトフォルダで `pip install -r requirements.txt` を実行してください。

---

### Project 2 で `No /Root object!` エラー

```
PdfminerException: No /Root object! - Is this really a PDF?
```

→ 指定したPDFが壊れているか、空ファイルです。`data/sample.pdf` を使って試してください。

---

### Project 3 で「記事が見つかりませんでした」

→ 指定したキーワードに一致する記事がHacker Newsのトップページにない状態です。キーワードを変えるか、外して実行してください。

```bash
python src/scraper.py  # キーワードなし（全件取得）
```

---

### `cd` でフォルダが見つからない

```
指定されたパスが見つかりません。
```

→ このリポジトリをどこに保存したか確認してください。エクスプローラーで `python_portfolio` フォルダを右クリック →「パスのコピー」でパスを取得できます。

---

## Quick Reference / コマンド早見表

```bash
# --- Setup (one time) ---
cd path/to/python_portfolio

# --- Project 1 ---
cd project1_csv_cleaner
pip install -r requirements.txt
python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv
python src/visualize.py --input data/sales_cleaned.csv --output output/

# --- Project 2 ---
cd ../project2_pdf_extractor
pip install -r requirements.txt
python src/extractor.py --pdf data/sample.pdf --keyword ERROR --output data/result.xlsx

# --- Project 3 ---
cd ../project3_scraper
pip install -r requirements.txt
python src/scraper.py --keyword python --pages 1
```
