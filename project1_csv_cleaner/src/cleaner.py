"""
売上CSVクレンジングツール

処理内容:
- 重複行の削除
- 欠損値・不正値（amount <= 0）のドロップ
- customer 列の前後空白除去
- category 列の小文字正規化
- 列の並び替えと日付昇順ソート
- クレンジング済みファイルの出力

使い方:
    python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv
"""

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_csv(path: str) -> pd.DataFrame:
    """CSVファイルを読み込んでDataFrameを返す。

    Args:
        path: 入力CSVファイルのパス（UTF-8 BOM対応）。

    Returns:
        読み込んだDataFrame。
    """
    df = pd.read_csv(path, encoding="utf-8-sig")
    logging.info(f"読み込み完了: {len(df)}行")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """DataFrameに対して以下のクレンジングを順番に適用する。

    1. 全列一致の重複行を削除
    2. amount を数値変換し、変換不可（NaN）の行を除外
    3. amount が 0 以下の行を除外
    4. customer 列の前後空白を除去
    5. category 列を小文字に正規化
    6. 列順を [order_id, date, customer, category, amount] に整列
    7. date を datetime 型に変換して昇順ソート

    Args:
        df: クレンジング前のDataFrame。

    Returns:
        クレンジング済みのDataFrame（インデックスはリセット済み）。
    """
    original = len(df)

    # 1. 重複行を削除（全列一致）
    df = df.drop_duplicates()
    logging.info(f"重複削除: {original - len(df)}行削除")

    # 2. amount列を数値に変換し、変換できない行を除外
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    logging.info(f"欠損値(amount)除外後: {len(df)}行")

    # 3. 不正値（amountが0以下）を除外
    before = len(df)
    df = df[df["amount"] > 0]
    logging.info(f"不正値除外: {before - len(df)}行削除")

    # 4. customer 列の前後空白を除去
    df["customer"] = df["customer"].str.strip()

    # 5. category 列を小文字に正規化（表記ゆれ対策）
    df["category"] = df["category"].str.lower()

    # 6. 列の並び替え
    column_order = ["order_id", "date", "customer", "category", "amount"]
    df = df[column_order]

    # 7. dateを日付型に変換して昇順ソート
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    logging.info(f"クレンジング完了: {len(df)}行")
    return df


def save_csv(df: pd.DataFrame, output_path: str) -> None:
    """DataFrameをCSVファイルに保存する。

    出力先ディレクトリが存在しない場合は自動生成する。

    Args:
        df: 保存するDataFrame。
        output_path: 出力先CSVファイルのパス。
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    logging.info(f"出力完了: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="売上CSVクレンジングツール")
    parser.add_argument(
        "--input",
        default="data/sales_sample.csv",
        help="入力CSVファイルのパス（デフォルト: data/sales_sample.csv）",
    )
    parser.add_argument(
        "--output",
        default="data/sales_cleaned.csv",
        help="出力CSVファイルのパス（デフォルト: data/sales_cleaned.csv）",
    )
    args = parser.parse_args()

    df = load_csv(args.input)
    df_clean = clean(df)
    save_csv(df_clean, args.output)

    print("\n=== クレンジング結果サマリー ===")
    print(df_clean.to_string(index=False))


if __name__ == "__main__":
    main()
