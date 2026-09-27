# config.py

# 国内新闻 RSS 源
RSS_SOURCES = [
    # ========== 科技 / 互联网 ==========
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
        "name": "爱范儿",
        "url": "https://www.ifanr.com/feed",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "IT之家",
        "url": "https://www.ithome.com/rss/",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "Solidot 奇客",
        "url": "https://www.solidot.org/index.rss",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "虎嗅",
        "url": "https://www.huxiu.com/rss/0.xml",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "钛媒体",
        "url": "https://www.tmtpost.com/rss.xml",
        "category": "科技",
        "max_items": 15,
    },
    {
        "name": "InfoQ 中文",
        "url": "https://www.infoq.cn/feed",
        "category": "技术",
        "max_items": 15,
    },
    {
        "name": "酷壳",
        "url": "https://www.coolshell.cn/feed",
        "category": "技术",
        "max_items": 10,
    },
    {
        "name": "V2EX",
        "url": "https://www.v2ex.com/index.xml",
        "category": "技术",
        "max_items": 15,
    },

    # ========== 社会 / 综合 ==========
    {
        "name": "联合早报·中国",
        "url": "https://www.zaobao.com/realtime/china/rss.xml",
        "category": "社会",
        "max_items": 15,
    },
    {
        "name": "人民网·时政",
        "url": "http://www.people.com.cn/rss/politics.xml",
        "category": "时政",
        "max_items": 15,
    },
    {
        "name": "新华网·时政",
        "url": "http://www.xinhuanet.com/politics/news_politics.xml",
        "category": "时政",
        "max_items": 15,
    },
    {
        "name": "中国新闻网",
        "url": "https://www.chinanews.com.cn/rss/scroll-news.xml",
        "category": "社会",
        "max_items": 15,
    },

    # ========== 热搜榜（通过 RSSHub） ==========
    {
        "name": "微博热搜",
        "url": "https://rsshub.app/weibo/search/hot",
        "category": "热搜",
        "max_items": 20,
    },
    {
        "name": "知乎热榜",
        "url": "https://rsshub.app/zhihu/hotlist",
        "category": "热搜",
        "max_items": 20,
    },
    {
        "name": "百度热搜",
        "url": "https://rsshub.app/baidu/top",
        "category": "热搜",
        "max_items": 20,
    },
]

# HTML 爬虫源（保留为空，以后想加 HTML 爬虫再填）
HTML_SOURCES = []

# 去重阈值
DEDUP_HAMMING_THRESHOLD = 3