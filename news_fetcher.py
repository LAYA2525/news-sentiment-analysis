# news_fetcher.py
"""
Polls a News API and writes each article as a single-line JSON into data/incoming/
This file is intentionally simple: it polls every POLL_INTERVAL_SECONDS.

Put your API key into .env as NEWS_API_KEY.
"""

import os
import time
import json
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS") or 30)
QUERY = os.getenv("NEWS_QUERY") or "technology"
PAGE_SIZE = int(os.getenv("PAGE_SIZE") or 10)

INCOMING_DIR = "data/incoming"
os.makedirs(INCOMING_DIR, exist_ok=True)

if not API_KEY:
    print("No NEWS_API_KEY set in environment. Copy .env.example -> .env and fill key.")
    raise SystemExit(1)

# NewsAPI.org endpoint style. If you use a different provider, adjust the URL/params.
NEWS_URL = "https://newsapi.org/v2/everything"

def fetch_and_write():
    params = {
        "q": QUERY,
        "pageSize": PAGE_SIZE,
        "language": "en",
        # "from": (optional) use ISO8601 timestamp,
        "apiKey": API_KEY
    }
    try:
        r = requests.get(NEWS_URL, params=params, timeout=15)
        r.raise_for_status()
        resp = r.json()
        articles = resp.get("articles", [])
        now_ms = int(time.time() * 1000)
        for a in articles:
            obj = {
                "id": str(uuid.uuid4()),
                "text": a.get("title") or "",
                "publishedAt": a.get("publishedAt"),
                "source": (a.get("source") or {}).get("name"),
                "url": a.get("url")
            }
            fname = os.path.join(INCOMING_DIR, f"{now_ms}_{obj['id']}.json")
            # Write one JSON object per file
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False)
        print(f"Fetched {len(articles)} articles → wrote to {INCOMING_DIR}")
    except Exception as e:
        print("Fetch error:", e)

def main():
    print("Starting news fetcher (ctrl-C to stop). Poll interval:", POLL_INTERVAL, "seconds")
    while True:
        fetch_and_write()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
