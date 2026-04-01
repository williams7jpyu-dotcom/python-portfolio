"""
売上データ可視化ツール

cleaner.py で生成したクレンジング済みCSVを読み込み、
2種類のグラフを PNG として出力する。

  1. カテゴリ別売上合計  棒グラフ  → output/category_sales.png
  2. 日別売上推移        折れ線グラフ → output/daily_sales.png

使い方:
    # cleaner.py でCSVを生成してから実行
    python src/cleaner.py --input data/sales_sample.csv --output data/sales_cleaned.csv
    python src/visualize.py --input data/sales_cleaned.csv --output output/
"""

import argparse
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # GUI不要のバックエンド（サーバー・CI環境対応）
import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

_COLOR = "#4C72B0"


def load_cleaned_csv(path: str) -> pd.DataFrame:
    """クレンジング済みCSVを読み込み、date 列を datetime 型に変換して返す。

    Args:
        path: クレンジング済みCSVファイルのパス。

    Returns:
        date 列が datetime64 型の DataFrame。
    """
    df = pd.read_csv(path, encoding="utf-8-sig", parse_dates=["date"])
    logging.info(f"読み込み完了: {len(df)}行")
    return df


def plot_category_sales(df: pd.DataFrame, output_dir: str) -> None:
    """カテゴリ別売上合計を棒グラフで保存する。

    Args:
        df: クレンジング済み DataFrame（category / amount 列が必要）。
        output_dir: PNG ファイルの保存先ディレクトリ。
    """
    totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(totals.index, totals.values, color=_COLOR, edgecolor="white", width=0.6)

    ax.bar_label(
        bars,
        labels=[f"¥{v:,.0f}" for v in totals.values],
        padding=4,
        fontsize=10,
    )
    ax.set_title("Sales by Category", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Category", fontsize=11)
    ax.set_ylabel("Total Amount (JPY)", fontsize=11)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"¥{x:,.0f}")
    )
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    out_path = Path(output_dir) / "category_sales.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logging.info(f"棒グラフ保存: {out_path}")


def plot_daily_sales(df: pd.DataFrame, output_dir: str) -> None:
    """日別売上推移を折れ線グラフで保存する。

    Args:
        df: クレンジング済み DataFrame（date / amount 列が必要）。
        output_dir: PNG ファイルの保存先ディレクトリ。
    """
    daily = df.groupby("date")["amount"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        daily["date"],
        daily["amount"],
        marker="o",
        linewidth=2,
        color=_COLOR,
        markersize=7,
        markerfacecolor="white",
        markeredgewidth=2,
    )
    ax.fill_between(daily["date"], daily["amount"], alpha=0.12, color=_COLOR)

    ax.set_title("Daily Sales Trend", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Total Amount (JPY)", fontsize=11)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"¥{x:,.0f}")
    )
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    out_path = Path(output_dir) / "daily_sales.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logging.info(f"折れ線グラフ保存: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="売上データ可視化ツール")
    parser.add_argument(
        "--input",
        default="data/sales_cleaned.csv",
        help="クレンジング済みCSVのパス（デフォルト: data/sales_cleaned.csv）",
    )
    parser.add_argument(
        "--output",
        default="output/",
        help="グラフ保存先ディレクトリ（デフォルト: output/）",
    )
    args = parser.parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)

    df = load_cleaned_csv(args.input)
    plot_category_sales(df, args.output)
    plot_daily_sales(df, args.output)

    print(f"完了: グラフを {args.output} に保存しました。")


if __name__ == "__main__":
    main()
