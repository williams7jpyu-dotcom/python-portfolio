"""
PDF テキスト抽出ツール

処理内容:
- pdfplumber でPDFからテキスト行を抽出
- 指定キーワード（大文字小文字を無視）にマッチした行をフィルタリング
- 複数キーワード対応（いずれかに一致する行を抽出）
- ページ番号・行番号・テキストをExcel（.xlsx）に出力

使い方:
    # 単一キーワード
    python src/extractor.py --pdf data/sample.pdf --keyword ERROR --output data/result.xlsx

    # 複数キーワード（スペース区切り）
    python src/extractor.py --pdf data/sample.pdf --keyword ERROR WARNING --output data/result.xlsx
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
import pdfplumber  # pip install pdfplumber

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def extract_lines(pdf_path: str, keywords: list[str]) -> list[dict]:
    """PDFを開き、いずれかのキーワードを含む行を抽出して返す。

    大文字小文字を無視してマッチングを行う。

    Args:
        pdf_path: 入力PDFファイルのパス。
        keywords: 検索キーワードのリスト（OR 条件で検索）。

    Returns:
        マッチした行の情報を含む辞書のリスト。
        各辞書は {"page": int, "line_num": int, "text": str} の形式。
    """
    results = []
    lower_keywords = [kw.lower() for kw in keywords]

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        logging.info(f"ページ数: {total_pages}")
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            for line_num, line in enumerate(text.split("\n"), start=1):
                if any(kw in line.lower() for kw in lower_keywords):
                    results.append({
                        "page": page_num,
                        "line_num": line_num,
                        "text": line.strip(),
                    })

    logging.info(f"マッチ行数: {len(results)}")
    if not results:
        logging.warning("キーワードに一致する行が見つかりませんでした。")
    return results


def save_to_excel(records: list[dict], output_path: str) -> None:
    """抽出結果をExcelファイルに保存する。

    出力先ディレクトリが存在しない場合は自動生成する。

    Args:
        records: extract_lines() の戻り値（辞書のリスト）。
        output_path: 出力先 .xlsx ファイルのパス。
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="抽出結果")
    logging.info(f"Excel出力完了: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF行抽出ツール")
    parser.add_argument("--pdf",     required=True, help="入力PDFのパス")
    parser.add_argument(
        "--keyword",
        required=True,
        nargs="+",
        help="抽出対象キーワード（スペース区切りで複数指定可）",
    )
    parser.add_argument("--output",  default="data/result.xlsx", help="出力Excelのパス")
    args = parser.parse_args()

    if not Path(args.pdf).exists():
        logging.error(f"PDFファイルが見つかりません: {args.pdf}")
        return

    records = extract_lines(args.pdf, args.keyword)
    if not records:
        print("マッチする行が見つかりませんでした。")
        return
    save_to_excel(records, args.output)
    print(f"完了: {len(records)}行を {args.output} に保存しました。")


if __name__ == "__main__":
    main()
