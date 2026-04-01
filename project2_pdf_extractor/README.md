# PDF Text Extractor / PDFテキスト抽出ツール

A CLI tool that scans PDF files for lines matching specified keywords and exports the results — including page number, line number, and text — to an Excel spreadsheet.

PDFファイルから **指定キーワードを含む行** を抽出し、ページ番号・行番号・テキストをExcel（.xlsx）に出力するCLIツールです。ログ解析や帳票からの情報収集の自動化を想定しています。

---

## Features / 機能

- Case-insensitive keyword matching（大文字小文字を無視したマッチング）
- Multiple keyword support with OR logic（複数キーワードをOR条件で検索）
- Records page number and line number for easy cross-reference（元PDFとの照合が容易）
- Outputs to Excel with a dedicated sheet（Excelの専用シートに出力）

## Requirements / 動作環境

- Python 3.11+

## Setup / セットアップ

```bash
cd project2_pdf_extractor
pip install -r requirements.txt
```

## Usage / 使い方

```bash
# Single keyword / 単一キーワード
python src/extractor.py --pdf data/sample.pdf --keyword ERROR --output data/result.xlsx

# Multiple keywords (OR) / 複数キーワード（スペース区切り）
python src/extractor.py --pdf data/sample.pdf --keyword ERROR WARNING --output data/result.xlsx
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--pdf` | Input PDF path | required |
| `--keyword` | Keyword(s) to search (space-separated) | required |
| `--output` | Output Excel path | `data/result.xlsx` |

## Demo Output / 実行例

```
INFO: ページ数: 3
INFO: マッチ行数: 4
完了: 4行を data/result.xlsx に保存しました。
```

Output Excel (`sheet: 抽出結果`):

| page | line_num | text |
|------|----------|------|
| 1 | 5 | ERROR: connection timeout |
| 2 | 12 | WARNING: retry limit reached |
| 3 | 3 | ERROR: disk write failed |

## Running Tests / テスト実行

```bash
pytest tests/ -v
```

## Directory Structure / ディレクトリ構成

```
project2_pdf_extractor/
├── data/
│   ├── sample.pdf           # Test PDF
│   └── result.xlsx          # Output (generated after running extractor.py)
├── src/
│   └── extractor.py         # Extraction logic
├── tests/
│   └── test_extractor.py    # 6 unit tests (pytest + unittest.mock)
├── conftest.py
├── requirements.txt
└── README.md
```

## Implementation Notes / 実装のポイント

- `pdfplumber` の `extract_text()` は複雑な文字コードのPDFでも比較的安定
- `any(kw in line.lower() for kw in keywords)` で複数キーワードをOR検索
- `unittest.mock.patch` でpdfplumberをモック化し、実PDFに依存しないテストを実現
- `argparse` の `nargs="+"` で複数キーワードをスペース区切りで受け取る設計
