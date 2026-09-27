# dedup.py
import re
import hashlib
import jieba
from config import DEDUP_HAMMING_THRESHOLD

def normalize_title(title: str) -> str:
    title = re.sub(r'[^\w\u4e00-\u9fff]', '', title)
    title = title.lower()
    for suffix in ['独家', '重磅', '最新', '快讯', '视频', '图集']:
        title = title.replace(suffix, '')
    return title.strip()

def _hash_token(token: str) -> int:
    return int(hashlib.md5(token.encode('utf-8')).hexdigest()[:16], 16)

def _has_chinese(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def simhash(text: str) -> int:
    tokens = list(jieba.cut(text)) if _has_chinese(text) else text.split()
    if not tokens:
        return 0
    v = [0] * 64
    for token in tokens:
        h = _hash_token(token)
        for i in range(64):
            if h >> i & 1:
                v[i] += 1
            else:
                v[i] -= 1
    fingerprint = 0
    for i in range(64):
        if v[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint

def hamming_distance(h1: int, h2: int) -> int:
    return bin(h1 ^ h2).count('1')

def deduplicate(articles: list) -> list:
    seen = []
    result = []
    for art in articles:
        norm = normalize_title(art.get('title', ''))
        if not norm:
            continue
        if any(norm == s[0] for s in seen):
            continue
        h = simhash(norm)
        is_dup = False
        for _, existing_hash, _ in seen:
            if hamming_distance(h, existing_hash) <= DEDUP_HAMMING_THRESHOLD:
                is_dup = True
                break
        if is_dup:
            continue
        seen.append((norm, h, art))
        result.append(art)
    return result