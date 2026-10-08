# src/youtube_university/youtube.py
"""Everything that talks to the YouTube Data API."""
import json
import os
import html

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

VIDEOS_PER_MODULE = 3


def find_videos(queries: list[str], seen_ids: set[str]) -> list[dict]:
    """Search YouTube with each query and return a few simple video dicts."""
    videos = []
    for query in queries:
        for item in search_youtube(query):
            video_id = item["id"]["videoId"]
            title = html.unescape(item["snippet"]["title"])
            channel_title = html.unescape(item["snippet"]["channelTitle"])
            
            if video_id in seen_ids:
                continue

            if "#shorts" in title.lower():
                continue
            
            seen_ids.add(video_id)

            videos.append({"title": title, "channel": channel_title, "url": f"https://www.youtube.com/watch?v={video_id}"})

            if len(videos) == VIDEOS_PER_MODULE: 
                return videos
    return videos

if __name__ == "__main__":
    seen = set()
    first = find_videos(["python for beginners"], seen)
    second = find_videos(["python for beginners"], seen)   # same query, same seen set
    print("first: ", first)
    print("second:", second)