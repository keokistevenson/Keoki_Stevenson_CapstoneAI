# src/youtube_university/transcripts.py
"""Read the local transcript library: headers and manifest now, parsing and chunking in CP10."""
import csv
import re
from dataclasses import dataclass
from pathlib import Path

TRANSCRIPT_DIR = Path("data/transcripts")
MANIFEST_PATH = Path("data/transcript_manifest.csv")

VIDEO_URL = re.compile(r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})")
STANDARD_TS = re.compile(r"^\d+:\d{2}(?::\d{2})?$")                          # "4:11" alone on a line
MERGED_TS = re.compile(r"^\d+:\d{2}(?::\d{2})?\d+ (?:hour|minute|second)")   # "0:077 secondsWelcome..."


@dataclass
class TranscriptHeader:
    """What we know about one transcript file before parsing its text."""
    file: str
    video_id: str
    title: str
    url: str
    timestamp_format: str      # "standard", "merged", or "none"


def read_header(path: Path) -> TranscriptHeader:
    """Read the title (line 1), the YouTube URL (first 6 lines), and the timestamp style."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()   # -sig strips a Windows byte-order mark
    title = lines[0].strip()

    for line in lines[:6]:
        match = VIDEO_URL.search(line)
        if match:
            break
    else:                      # runs only if the loop finished WITHOUT break
        raise ValueError(f"No YouTube URL in the first 6 lines of {path.name}")
    video_id = match.group(1)

    if any(STANDARD_TS.match(line.strip()) for line in lines):
        timestamp_format = "standard"
    elif any(MERGED_TS.match(line) for line in lines):
        timestamp_format = "merged"
    else:
        timestamp_format = "none"

    url = f"https://www.youtube.com/watch?v={video_id}"
    return TranscriptHeader(path.name, video_id, title, url, timestamp_format)


def build_manifest(folder: Path = TRANSCRIPT_DIR, out: Path = MANIFEST_PATH) -> list[TranscriptHeader]:
    """Read every transcript header and write them all to one CSV file."""
    headers = [read_header(path) for path in sorted(folder.glob("*.txt"))]
    with out.open("w", newline="", encoding="utf-8") as f:     # newline="" avoids blank rows on Windows
        writer = csv.writer(f)
        writer.writerow(["file", "video_id", "title", "url", "timestamp_format"])
        for h in headers:
            writer.writerow([h.file, h.video_id, h.title, h.url, h.timestamp_format])
    return headers


if __name__ == "__main__":
    headers = build_manifest()
    for h in headers:
        print(f"{h.video_id}  {h.timestamp_format:8}  {h.title}")
    print(f"\n{len(headers)} transcripts written to {MANIFEST_PATH}")
