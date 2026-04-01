"""Unit tests for extractor.py"""

import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from extractor import extract_lines, save_to_excel


# ── helpers ───────────────────────────────────────────────────────────────────

def make_mock_pdf(pages_text: list[str]) -> MagicMock:
    """pdfplumber.open() が返すコンテキストマネージャをモック化する。

    Args:
        pages_text: ページごとのテキスト文字列のリスト。

    Returns:
        with 文で使える MagicMock オブジェクト。
    """
    mock_pdf = MagicMock()
    mock_pages = []
    for text in pages_text:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = text
        mock_pages.append(mock_page)
    mock_pdf.pages = mock_pages
    mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
    mock_pdf.__exit__ = MagicMock(return_value=False)
    return mock_pdf


# ── extract_lines() tests ─────────────────────────────────────────────────────

@patch("extractor.pdfplumber.open")
def test_extract_lines_with_match(mock_open: MagicMock) -> None:
    """キーワードを含む行が抽出されること。"""
    mock_open.return_value = make_mock_pdf(["Line one\nError occurred\nLine three"])
    results = extract_lines("dummy.pdf", ["error"])
    assert len(results) == 1
    assert "Error" in results[0]["text"]


@patch("extractor.pdfplumber.open")
def test_extract_lines_no_match(mock_open: MagicMock) -> None:
    """一致しないキーワードで空リストが返ること。"""
    mock_open.return_value = make_mock_pdf(["Normal line\nAnother line"])
    results = extract_lines("dummy.pdf", ["notfound"])
    assert results == []


@patch("extractor.pdfplumber.open")
def test_case_insensitive_match(mock_open: MagicMock) -> None:
    """大文字小文字を無視してマッチすること。"""
    mock_open.return_value = make_mock_pdf(["ERROR: system failure\nNormal line"])
    results = extract_lines("dummy.pdf", ["error"])
    assert len(results) == 1


@patch("extractor.pdfplumber.open")
def test_page_number_recorded(mock_open: MagicMock) -> None:
    """ページ番号が正しく記録されること。"""
    mock_open.return_value = make_mock_pdf(
        ["No match here", "Target keyword found"]
    )
    results = extract_lines("dummy.pdf", ["keyword"])
    assert results[0]["page"] == 2


@patch("extractor.pdfplumber.open")
def test_multiple_keywords(mock_open: MagicMock) -> None:
    """複数キーワードのいずれかに一致する行が抽出されること（OR 条件）。"""
    mock_open.return_value = make_mock_pdf(
        ["Error happened\nWarning issued\nNormal line"]
    )
    results = extract_lines("dummy.pdf", ["error", "warning"])
    assert len(results) == 2


# ── save_to_excel() tests ─────────────────────────────────────────────────────

def test_save_to_excel_columns(tmp_path: Path) -> None:
    """出力 Excel に page, line_num, text 列が存在すること。"""
    records = [{"page": 1, "line_num": 3, "text": "sample line"}]
    out = str(tmp_path / "result.xlsx")
    save_to_excel(records, out)
    df = pd.read_excel(out, sheet_name="抽出結果")
    assert list(df.columns) == ["page", "line_num", "text"]
