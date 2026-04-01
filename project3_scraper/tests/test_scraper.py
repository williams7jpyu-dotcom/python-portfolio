"""Unit tests for scraper.py"""

import csv
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests as req_lib
from bs4 import BeautifulSoup

from scraper import fetch_page, parse_articles, save_csv


# ── HTML fixture ──────────────────────────────────────────────────────────────

HN_HTML = """
<html><body><table>
  <tr class="athing">
    <td><span class="titleline">
      <a href="https://example.com/python">Python 3.13 Released</a>
    </span></td>
  </tr>
  <tr>
    <td><span class="score">312 points</span></td>
  </tr>
  <tr class="athing">
    <td><span class="titleline">
      <a href="https://other.com/js">JavaScript Framework Wars</a>
    </span></td>
  </tr>
  <tr>
    <td><span class="score">87 points</span></td>
  </tr>
</table></body></html>
"""


@pytest.fixture
def soup() -> BeautifulSoup:
    """テスト用の BeautifulSoup オブジェクトを返す。"""
    return BeautifulSoup(HN_HTML, "html.parser")


# ── parse_articles() tests ────────────────────────────────────────────────────

def test_parse_articles_returns_list(soup: BeautifulSoup) -> None:
    """記事リストが返ること。"""
    articles = parse_articles(soup)
    assert isinstance(articles, list)
    assert len(articles) == 2


def test_parse_articles_keys(soup: BeautifulSoup) -> None:
    """各記事に title, url, score, scraped_at キーが存在すること。"""
    articles = parse_articles(soup)
    for article in articles:
        assert set(article.keys()) == {"title", "url", "score", "scraped_at"}


def test_score_is_integer(soup: BeautifulSoup) -> None:
    """score が整数型で返ること。"""
    articles = parse_articles(soup)
    for article in articles:
        assert isinstance(article["score"], int)


def test_keyword_filter(soup: BeautifulSoup) -> None:
    """キーワードフィルタが大文字小文字を無視して動作すること。"""
    articles = parse_articles(soup, keyword="python")
    assert len(articles) == 1
    assert "Python" in articles[0]["title"]


def test_relative_url_converted() -> None:
    """Hacker News 内部リンク（相対URL）が絶対URLに変換されること。"""
    html = """
    <html><body><table>
      <tr class="athing">
        <td><span class="titleline">
          <a href="item?id=12345">HN Discussion</a>
        </span></td>
      </tr>
      <tr><td></td></tr>
    </table></body></html>
    """
    s = BeautifulSoup(html, "html.parser")
    articles = parse_articles(s)
    assert articles[0]["url"].startswith("https://")


# ── fetch_page() tests ────────────────────────────────────────────────────────

@patch("scraper.requests.get")
def test_fetch_page_returns_none_on_error(mock_get: MagicMock) -> None:
    """通信エラー発生時に None が返ること（クラッシュしないこと）。"""
    mock_get.side_effect = req_lib.RequestException("connection timeout")
    result = fetch_page("https://example.com")
    assert result is None


# ── save_csv() tests ──────────────────────────────────────────────────────────

def test_save_csv_creates_file(tmp_path: Path) -> None:
    """CSVファイルが正しく生成されること。"""
    records = [
        {
            "title": "Test Article",
            "url": "https://example.com",
            "score": 100,
            "scraped_at": "2024-01-01 00:00:00",
        }
    ]
    out = str(tmp_path / "articles.csv")
    save_csv(records, out)
    assert Path(out).exists()

    # 保存した内容を検証
    with open(out, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["title"] == "Test Article"
