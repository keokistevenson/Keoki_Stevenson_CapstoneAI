# LearningPath AI — Revised V2 Implementation Plan

Oct 13, 2026 · @Sam

V2 adds saved learning paths and curriculum-scoped transcript Q&A in checkpoints 7–14, estimated at 18–25 hours across three focused days. This replaces the V2 section of `implementation_plan.md`; V1 checkpoints 1–6 stay as they are.

## Scope decisions and flagged adjustments

**1. The demo curriculum will not match the library on its own.** V1 searches all of YouTube, so a freshly generated Python curriculum will rarely recommend any of the 29 library videos. Without a fix, requirement 7.5 (several indexed videos in the saved curriculum) cannot be met. Smallest adjustment: a small curation helper that attaches chosen library videos to a saved curriculum's modules by video ID, taking title and URL from the transcript manifest, so every record is genuine. Saved videos get a `source` field (`youtube_search` or `library`) so the demo is honest about which is which. Automatic matching of modules to library videos is deliberately excluded; it borders on curriculum rewriting, which section 6 rules out.

**2. Timestamps depend on what the .txt files contain.** If the transcripts carry per-line times, chunks keep the start time of their first line. If they don't, links go to the video without `&t=`, as the requirements allow; timestamps are never reconstructed. Checkpoint 7 settles this before any parsing code is written.

**3. Checkpoint 6 is still open.** README, documentation, workflow diagram, fresh-clone check and rehearsal are unchecked, yet the GitHub/Canvas submission is checked. If the presentation has not happened yet, finish those first; the three V2 days start afterward.

**4. Stack choices.**

- Persistence: one JSON file per learning path in `data/curricula/`, written and read through Pydantic.
- Embeddings: `nomic-embed-text` through the Ollama you already run; no PyTorch install.
- Vector store: Qdrant `PersistentClient` in `data/qdrant/` (Git-ignored), cosine distance, metadata filter for curriculum scoping.
- Generation: `llama3.2:3b`, as in V1. No LangChain; the direct calls are a few lines each.

**Open questions to answer before coding**

- [ ] What does one transcript file look like (first 20 lines)? Does it include timestamps, a title or a URL?
- [ ] Does V1 store videos as a Pydantic model or as dicts?
- [ ] Has the capstone presentation already been given?

## Schedule

Day 1 delivers saved learning paths, Day 2 delivers a scoped search over the index, and Day 3 delivers grounded answers and the demo.

| Day | Checkpoints | Hours | V2 checklist items covered |
| --- | --- | --- | --- |
| 1 | 7 Transcript spike + manifest · 8 Save/load paths · 9 Terminal menu | 5–7.5 | Save to JSON; list and reopen |
| 2 | 10 Parse + chunk · 11 Embedding index · 12 Scoped retrieval + demo curriculum | 7–9.5 | Index transcripts; match by video ID |
| 3 | 13 Grounded answers + links · 14 Tests, eval, demo, tag | 5.5–8 | Ask across curriculum; display sources; test cases |

The end of Day 2 is the checkpoint that matters most: if scoped retrieval returns the right videos, Day 3 is prompt work and polish. If Day 2 runs over, cut in this order:

