# config.py

# RSS 新闻源配置
RSS_SOURCES = [
    {
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "少数派",
        "url": "https://sspai.com/feed",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "纽约时报中文网",
        "url": "https://cn.nytimes.com/rss/",
        "category": "国际",
        "max_items": 10,
    },
    {
        "name": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
        "category": "国际",
        "max_items": 10,
    },
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "category": "科技",
        "max_items": 10,
    },
]

# HTML 爬虫源（作为补充）
HTML_SOURCES = [
    {
        "name": "IT之家",
        "url": "https://www.ithome.com/",
        "category": "科技",
        "parser": "ithome",
    },
]

# 去重阈值（SimHash 汉明距离）
DEDUP_HAMMING_THRESHOLD = 3