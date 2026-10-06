# src/youtube_university/youtube.py
"""Everything that talks to the YouTube Data API."""
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()                                # copies key=value lines from .env into environment variables
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")   # None (null) if missing
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def search_youtube(query: str, max_results: int = 5) -> list[dict]:
    """Call YouTube search.list for one query and return the raw result items."""
    try:
        resp = requests.get(
            SEARCH_URL,
            params={                          # requests URL-encodes this dict for you
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "key": YOUTUBE_KEY,
            },
            timeout=10,                       # without a timeout, a network problem can hang forever
        )
    except requests.RequestException:
        # `from None` hides the original error: its text can contain the URL, which contains your key
        raise RuntimeError("Could not reach YouTube. Check your internet connection.") from None
    
    if resp.status_code != 200:
        try:
            message = resp.json()["error"]["message"]    # Google's own explanation
        except (ValueError, KeyError):                   # body wasn't JSON, or had no "error" field
            message = "no details provided"
        raise RuntimeError(f"YouTube returned an error ({resp.status_code}): {message}")
    return resp.json()["items"]

if __name__ == "__main__":   # test this file alone: uv run python -m youtube_university.youtube
    items = search_youtube("python tutorial for beginners")
    print(json.dumps(items[0], indent=2))     # look at the raw structure once
    for item in items:
        video_id = item["id"]["videoId"]
        print(item["snippet"]["title"], "->", f"https://www.youtube.com/watch?v={video_id}")