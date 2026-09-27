# scraper.py
import os
import re
import json
import hashlib
import concurrent.futures
from datetime import datetime, timezone
import feedparser
import requests
import trafilatura
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

MAX_CONTENT_LEN = 5000
MAX_IMAGES = 5


def article_id(url: str, title: str) -> str:
    return hashlib.md5((url or title).encode("utf-8")).hexdigest()[:10]


def is_image_url(url: str) -> bool:
    return bool(re.search(r'\.(jpg|jpeg|png|gif|webp|bmp)(\?|$)', url or '', re.I))


def extract_cover(entry, summary_html: str = "") -> str:
    for m in entry.get("media_content") or []:
        u = m.get("url", "")
        if u and (is_image_url(u) or m.get("medium") == "image"):
            return u
    for m in entry.get("media_thumbnail") or []:
        u = m.get("url", "")
        if u:
            return u
    for e in entry.get("enclosures") or []:
        if "image" in (e.get("type") or ""):
            return e.get("href") or e.get("url") or ""
    if summary_html:
        m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary_html)
        if m:
            return m.group(1)
    return ""


def fetch_rss_source(source: dict) -> list:
    articles = []
    try:
        feed = feedparser.parse(source["url"], request_headers=HEADERS)
        for entry in feed.entries[: source.get("max_items", 15)]:
            title = entry.get("title", "").strip()
            if not title:
                continue
            link = entry.get("link", "")
            pub = entry.get("published_parsed") or entry.get("updated_parsed")
            if pub:
                pub_str = datetime(*pub[:6], tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M")
            else:
                pub_str = datetime.now().strftime("%Y-%m-%d %H:%M")

            summary_raw = entry.get("summary", "") or entry.get("description", "")
            summary = BeautifulSoup(summary_raw, "html.parser").get_text()[:200].strip()
            cover = extract_cover(entry, summary_raw)

            articles.append({
                "id": article_id(link, title),
                "title": title,
                "link": link,
                "source": source["name"],
                "category": source.get("category", "综合"),
                "published": pub_str,
                "summary": summary,
                "cover": cover,
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
                "id": article_id(link, title),
                "title": title,
                "link": link,
                "source": source["name"],
                "category": source.get("category", "科技"),
                "published": pub_str,
                "summary": "",
                "cover": "",
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


def fetch_content_and_images(url: str):
    if not url:
        return "", []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = resp.apparent_encoding or "utf-8"
        html = resp.text

        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
        ) or ""

        images = []
        soup = BeautifulSoup(html, "html.parser")
        container = (
            soup.select_one("article") or
            soup.select_one(".article-content") or
            soup.select_one(".post-content") or
            soup.select_one(".content") or
            soup.select_one("#content") or
            soup
        )
        for img in container.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-original") or ""
            if not src.startswith("http"):
                continue
            w = img.get("width")
            if w and str(w).isdigit() and int(w) < 200:
                continue
            if src not in images:
                images.append(src)
            if len(images) >= MAX_IMAGES:
                break

        return text[:MAX_CONTENT_LEN], images
    except Exception as e:
        print(f"[CONTENT ERROR] {url[:60]}: {e}")
        return "", []


def main():
    print("开始抓取新闻列表...")
    raw = fetch_all()
    deduped = deduplicate(raw)
    deduped.sort(key=lambda x: x.get("published", ""), reverse=True)
    print(f"去重后 {len(deduped)} 条，开始抓正文和封面...")

    contents = {}

    def worker(art):
        text, imgs = fetch_content_and_images(art.get("link", ""))
        contents[art["id"]] = {"content": text, "images": imgs}
        if not art.get("cover") and imgs:
            art["cover"] = imgs[0]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(worker, deduped))

    got_content = sum(1 for c in contents.values() if c.get("content"))
    got_cover = sum(1 for a in deduped if a.get("cover"))
    print(f"成功抓正文：{got_content}/{len(deduped)}，封面图：{got_cover}/{len(deduped)}")

    os.makedirs("data", exist_ok=True)

    news_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_raw": len(raw),
        "total_after_dedup": len(deduped),
        "articles": deduped,
    }
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, separators=(",", ":"))

    with open("data/contents.json", "w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, separators=(",", ":"))

    print("完成！")


if __name__ == "__main__":
    main()