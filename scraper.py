# scraper.py
import os
import json
import concurrent.futures
from datetime import datetime, timezone
import feedparser
import requests
from bs4 import BeautifulSoup
from config import RSS_SOURCES, HTML_SOURCES
from dedup import deduplicate

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def fetch_rss_source(source: dict) -> list:
    articles = []
    try:
        feed = feedparser.parse(source["url"], request_headers=HEADERS)
        for entry in feed.entries[: source.get("max_items", 15)]:
            title = entry.get("title", "").strip()
            if not title:
                continue
            link = entry.get("link", "")
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            if published:
                pub_dt = datetime(*published[:6], tzinfo=timezone.utc)
                pub_str = pub_dt.strftime("%Y-%m-%d %H:%M")
            else:
                pub_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            summary = entry.get("summary", "") or entry.get("description", "")
            summary = BeautifulSoup(summary, "html.parser").get_text()[:200]
            articles.append({
                "title": title,
                "link": link,
                "source": source["name"],
                "category": source.get("category", "综合"),
                "published": pub_str,
                "summary": summary.strip(),
            })
    except Exception as e:
        print(f"[RSS ERROR] {source['name']}: {e}")
    return articles

def fetch_ithome(source: dict) -> list:
    articles = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(".newslist li")[:15]:
            a_tag = item.select_one("a")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            link = a_tag.get("href", "")
            if link and not link.startswith("http"):
                link = "https://www.ithome.com" + link
            time_tag = item.select_one(".time")
            pub_str = time_tag.get_text(strip=True) if time_tag else \
                datetime.now().strftime("%Y-%m-%d %H:%M")
            articles.append({
                "title": title,
                "link": link,
                "source": source["name"],
                "category": source.get("category", "科技"),
                "published": pub_str,
                "summary": "",
            })
    except Exception as e:
        print(f"[HTML ERROR] {source['name']}: {e}")
    return articles

def fetch_all() -> list:
    all_articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        rss_futures = [executor.submit(fetch_rss_source, src) for src in RSS_SOURCES]
        html_futures = [
            executor.submit(fetch_ithome, src)
            for src in HTML_SOURCES
            if src.get("parser") == "ithome"
        ]
        for future in concurrent.futures.as_completed(rss_futures + html_futures):
            try:
                all_articles.extend(future.result())
            except Exception as e:
                print(f"[FETCH ERROR] {e}")
    return all_articles

def main():
    print("开始抓取新闻...")
    raw = fetch_all()
    deduped = deduplicate(raw)
    deduped.sort(key=lambda x: x.get("published", ""), reverse=True)
    result = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_raw": len(raw),
        "total_after_dedup": len(deduped),
        "articles": deduped
    }
    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"抓取完成：原始 {len(raw)} 条 → 去重后 {len(deduped)} 条")

if __name__ == "__main__":
    main()