# config.py

RSS_SOURCES = [
    # ========== 科技 ==========
    {"name": "36氪", "url": "https://36kr.com/feed", "category": "科技", "max_items": 20},
    {"name": "少数派", "url": "https://sspai.com/feed", "category": "科技", "max_items": 20},
    {"name": "爱范儿", "url": "https://www.ifanr.com/feed", "category": "科技", "max_items": 20},
    {"name": "IT之家", "url": "https://www.ithome.com/rss/", "category": "科技", "max_items": 20},
    {"name": "虎嗅", "url": "https://www.huxiu.com/rss/0.xml", "category": "科技", "max_items": 20},
    {"name": "钛媒体", "url": "https://www.tmtpost.com/rss.xml", "category": "科技", "max_items": 20},
    {"name": "雷峰网", "url": "https://www.leiphone.com/feed", "category": "科技", "max_items": 20},

    # ========== 技术 ==========
    {"name": "V2EX", "url": "https://www.v2ex.com/index.xml", "category": "技术", "max_items": 20},
    {"name": "开源中国", "url": "https://www.oschina.net/news/rss", "category": "技术", "max_items": 20},
    {"name": "掘金前端", "url": "https://rsshub.app/juejin/category/frontend", "category": "技术", "max_items": 20},
    {"name": "掘金后端", "url": "https://rsshub.app/juejin/category/backend", "category": "技术", "max_items": 20},

    # ========== 财经 ==========
    {"name": "华尔街见闻", "url": "https://rsshub.app/wallstreetcn/news/global", "category": "财经", "max_items": 20},
    {"name": "雪球热帖", "url": "https://rsshub.app/xueqiu/hots", "category": "财经", "max_items": 20},

    # ========== 社会 ==========
    {"name": "中国新闻网", "url": "https://www.chinanews.com.cn/rss/scroll-news.xml", "category": "社会", "max_items": 20},

    # ========== 热搜 ==========
    {"name": "微博热搜", "url": "https://rsshub.app/weibo/search/hot", "category": "热搜", "max_items": 30},
    {"name": "百度热搜", "url": "https://rsshub.app/baidu/top", "category": "热搜", "max_items": 30},
    {"name": "知乎热榜", "url": "https://rsshub.app/zhihu/hotlist", "category": "热搜", "max_items": 30},
    {"name": "抖音热点", "url": "https://rsshub.app/douyin/hot", "category": "热搜", "max_items": 30},
    {"name": "B站热门", "url": "https://rsshub.app/bilibili/popular/all", "category": "热搜", "max_items": 30},
    {"name": "今日头条", "url": "https://rsshub.app/toutiao/today", "category": "热搜", "max_items": 30},

    # ========== 娱乐 ==========
    {"name": "豆瓣电影", "url": "https://rsshub.app/douban/movie/playing", "category": "娱乐", "max_items": 20},

    # ========== 游戏 ==========
    {"name": "机核 GCORES", "url": "https://www.gcores.com/rss", "category": "游戏", "max_items": 20},
    {"name": "游研社", "url": "https://rsshub.app/yystv/home", "category": "游戏", "max_items": 20},

    # ========== 阅读 ==========
    {"name": "知乎日报", "url": "https://rsshub.app/zhihu/daily", "category": "阅读", "max_items": 20},
    {"name": "理想生活实验室", "url": "https://www.toodaylab.com/feed", "category": "阅读", "max_items": 15},
]

HTML_SOURCES = []

DEDUP_HAMMING_THRESHOLD = 3