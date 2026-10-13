## [Python] Retry loop ran the model twice
- Problem: text and return were outside the for loop, so every run called the model twice (~60 s).
- Found: only the last response was used; a bad answer crashed instead of retrying.
- Lesson: indentation decides what a loop repeats; return inside the loop is what ends it.

## [Setup] Edits did nothing until I saved
- Problem: python -m ran but printed nothing.
- Lesson: Python runs the file on disk, not what's on screen. Turn on auto-save.

## [YouTube] API keys leak through URLs
- Problem: requests errors can contain the full URL, which includes the key.
- Lesson: wrap failures in my own RuntimeError and never print resp.url.

## [Setup] Google Cloud settings belong to a project
- Problem: my key and the enabled API were in a different project than I thought.
- Lesson: API enablement and keys are per project; check the project name first.

## [Prompt] Module 4 drifted off the goal
- Problem: When requesting a curriculum for "Python for spreadsheets", the model added a deployment module which was outside the requested goal.
- Change: added "Stay focused on the learner's goal" to the prompt.
- Result: (fill in)

## [Idea] Pre-flight topic check (not built)
- Problem: gibberish input produces a confident curriculum.
- Idea: ask the LLM whether the topic + goal make sense before generating; optionally
  confirm with a YouTube search and a result-count threshold.
- Risks: a small model may misjudge; search engines return results for almost anything.
- Status: parked as NICE TO HAVE; the confirmation step covers the common cases.

## [Prompt] The model invents a curriculum for gibberish
- Problem: input "fas asdfwedvszc44" produced a confident 4-module "FAS Mastery" plan.
- Found: schema validation checks shape, not meaning; the model has no way to refuse.
- Lesson: add a confirmation step; document as a limitation.

## [Setup] ChromaDB crashed Python on insert
- Problem: upsert killed Python with exit code -1073741819 and no traceback.
- Found: Windows access violation (0xC0000005) inside ChromaDB's native code; same crash on Python 3.12 with hand-made vectors, so not my code or the Python version.
- Lesson: echo $LASTEXITCODE when a script stops silently; a big negative number means a native crash, not a Python error.

## [RAG] Switched the vector store to Qdrant local mode
- Problem: ChromaDB unusable on Windows; a NumPy index worked but wasn't a real vector database.
- Change: qdrant-client local mode stored in data/qdrant/, no server or Docker.
- Result: smoke test with nomic-embed-text passed; the video_id filter excludes videos outside the curriculum.

## [Qdrant] Point IDs must be numbers or UUIDs
- Problem: IDs like "VIDEO_ID_0007" are rejected.
- Lesson: uuid5(namespace, "VIDEO_ID_0007") turns the name into the same UUID every run, so re-indexing overwrites instead of duplicating (3 points after two runs).