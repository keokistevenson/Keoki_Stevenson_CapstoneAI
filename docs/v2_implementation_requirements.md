# LearningPath AI — Final V2 Requirements and Implementation Planning

We've finalized the direction for Version 2. Please use these instructions to revise the existing implementation plan and prepare us to begin coding.

**Do not create a separate, unrelated project or restart V1.** Preserve our existing implementation plan, completed checkpoints, project structure, and guided pair-programming approach.

## 1. Current status

Version 1 is complete and working end to end.

V1:
- Accepts a learner profile (topic, experience level, learning goal, hours per week).
- Uses local Ollama to generate a four-module curriculum with learning objectives.
- Uses the YouTube Data API to find real videos.
- Displays the resulting curriculum and recommended videos in the terminal.

We also have 29 Python-related YouTube transcripts saved locally. These will form our initial transcript library.

## 2. What we're building in V2

**V2 will allow learners to save a curriculum, reopen it later, and ask questions about the educational content of the videos associated with that curriculum.**

This is a genuine Retrieval-Augmented Generation (RAG) extension to V1.

The learner asks questions. Ollama answers using relevant passages retrieved from indexed video transcripts.

We are NOT building an automatic quiz generator in V2.

## 3. Required user workflow

### Option A — Create a new learning path

1. The learner enters their profile.
2. The existing V1 workflow generates the curriculum and finds YouTube videos.
3. The learner can save the resulting curriculum, including its profile, modules, objectives, and video recommendations.
4. The saved curriculum receives a unique identifier and can be reopened without calling Ollama or the YouTube API again.

### Option B — Open an existing learning path

1. The application lists saved curricula.
2. The learner selects one.
3. The application loads its modules, objectives, and previously recommended videos.
4. The learner can review the curriculum and continue studying without regenerating it.

### Option C — Ask questions about saved learning material

1. The learner opens a saved curriculum.
2. The application identifies which of its recommended videos have indexed transcripts.
3. The learner asks a natural-language question.
4. The application searches relevant transcript chunks across ALL indexed videos belonging to that saved curriculum.
5. Retrieved passages are provided to Ollama as context.
6. Ollama generates an answer grounded in those passages.
7. The application displays:
   - The answer.
   - The source video title.
   - The relevant timestamp, when available.
   - A clickable YouTube link that starts at the relevant timestamp.
8. If several videos contribute relevant information, display multiple source references where appropriate.
9. If the available transcripts do not support an answer, clearly state that the information could not be established from the indexed material.

**Important:** RAG retrieval must be restricted to videos associated with the selected saved curriculum. It must not silently search all 29 transcripts and present unrelated content as part of that curriculum.

## 4. Technical requirements

### Curriculum persistence

Use simple JSON file storage unless you identify a compelling reason otherwise.

- Save complete learning paths, including video metadata and YouTube video IDs.
- Support listing and loading saved paths.
- Avoid unnecessary database infrastructure.
- Reuse existing Pydantic models where practical.
- Keep the implementation easy to understand and test.

### Transcript indexing

- Read the existing transcript files.
- Extract video titles, YouTube URLs/IDs, and timestamps where available.
- Split transcript content into meaningful chunks.
- Generate embeddings using a suitable local embedding model.
- Store embeddings, text chunks, and metadata in a persistent local vector database.
- Index the transcripts once and reuse the index.
- Preserve source metadata so retrieved passages can be traced to the correct video and approximate timestamp.

### Curriculum-to-transcript association

- Use YouTube video IDs as the primary matching identifier.
- For the demonstration, create or save at least one realistic Python curriculum containing several videos that exist in our indexed transcript library.
- Use genuine video IDs and metadata, not fabricated YouTube records.
- Videos without indexed transcripts remain valid curriculum recommendations but do not participate in transcript-based Q&A.
- Do not automatically scrape or download additional transcripts.

### RAG question answering

- Search across all indexed transcripts associated with the currently selected saved curriculum.
- Retrieve relevant passages through semantic vector search.
- Supply the passages and learner's question to local Ollama.
- Instruct Ollama to ground its answer in the supplied material.
- Avoid attributing information to videos when it is not supported by the transcript.
- Display source titles and relevant timestamped links.
- Handle missing transcripts, weak retrieval, and insufficient evidence gracefully.

### Timestamped YouTube links

Use a URL such as:

`https://www.youtube.com/watch?v=VIDEO_ID&t=251s`

where 251 represents the timestamp in seconds.

If reliable timestamps are unavailable, link to the video without a timestamp.

We should preserve timestamps during transcript ingestion rather than attempting to reconstruct them afterward.

## 5. Transcript limitations

YouTube transcripts frequently omit code shown visually on screen.

The RAG system must not invent code examples or claim to know exactly what appeared in a video if that information is absent from the transcript.

Focus the initial Q&A experience on conceptual explanations, instructor discussions, and examples actually supported by transcript text.

The system should acknowledge when the transcript does not contain enough information.

## 6. Explicitly excluded from V2

Do NOT add:

- Streamlit or another new user interface.
- Automatically generated quizzes or grading.
- Automatic curriculum rewriting or refinement.
- Automatic transcript scraping/downloading.
- Agent frameworks or multi-agent workflows.
- User authentication.
- Relational database infrastructure.
- Cloud deployment.
- Unnecessary architectural abstractions.

These may be considered in later versions.

## 7. Demonstration

Use a Python-focused saved curriculum because our existing transcript collection primarily covers Python.

A suitable scenario:

- Topic: Python for AI development.
- Learner: Experienced C# developer.
- Goal: Learn Python skills relevant to LLM and RAG application development.
- Available study time: Five hours per week.

The demonstration should show:

1. A curriculum created using V1.
2. The curriculum saved to disk.
3. The application closed and restarted.
4. The same curriculum reopened without regeneration.
5. Several indexed videos associated with the saved curriculum.
6. A learner question answered using retrieved passages from the associated transcripts.
7. Source video titles and clickable timestamped YouTube links.

Use a small subset of transcripts during initial development before indexing the full library.

## 8. Implementation constraints

We have approximately three focused development days for V2.

Prioritize a complete working vertical slice over additional features.

Use the existing Python environment, uv, VS Code, and local Ollama setup.

Prefer simple, well-supported libraries. Avoid adding LangChain merely for abstraction if direct integration is clearer.

Continue guided pair programming:

- Give me small, manageable coding steps.
- Explain Python-specific concepts and unfamiliar library behavior.
- Do not reteach general programming concepts I already understand from C#/.NET.
- Include focused tests and debugging checkpoints.
- Do not spend excessive time on peripheral tooling.
- Keep implementation progress visible in our development log.

## 9. What I want you to do now

Review the existing implementation plan and revise only the V2 portion.

Maintain continuous checkpoint numbering beginning after the completed V1 checkpoints.

For each V2 checkpoint, provide:

- Its purpose.
- What we're building.
- Files or modules affected.
- Important concepts I will learn.
- A specific, testable completion criterion.
- A realistic time estimate.

Identify any technical risks, especially transcript parsing, timestamp accuracy, video-ID matching, local embedding performance, and vector search restricted to the selected curriculum.

Also provide a clear example of the final terminal experience.

**Do not begin coding yet. Produce the revised implementation plan first so I can review it.**

Keep the plan achievable in approximately three focused development days. If any requirement threatens that schedule, flag it and recommend the smallest practical adjustment rather than silently expanding the scope.