1. Menu niceties (keep plain numbered input).
2. Embedding the full library (demo on the 8–10 transcripts in the demo curriculum).
3. Distance-threshold tuning (keep the LLM's refusal instruction only).
4. The automated eval script (run the six demo questions by hand).

## Day 1: checkpoints 7–9

### Checkpoint 7 — Transcript format spike and manifest

- **Purpose:** know exactly what the 29 files contain before writing parsing code, and give every transcript a genuine video ID.
- **Build:** a throwaway script that prints each file's first lines, encoding issues, and whether timestamps are present; then `data/transcript_manifest.csv` with `file, video_id, title, url`, filled from the real YouTube pages.
- **Files:** `scratch/inspect_transcripts.py`, `data/transcripts/`, `data/transcript_manifest.csv`, `docs/dev_log.md`.
- **Concepts:** `pathlib.Path` (like `System.IO.Path` plus `FileInfo` in one object), reading with `encoding="utf-8-sig"` to strip a Windows byte-order mark, `re` patterns for timestamps such as `[04:11]` or `0:04:11`.
- **Done when:** the script reports all 29 files as matched to a manifest row, each with an 11-character video ID and a yes/no for timestamps, and the timestamp format is recorded in the dev log.
- **Time:** 1.5–2.5 h.

### Checkpoint 8 — Save, list and load learning paths

- **Purpose:** a generated curriculum survives a restart without calling Ollama or YouTube again.
- **Build:** a `SavedLearningPath` model (id, created time, profile, curriculum, videos per module, each video with `source`), plus `save_path`, `list_paths` and `load_path`. One JSON file per path, named by its id.
- **Files:** `models.py` (add models; add a `Video` model if V1 uses dicts), new `storage.py`, `tests/test_storage.py`.
- **Concepts:** Pydantic `model_dump_json()` and `model_validate_json()` (comparable to `System.Text.Json` with validation built in), `uuid4().hex` ids, timezone-aware `datetime.now(timezone.utc)`, pytest's `tmp_path` fixture for writing to a throwaway folder.
- **Done when:** a round-trip test saves and reloads a path and the two models compare equal; listing returns paths newest first; loading a missing or corrupted file raises a clear error naming the file.
- **Time:** 2.5–3.5 h.

### Checkpoint 9 — Terminal menu for new and saved paths

- **Purpose:** wire Options A and B into the existing terminal app.
- **Build:** a main menu (new path, open saved path, quit); after generating, a save prompt; after opening, a review screen with an "ask a question" option stubbed for now.
- **Files:** your existing entry point (for example `main.py` or `cli.py`).
- **Concepts:** keeping input loops separate from logic so the logic stays testable; `match` statements (Python 3.10+, similar to a C# `switch` expression).
- **Done when:** generate → save → quit → restart → open shows the same curriculum and videos, with Ollama stopped during the reopen to prove nothing is regenerated; invalid menu input re-prompts instead of crashing.
- **Time:** 1–1.5 h (merge into checkpoint 8 if it runs short).

## Day 2: checkpoints 10–12

### Checkpoint 10 — Parse and chunk transcripts with timestamps

- **Purpose:** turn each file into chunks that carry their video ID, title and start time from the moment they are created.
- **Build:** a parser that yields `(start_seconds, text)` segments in the format found in checkpoint 7, and a chunker that groups consecutive segments into roughly 150–250 words with one segment of overlap. Each chunk keeps the start time of its first segment and a stable id such as `<video_id>_0007`.
- **Files:** new `transcripts.py`, `tests/test_transcripts.py` with a small sample transcript under `tests/fixtures/`.
- **Concepts:** generator functions with `yield` (the same idea as C# `yield return`), `re` named groups, `@dataclass` for a lightweight chunk record (similar to a C# record), converting `h:mm:ss` to seconds.
- **Done when:** tests pass for timestamp parsing (including a line without a time), chunk overlap and stable ids; all 29 files parse with zero empty chunks; the total chunk count is logged.
- **Time:** 2.5–3.5 h.

### Checkpoint 11 — Embedding index in Qdrant

- **Purpose:** index once, reuse on every run.
- **Build:** a `build_index` command that embeds chunks in batches with `nomic-embed-text` (prefix `"search_document: "`) and upserts them into a persistent qdrant collection created with cosine distance. Metadata per chunk: `video_id`, `title`, `start_seconds`, `chunk_index`. Run it on 3 transcripts first, time it, then run the rest.
- **Files:** new `index.py`, a small script or menu option to build the index, `.gitignore` entry for `data/qdrant/`.
- **Concepts:** what an embedding is and why queries and documents must use the same model; batching; `upsert` versus `add` (re-running replaces rather than duplicates); Qdrant metadata accepts only strings, numbers and booleans, so a missing timestamp is stored as `-1`, never `None`.
- **Done when:** the collection count equals the chunk count; running the build a second time leaves the count unchanged; per-chunk embedding time is recorded in the dev log.
- **Time:** 2.5–3.5 h.

### Checkpoint 12 — Curriculum-scoped retrieval and the demo curriculum

- **Purpose:** search only the videos that belong to the open learning path.
- **Build:** `indexed_video_ids(path)` returns the curriculum's video IDs that exist in the index; `search(question, video_ids, k=4)` embeds the question (prefix `"search_query: "`) and queries Qdrant with `where={"video_id": {"$in": video_ids}}`. Then the curation helper from scope decision 1 attaches several library videos to a saved "Python for AI development" curriculum generated by V1.
- **Files:** `index.py` (or a new `retrieval.py`), `storage.py` (curation helper), `tests/test_retrieval.py`.
- **Concepts:** vector search and cosine distance; metadata filtering; reading distances to calibrate what a weak match looks like.
- **Done when:** a test asserts that every returned chunk's video ID is in the curriculum; a curriculum with no indexed videos returns a clear message without querying Qdrant (an empty `$in` filter is not a safe query); the saved demo curriculum shows at least four indexed videos; distances for three on-topic and two off-topic questions are logged.
- **Time:** 2–2.5 h.

## Day 3: checkpoints 13–14

### Checkpoint 13 — Grounded answers with timestamped links

- **Purpose:** answer only from retrieved passages and show exactly where each claim came from.
- **Build:** a prompt that numbers the retrieved passages `[1]`–`[4]` with their video titles, tells the model to answer only from them, cite with `[n]`, never invent code that is not in the text, and reply with a fixed "could not establish this from the indexed videos" sentence when the passages do not cover the question. After generation, parse the `[n]` citations and show only the sources actually cited, each with `https://www.youtube.com/watch?v=VIDEO_ID&t=251s` (or no `&t=` when the start time is `-1`). If the best distance is past the threshold from checkpoint 12, skip the LLM call and return the refusal directly.
- **Files:** new `qa.py`, `llm.py` (reuse the existing Ollama call), `tests/test_qa.py`.
- **Concepts:** context injection; grounding and refusal; why citations are validated in code rather than trusted; a low temperature for factual answers; Ollama's context length limit (keep 4 chunks of about 200 words).
- **Done when:** with Ollama mocked, tests confirm that citations map to the right titles and links, an uncited or out-of-range `[n]` is dropped, and a weak retrieval skips the LLM; live, three supported questions cite the correct videos and their links open within about 30 seconds of the relevant passage.
- **Time:** 3–4.5 h.

### Checkpoint 14 — Q&A in the menu, evaluation and demo

- **Purpose:** close the vertical slice and prove it holds up.
- **Build:** connect the "ask a question" option from checkpoint 9 to `qa.py`; show which videos in the path are indexed before the first question. Write six evaluation questions: three the transcripts answer, two they do not (including one about on-screen code), and one asked on a curriculum with no indexed videos. Update the README, dev log and V2 checklist; tag `v2.0-rag`.
- **Files:** entry point, `docs/eval_questions.md`, `README.md`, `docs/dev_log.md`.
- **Concepts:** end-to-end manual testing against acceptance criteria; recording known limitations honestly.
- **Done when:** the seven-step demo in requirements section 7 runs start to finish after a restart, and all six evaluation questions behave as expected (answer with sources, or a clear refusal).
- **Time:** 2.5–3.5 h.

## Technical risks

The two risks most likely to change the plan are the transcript format and the demo-curriculum gap; both are settled on Day 1.

| Risk | What can go wrong | Mitigation | Settled in |
| --- | --- | --- | --- |
| Transcript parsing | Files differ in format; byte-order marks; auto-captions repeat lines; some files lack titles or IDs | Inspect all 29 first; one parser for the format found; manifest supplies titles and IDs; drop consecutive duplicate lines | CP7, CP10 |
| Timestamp accuracy | No timestamps at all; caption times drift; a link points to the chunk start, not the exact sentence | Keep each chunk's first-segment time; chunks of 150–250 words keep the jump within about a minute; no `&t=` when unknown | CP7, CP10, CP13 |
| Video-ID matching | IDs are case-sensitive 11-character strings; manifest URLs come in several forms (`youtu.be`, `&t=`, `shorts/`); V1 search almost never returns library videos | Normalize every ID with one tested function; compare exact strings; curation helper for the demo curriculum | CP7, CP12 |
| Embedding performance | Embedding the full library on CPU takes minutes; Ollama may swap between the embedding model and `llama3.2:3b` | Batch requests; time 3 transcripts first; index once with upsert; demo can run on the demo curriculum's subset | CP11 |
| Curriculum-scoped search | Search leaks into unrelated transcripts; empty filter; fewer matching chunks than `k`; distance metric fixed at collection creation | `$in` filter on `video_id` with a test asserting scope; check for zero indexed videos before querying; create the collection with cosine distance from the start | CP11, CP12 |
| Small-model compliance | `llama3.2:3b` may skip citations, cite passages that were not given, or invent code | Numbered passages, strict instructions, low temperature; citations validated in code; refusal path that skips the LLM on weak retrieval | CP13 |
| Library versions | Qdrant's API has changed between releases | Pin the installed version in `pyproject.toml` and note it in the dev log | CP11 |

## Final terminal experience

The session below is illustrative: titles, IDs and timings are placeholders, and the real demo uses genuine records from the manifest.

```text
=== LearningPath AI ===
1) Create a new learning path
2) Open a saved learning path
3) Quit
> 2

Saved learning paths
1) Python for AI development · Advanced · 5 h/week · saved 2026-10-14 10:42
2) Intro to data visualization · Beginner · 3 h/week · saved 2026-10-13 18:05
> 1

Python for AI development (C# developer, 5 h/week)
Module 1: Pythonic syntax for experienced developers
  - Python Functions Deep Dive              [indexed] [library]
  - Python for C# Developers                [not indexed]
Module 2: Working with data structures and JSON
  - Python Dictionaries Explained           [indexed] [library]
...
Indexed videos in this path: 5 of 12. Q&A searches only these 5.

1) Ask a question  2) Back
> 1
Question: What's the difference between a list and a tuple, and when should I use each?

Answer:
Lists are mutable, so items can be added or changed after creation; tuples
cannot be changed once created [1]. The instructor recommends tuples for fixed
groups of values, such as coordinates, and lists for collections that grow [2].

Sources:
[1] Python Lists and Tuples Explained — 04:11
    https://www.youtube.com/watch?v=VIDEO_ID_A&t=251s
[2] Python Data Structures Overview — 12:38
    https://www.youtube.com/watch?v=VIDEO_ID_B&t=758s

Question: Show me the exact code from the decorators video.

I could not establish this from the indexed videos in this learning path.
The transcripts describe decorators but do not contain the code shown on screen.
```

Checkpoint 7 starts once the open questions in the scope section are answered.
