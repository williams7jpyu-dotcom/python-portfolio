"""Unit tests for cleaner.py"""

import pandas as pd
import pytest
from pathlib import Path

from cleaner import clean, load_csv, save_csv


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_df() -> pd.DataFrame:
    """クレンジング処理の動作確認に使う「汚れた」DataFrameを返す。

    含まれる問題:
      - 行0と行2は全列一致の重複 → 重複削除で行2を除去
      - 行3: amount = NaN          → dropna で除去
      - 行4: amount = -50          → 不正値フィルタで除去
      - 行5: customer に前後空白    → strip で除去
      - 行1: category が大文字混じり → lower() で正規化

    クレンジング後の残存行: 行0（001）, 行1（002）, 行5（005） = 3行
    """
    return pd.DataFrame({
        "order_id": ["001", "002", "001", "003", "004", "005"],
        "customer":  ["Alice", "Bob", "Alice", "Charlie", "Dave", " Eve "],
        "amount":    [100.0, 200.0, 100.0, float("nan"), -50.0, 300.0],
        "date": [
            "2024-01-02", "2024-01-01", "2024-01-02",
            "2024-01-03", "2024-01-04", "2024-01-05",
        ],
        "category": ["food", "Electronics", "food", "clothing", "food", "food"],
    })


# ── clean() tests ─────────────────────────────────────────────────────────────

def test_drop_duplicates(sample_df: pd.DataFrame) -> None:
    """全列一致の重複行が除去されること。"""
    result = clean(sample_df.copy())
    assert result.duplicated().sum() == 0


def test_remove_nan_amount(sample_df: pd.DataFrame) -> None:
    """amount が NaN の行が除去されること。"""
    result = clean(sample_df.copy())
    assert result["amount"].isna().sum() == 0


def test_remove_negative_amount(sample_df: pd.DataFrame) -> None:
    """amount が 0 以下の行が除去されること。"""
    result = clean(sample_df.copy())
    assert (result["amount"] <= 0).sum() == 0


def test_output_row_count(sample_df: pd.DataFrame) -> None:
    """重複1件・NaN1件・負値1件が除去され、3行が残ること。"""
    result = clean(sample_df.copy())
    assert len(result) == 3


def test_sort_by_date(sample_df: pd.DataFrame) -> None:
    """date 列が昇順ソートされること。"""
    result = clean(sample_df.copy())
    dates = result["date"].tolist()
    assert dates == sorted(dates)


def test_column_order(sample_df: pd.DataFrame) -> None:
    """出力列の順序が [order_id, date, customer, category, amount] であること。"""
    result = clean(sample_df.copy())
    assert list(result.columns) == ["order_id", "date", "customer", "category", "amount"]


def test_strip_customer_whitespace(sample_df: pd.DataFrame) -> None:
    """customer 列の前後空白が除去されること。"""
    result = clean(sample_df.copy())
    for name in result["customer"]:
        assert name == name.strip()


def test_normalize_category(sample_df: pd.DataFrame) -> None:
    """category 列が小文字に統一されること。"""
    result = clean(sample_df.copy())
    for cat in result["category"]:
        assert cat == cat.lower()


# ── save_csv() / load_csv() round-trip tests ─────────────────────────────────

def test_save_and_reload(sample_df: pd.DataFrame, tmp_path: Path) -> None:
    """保存したCSVを再読み込みしても行数が一致すること。"""
    df_clean = clean(sample_df.copy())
    out = str(tmp_path / "out.csv")
    save_csv(df_clean, out)
    assert Path(out).exists()
    reloaded = load_csv(out)
    assert len(reloaded) == len(df_clean)
