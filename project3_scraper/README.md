# Hacker News Scraper / Hacker News 記事スクレイパー

A CLI web scraper that collects top articles from [Hacker News](https://news.ycombinator.com), with optional keyword filtering and multi-page support, and saves the results to CSV.

[Hacker News](https://news.ycombinator.com) のトップ記事を取得し、タイトル・URL・スコア・取得日時をCSVに保存するスクレイパーです。キーワードフィルタと複数ページ取得に対応しています。

---

## Features / 機能

- Keyword filtering with case-insensitive matching（大文字小文字を無視したキーワードフィルタ）
- Multi-page collection with polite crawl delay（複数ページ取得 + サーバー負荷軽減のwait）
- Numeric score field for easy sorting and aggregation（scoreを整数型で保存し集計が容易）
- Graceful error handling — skips unreachable pages without crashing（通信エラー時にクラッシュしない設計）

## Requirements / 動作環境

- Python 3.11+

## Setup / セットアップ

```bash
cd project3_scraper
pip install -r requirements.txt
```

## Usage / 使い方

```bash
# Fetch all articles (1 page) / 全記事を1ページ分取得
python src/scraper.py

# Filter by keyword / キーワードフィルタ
python src/scraper.py --keyword python

# Fetch multiple pages / 複数ページ取得
python src/scraper.py --pages 3

# Combine options / 複合使用例
python src/scraper.py --keyword python --pages 2 --output output/python_news.csv
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--keyword` | Filter keyword (case-insensitive) | *(none)* |
| `--pages` | Number of pages to fetch | `1` |
| `--output` | Output CSV path | `output/hn_articles.csv` |

## Demo Output / 実行例

```
INFO: 取得中: https://news.ycombinator.com
INFO:   → 28件取得
INFO: CSV出力完了: output/hn_articles.csv (28件)
INFO: 合計: 1ページから 28件取得
完了: 28件を output/hn_articles.csv に保存しました。
```

Output CSV columns:

| Column | Type | Description |
|--------|------|-------------|
| `title` | str | Article title |
| `url` | str | Article URL (absolute) |
| `score` | int | Upvote count |
| `scraped_at` | str | Timestamp (`YYYY-MM-DD HH:MM:SS`) |

## Running Tests / テスト実行

```bash
pytest tests/ -v
```

## Directory Structure / ディレクトリ構成

```
project3_scraper/
├── src/
│   └── scraper.py           # Scraping logic
├── tests/
│   └── test_scraper.py      # 6 unit tests (pytest + unittest.mock)
├── output/
│   ├── hn_articles.csv      # Output (generated after running scraper.py)
│   └── .gitkeep
├── conftest.py
├── requirements.txt
└── README.md
```

## Implementation Notes / 実装のポイント

- `time.sleep(1)` で複数ページ取得時にサーバー負荷を軽減（マナー対策）
- `User-Agent` ヘッダーにポートフォリオ用スクレイパーと明記
- `try/except requests.RequestException` で通信エラーをキャッチ（クラッシュしない）
- `score` を `int` 型で保存し、CSVでの集計・ソートを容易に
- `unittest.mock.patch` でHTTPリクエストをモック化し、ネットワーク不要のテストを実現
