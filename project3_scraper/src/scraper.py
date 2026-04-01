"""
Hacker News トップ記事スクレイパー
- Hacker News（https://news.ycombinator.com）の記事一覧を取得
- タイトル・URL・スコア・投稿日時をCSVに保存
- キーワードフィルタオプション付き

使い方:
    python src/scraper.py                        # 全記事取得
    python src/scraper.py --keyword python       # "python"を含む記事のみ
    python src/scraper.py --pages 3              # 3ページ分取得

依存: pip install requests beautifulsoup4
"""

import argparse
import csv
import logging
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

BASE_URL = "https://news.ycombinator.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-scraper/1.0)"}


def fetch_page(url: str) -> BeautifulSoup | None:
    """ページを取得してBeautifulSoupオブジェクトを返す。

    通信エラーが発生した場合はログに記録して None を返す（クラッシュしない設計）。

    Args:
        url: 取得対象のURL。

    Returns:
        パース済みの BeautifulSoup オブジェクト。取得失敗時は None。
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logging.error(f"取得失敗: {url} - {e}")
        return None


def parse_articles(soup: BeautifulSoup, keyword: str = "") -> list[dict]:
    """BeautifulSoup から記事情報を抽出する。

    Args:
        soup: Hacker News ページのパース済み BeautifulSoup オブジェクト。
        keyword: タイトルフィルタ用のキーワード（省略可、大文字小文字を無視）。

    Returns:
        記事情報の辞書リスト。各辞書は以下のキーを持つ:
        - title (str): 記事タイトル
        - url   (str): 記事URL（絶対URL）
        - score (int): スコア（取得できない場合は 0）
        - scraped_at (str): スクレイピング日時（"YYYY-MM-DD HH:MM:SS" 形式）
    """
    articles = []
    rows = soup.select("tr.athing")
    for row in rows:
        # タイトルとURL
        title_tag = row.select_one("span.titleline > a")
        if not title_tag:
            continue
        title = title_tag.get_text()
        link = title_tag.get("href", "")
        if link.startswith("item?"):
            link = f"{BASE_URL}/{link}"

        # キーワードフィルタ（大文字小文字を無視）
        if keyword and keyword.lower() not in title.lower():
            continue

        # スコア行（次の兄弟 <tr> に格納されている）
        subrow = row.find_next_sibling("tr")
        score_tag = subrow.select_one("span.score") if subrow else None
        try:
            score: int = int(
                score_tag.get_text().replace(" points", "").replace(" point", "")
            ) if score_tag else 0
        except ValueError:
            score = 0

        articles.append({
            "title": title,
            "url": link,
            "score": score,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    return articles


def save_csv(records: list[dict], output_path: str) -> None:
    """記事リストをCSVファイルに保存する。

    出力先ディレクトリが存在しない場合は自動生成する。

    Args:
        records: parse_articles() の戻り値（辞書のリスト）。
        output_path: 出力先CSVファイルのパス。
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "score", "scraped_at"])
        writer.writeheader()
        writer.writerows(records)
    logging.info(f"CSV出力完了: {output_path} ({len(records)}件)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hacker News スクレイパー")
    parser.add_argument("--keyword", default="", help="フィルタキーワード（省略可）")
    parser.add_argument("--pages",   type=int, default=1, help="取得ページ数（デフォルト: 1）")
    parser.add_argument("--output",  default="output/hn_articles.csv", help="出力CSVのパス")
    args = parser.parse_args()

    all_articles = []
    for page in range(1, args.pages + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}/?p={page}"
        logging.info(f"取得中: {url}")
        soup = fetch_page(url)
        if soup:
            articles = parse_articles(soup, keyword=args.keyword)
            all_articles.extend(articles)
            logging.info(f"  → {len(articles)}件取得")
        if page < args.pages:
            time.sleep(1)  # サーバー負荷軽減のための待機

    if not all_articles:
        print("記事が見つかりませんでした。")
        return

    save_csv(all_articles, args.output)
    logging.info(f"合計: {args.pages}ページから {len(all_articles)}件取得")
    print(f"完了: {len(all_articles)}件を {args.output} に保存しました。")


if __name__ == "__main__":
    main()
