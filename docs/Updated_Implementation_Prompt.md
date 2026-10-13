# LearningPath AI — Updated Implementation Plan Prompt

You are an experienced Python instructor, software architect, and AI application development mentor.

Help me update and maintain an incremental implementation roadmap for LearningPath AI, beginning with completion of my CAP 942 capstone (Version 1), followed by a deliberately small RAG extension (Version 2). Do not treat this as a request to implement all versions immediately.

PROJECT IDEA:
LearningPath AI (formerly YouTube University) is an AI-powered learning path generator that creates a personalized curriculum using educational videos available on YouTube. A user enters a subject or skill they want to learn, and the application asks a small number of follow-up questions about factors such as their current experience level, learning goal, and available study time. An open-source LLM uses this information to generate an ordered curriculum consisting of learning modules, objectives, and suggested YouTube search queries. The application then uses the YouTube Data API v3 to search for relevant educational videos, filters and ranks the results, and organizes selected videos into a structured learning path for the user.

VERSION STRATEGY (STRICT SCOPE BOUNDARIES):
- Version 1 — CAP 942 submission: a working terminal-based curriculum generator using local Ollama, Pydantic structured output, and YouTube Data API video discovery. Complete, test, document, and tag this version before starting RAG. No transcript ingestion, embeddings, vector database, Streamlit, or assessment system is required in V1.
- Version 2 — smallest useful RAG extension, AFTER V1 submission: ingest a small set of legally and technically accessible transcripts or user-supplied transcript text; chunk the text; create embeddings; store/retrieve chunks in a local vector database; answer questions using retrieved excerpts and show source attribution. Begin with a tiny, reproducible dataset and a terminal interface. No autonomous agents, generalized crawling, bulk transcript downloading, full learning management system, or sophisticated UI.
- Version 3 — future learning platform: Streamlit UI, persistent curricula/library, learner progress, and later FAE-inspired assessments (question generation, attempts, scoring, reporting). Plan integration seams but do not implement FAE integration before the V2 RAG workflow works.
- Later portfolio hardening: expanded evaluation, CI/CD, deployment, and security/reliability refinements. Add essential tests and documentation continuously; do not postpone all quality work.
Keep the code modular by responsibility rather than creating parallel codebases for each version. Preserve V1 as a Git tag such as `v1.0-capstone`; continue sequential checkpoint numbers across versions. Do not build speculative V2/V3 infrastructure into V1.

MY CURRENT EXPERIENCE LEVEL:
INTERMEDIATE

The implementation plan should therefore:

- Assume I understand general programming concepts.
- Do not spend excessive time teaching basic programming concepts that
  transfer directly from other languages.
- Explain Python-specific concepts when they matter.
- Explain LLM/AI architecture and integration decisions rather than
  treating them as magic.
- Teach me how the components communicate with each other.
- Prefer learning by building and testing small pieces.

PREFERRED APPLICATION FORMAT:
PYTHON SCRIPT — command-line/terminal application for V1 and V2; Streamlit is a later V3 interface choice.

AVAILABLE COMPUTER OR DEVELOPMENT ENVIRONMENT:
Windows 10 Pro, 12 GB RAM, CPU-based local model execution, no dedicated GPU assumed. Development will be done locally using Visual Studio Code.

CURRENT IMPLEMENTATION STATUS (VERIFY AGAINST THE ACTUAL REPOSITORY):
- Checkpoint 1: Local Ollama connection tested.
- Checkpoint 2: YouTube Data API search tested independently.
- Checkpoint 3: Pydantic models, prompt construction, and `generate_curriculum()` implemented in part; retry/error-handling work is ongoing. `build_prompt(profile)` expects a `topic` key; the scratch experiment deliberately omitted it and produced `KeyError` before Ollama was called.
- Checkpoints 4–6: Not yet verified complete.
- Do not discard working code, restart earlier milestones, or assume a new package name is required for rebranding.

CAPSTONE REQUIREMENTS:

--- BEGIN OFFICIAL CAP 942 REQUIREMENTS ---

CAP 942 - Capstone Project: AI Application Development Guidelines
________________________________________
Project Overview
This capstone guides you through building a small but functional AI application using existing open-source LLMs. You will not train machine learning or deep learning models. Instead, you will learn how to run models, build a simple workflow, and produce a working prototype.
The capstone has three phases:
Phase 1: Research & Self‑Study
You will explore beginner-friendly, open-source tools such as:
●	Ollama (run local models like Llama 3, Mistral, Gemma)
●	GPT4All (cross‑platform local LLM ecosystem)
●	Hugging Face (free, open-source models; Transformers; text pipelines)
●	LangChain (LLM orchestration framework)
During this phase, you will:
●	Explore how LLMs work at a high level (no ML/DL training required).
●	Run a model locally.
●	Review documentation, tutorials, and sample applications.
●	Select a project idea and draft a proposal.
○	In a proposal, you must specify the problem statement and how you plan to solve it using AI.
Visit this resource for upskilling and research: Research & Self-Study

Phase 2: AI Application Development
You will design and build a functional application using an existing LLM that includes:
Minimum Requirements:
●	Use one open-source LLM
●	Accept user input
●	Produce LLM-generated output
●	Run as a:
○	Python script
○	Jupyter/Colab notebook
○	Small web app (Flask/Streamlit)
○	Simple API (FastAPI)
●	Database (vector or non-vector) if your project includes retrieval or memory features.
Optional Enhancements (Not required but allowed)
●	Vector search
●	Basic retrieval
●	Multi-step chains
●	Multiple tools or models
Keep the scope small. Functionality is more important than complexity.

Phase 3: Chatbot Deployment & Presentation
You will:
●	Run your application locally, in a notebook, or through a lightweight UI
●	Prepare a 5–10 minute presentation that walks through:
○	What your app does
○	User input → LLM → output
○	Tools used
○	Challenges and next steps
○	Application Workflow diagram.
●	Deploy on Github with instructions.

Project Goal
Build a small but complete AI application that:
●	Solves a clear problem
●	Uses at least one open-source LLM
●	Runs end-to-end with input, processing, and output
●	Demonstrates workflow design and prompt engineering
●	Includes clear documentation
This project does not require:
●	ML model training
●	Custom neural networks
●	GPUs
●	Paid APIs

Suggested Project Types
●	All project types should use pre-trained open-source LLMs such as Ollama or GPT4All or Hugging Face models or LangChain pipelines and any other open-source framework and model.
●	Learners will not build or train ML/DL models.
Beginner (Recommended)
●	Text Summarizer
●	Email or Message Rewriter
●	Simple Chat Assistant (LLM chatbot)
●	Text Translation App
●	Content Generator (blog outline, study notes)
Intermediate
●	Resume Screener with scoring
●	Movie or Book Recommendation Assistant (LLM-based)
●	Coding Helper (explanations, hints)
Advanced / Optional
●	Document Q&A App (simple retrieval)
●	RAG app with ChromaDB or FAISS
●	Multi-step chain using LangChain

See the full idea list for more examples.
Click here to see the list of project ideas: AI Project Ideas to Kickstart Your Journey

________________________________________
Tools & Technologies Learners Can Use
Learners may use any free or open-source AI tools. Below is an approved list of recommended frameworks, libraries, and platforms.
Programming Languages
●	Python
AI/LLM Frameworks and Libraries
●	Hugging Face Transformers (free, open-source models)
●	LangChain (orchestrating workflows with open-source models)
●	Ollama (local LLM runner for models like Llama 3, Mistral)
●	Llama.cpp (run LLMs locally on CPU)
●	GPT4All (free local model ecosystem)
●	Haystack (for retrieval-augmented generation / RAG)
NLP / Text Processing Tools
●	spaCy (for tokenization and text processing)
●	NLTK (fundamental NLP utilities)
●	SentenceTransformers (embeddings for semantic search, clustering)
Text Transformation & Document Processing Tools
●	Sentence-Transformers (embeddings for similarity search, clustering, semantic analysis)
●	PyPDF2 / pypdf (extract text from PDF files)
●	pdfplumber (more advanced PDF text extraction)
●	BeautifulSoup (extract and clean text from HTML pages)
●	Unstructured (document ingestion for text-based LLM apps)
●	Tiktoken (token counting and processing for LLM inputs)
●	ChromaDB / FAISS (vector databases for RAG-based search)

Model Hosting or Execution Options
●	Local execution on student computers
●	Google Colab (free)
●	Jupyter Notebook
●	Kaggle Notebooks (free GPU/TPU)
Application Development Frameworks (Beginner-Friendly)
Students may use any of the following to build their AI applications:
●	Python (recommended)
●	FastAPI (build lightweight APIs for LLM-powered apps)
●	Flask (simple web framework for prototypes)
●	Streamlit (quick UI for AI demos and dashboards)
Vector Databases (for RAG and search)
Students can use any free local vector database, including
●	ChromaDB (recommended, easy to use)
●	FAISS (local vector search library)
●	LanceDB (lightweight and Python-friendly)
●	Weaviate (local version optional)
System Requirements for Local Models (will depend on application as well)
●	Minimum: 16 GB RAM (Recommended: 32 GB RAM.)
●	Use 3B–7B models for best performance.
●	If your device cannot run local models, use Colab or Hugging Face Inference.

Project Deliverables
Each learner must submit:
1. Project Proposal (1–2 pages)
●	Problem statement
●	Why this project matters
●	Tools/frameworks chosen
●	Expected output or user interaction
2. Working AI Application
Choose any of the following formats:
●	Python script
●	Jupyter/Colab notebook
●	Flask/FastAPI app
●	Streamlit UI
●	Command-line tool
It must run without paid APIs.
3. Data or Input Sources (if applicable)
Only required if your project uses one.
Include:
●	Name/source of the data (public or original)
●	What the data contains
●	Steps you took to preprocess it
●	For simple LLM apps without datasets, you may skip this section.
4. Final Presentation (5–10 minutes)
You must prepare a clear and concise presentation demonstrating your application. In addition to the live demo, you are also required to submit a supporting project document that includes the following:
Required Final Documentation
●	Application Overview
o	Purpose of the application
o	The problem it solves
o	Intended users
●	Technical Workflow Diagram
o	A visual diagram showing:
▪	User input flow
▪	LLM interaction (Ollama, GPT4All, Hugging Face, etc.)
▪	Any retrieval or vector database components
▪	API or UI flow (FastAPI, Flask, Streamlit)
▪	Output handling
●	Tools, Libraries & Frameworks Used
o	LLM(s) selected
o	Libraries such as LangChain, Sentence-Transformers, pypdf, etc.
o	Frameworks (FastAPI, FlaskAPI, Streamlit)
o	Vector database (ChromaDB, FAISS, LanceDB, etc.)
●	Application Architecture Description
o	Explanation of major components
o	Description of how data flows through the system
●	Features & Functionality
o	List of key features
o	How the LLM powers each feature
●	Challenges & Lessons Learned
o	Development obstacles
o	How issues were solved
________________________________________
Rubrics Criteria
Total = 600 Points.
1. Proposal (60 points)
●	The proposal should clearly state the problem and its value.
●	The proposal should clearly define the tools, choose a suitable model, and outline a workflow plan.
2. Functional Application (210 points)
●	Application runs end-to-end without errors.
●	Required LLM functionality implemented.
●	Code readability, structure, and documentation within code.
●	Appropriate scope and completeness of features.
3. Documentation & Presentation (30 points)
●	Complete written project documentation.
●	Accurate workflow diagram explaining system flow.
●	Clear, professional final presentation demonstrating the system.

________________________________________
Success Tips for Students
●	Start small and expand only if time allows.
●	Choose a problem that interests you.
●	Use existing pre‑trained models when needed—no need to train massive models.
●	Document everything clearly.
●	Test your application with real or realistic inputs.
________________________________________
Submission Requirements
●	Submit all files through Canvas (ZIP or GitHub link).
o	Includes all required documents
●	Follow the naming convention: FirstName_LastName_CapstoneAI.
●	Ensure all code runs without requiring paid APIs.


--- END OFFICIAL CAP 942 REQUIREMENTS ---

GOAL:

Create the complete content for an updated `implementation_plan.md` file that preserves V1 completion checkpoints and adds a separate, small V2 RAG roadmap, with later V3 ideas clearly marked as deferred. This is a planning and teaching document, not a request for finished application code.

The implementation plan must align directly with the supplied capstone requirements. Treat those requirements as the primary source of truth.

Finish the Version 1 capstone first, using the smallest complete end-to-end application that satisfies the class requirements. Version 2 begins only after V1 is complete and preserved. Version 2 has no fixed deadline; keep its first working RAG increment small. Do not expand the capstone deliverables to include RAG.

IMPORTANT TEACHING REQUIREMENTS:

This plan must teach me how to develop the project. Do not create the complete application for me.

Assume I already understand general programming and software development concepts, but I am still learning Python-specific practices and AI/LLM application development. Focus explanations on unfamiliar Python and AI concepts rather than reteaching basic programming concepts.

Do not provide:

- A complete working project
- A complete repository
- Full production-ready application files
- A fully completed `main.py`, `app.py`, or notebook
- Large blocks of code that I can submit without understanding
- Paid APIs or services
- Machine learning or deep learning training

You may provide three to five short, isolated code examples that demonstrate individual concepts. Each example must:

- Be no longer than approximately 25 lines
- Teach only one concept
- Include comments explaining the important lines
- Contain a `TODO` showing what I must complete
- Avoid connecting all parts into a finished application
- Be followed by an explanation and a small practice task

Use placeholders for project-specific logic so that I must make decisions and write parts of the code myself.

PLANNING PROCESS:

Before creating the final plan, ask me up to five clarification questions if important technical or project details are missing.

Do not ask clarification questions about decisions that are already specified in this prompt. Only ask questions when the missing information would materially affect the implementation plan.

If an idea is too large for the capstone or V2, reduce it to a realistic minimum. Separate required V1 deliverables, V2 RAG tasks, and deferred V3/portfolio enhancements.

REQUIRED SECTIONS FOR `implementation_plan.md`:

1. Project Title

2. Project Summary
   - One-paragraph description
   - One-sentence value proposition

3. Problem Statement
   - Problem being addressed
   - Why it matters
   - Intended users

4. Capstone Requirement Alignment
   - Create a table containing:
     - Capstone requirement
     - How the application will meet it
     - Evidence or deliverable that will demonstrate completion

5. Project Scope
   - Minimum viable product features
   - Features that are outside the initial scope
   - Optional enhancements to consider only after the MVP works
   - Clearly distinguish V1 capstone, minimal V2 RAG, and deferred V3 features

6. Recommended Technology Stack
   - Open-source LLM
   - Method for running the model
   - Python libraries
   - Application framework
   - No database required for V1; recommend a small local vector store only for V2 RAG, explaining the tradeoff
   - Development tools
   - Explanation of why each tool is appropriate
   - Hardware considerations and a smaller-model alternative if necessary
   - Use `uv` for Python project and dependency management unless the selected environment requires something else
   - Identify which required tools must be installed or configured before development begins, but place the step-by-step setup instructions in the development milestones

7. Application Workflow
   - Explain the V1 flow and a separate V2 retrieval-and-answering flow without conflating them
   - Include a Mermaid workflow diagram
   - Clearly identify where the open-source LLM is used, and distinguish LLM generation from embedding and retrieval

8. Application Architecture
   - Major components
   - Responsibility of each component
   - How information moves between components
   - Where errors should be handled

9. Proposed Project Structure
   - Show a recommended folder and file structure
   - Explain the purpose of each file
   - Do not write the completed files
   - Follow practical Python best practices for file organization and code modularization appropriate to a small capstone project. Separate components when they have clearly different responsibilities, but avoid unnecessary abstraction, excessive files, design patterns, or architectural layers.

10. Step-by-Step Development Milestones

For each milestone, include:

   - Learning objective
   - Concepts I should review
   - Development tasks
   - A small coding exercise
   - Testing checkpoint
   - Acceptance criteria
   - Common mistakes
   - “What I need to build myself”
   - “How I will know it works”

Build incrementally. Continue from existing V1 code rather than restarting setup. Finish the V1 end-to-end flow and class deliverables first. Then add the smallest V2 RAG slice, with a working checkpoint after each new component. Do not add Streamlit or assessments to the V2 milestones.

Preserve the original V1 environment/setup milestone as historical context, but do not instruct me to repeat completed setup. First identify current status and any remaining V1 tasks. For the first V2 milestone, verify existing `uv`, Ollama, Python environment, and the selected embedding/vector-store tools with short smoke tests. Install only what the next milestone needs.

Prioritize reaching a basic end-to-end working version of the application as early as possible. Refinements and optional enhancements should come only after the basic workflow works.

11. Guided Code Examples
   - Provide only three to five short examples
   - Demonstrate isolated concepts such as:
     - Collecting and validating user input
     - Calling an open-source LLM
     - Creating a reusable function
     - Processing a model response
     - Handling one common error
   - Do not combine the examples into a finished application

12. Prompt-Engineering Plan
   - Purpose of the system prompt
   - Information the user will provide
   - Expected response format
   - One example prompt template with placeholders
   - Methods for reducing unclear or unsupported responses

13. Testing Plan
   - Unit or component tests
   - End-to-end testing
   - At least five realistic V1 test cases and a small separate set of V2 RAG tests
   - Expected behavior for each test
   - Invalid-input and error-handling tests
   - Test external dependency failures, including unavailable local LLM/model and YouTube API errors
   - A simple method for evaluating V1 curriculum quality and V2 retrieval/answer grounding using a handful of known questions and expected source passages

14. Privacy, Security, Accessibility, and Responsible-AI Considerations
   - Relevant risks
   - Project limitations
   - Ways to reduce those risks
   - Claims the application should not make

15. Documentation and GitHub Plan
   - README sections
   - Setup instructions
   - Dependency documentation
   - Instructions for running the application
   - Example inputs and outputs
   - GitHub submission checklist
   - Recommend meaningful Git commit checkpoints throughout development so commits represent small, logical units of completed work rather than large blocks of unrelated changes. Include suggested commit points and concise example commit messages in the development milestones.

16. Presentation Plan
   - Suggested structure for a 5–10 minute presentation
   - Live demonstration sequence
   - Workflow diagram
   - Challenges and lessons learned
   - Possible next steps

17. Suggested Timeline
   - Divide the project into manageable development sessions
   - Prioritize completing the V1 capstone promptly; give V2 its own short, flexible development sessions without assuming a fixed deadline
   - Complete, test, document, and Git-tag V1 before beginning V2; stop after the minimal working RAG extension before considering V3

18. Definition of Done
   - Provide separate definitions of done: V1 aligned with the capstone rubric; V2 focused on a reproducible, source-grounded RAG question-answering workflow

Use clear language appropriate for my experience level. Explain unfamiliar technical terms the first time they appear. Recommend a practical starting point and include specific checkpoints where I should stop, test my work, and confirm that I understand it before continuing.

IMPORTANT FINAL INSTRUCTIONS:
- Do not expand Version 1 beyond its capstone MVP. The official CAP 942 requirements above apply to the V1 submission, not as a demand to finish RAG for class.
- Include a clearly separate Version 2 roadmap, but do not imply V2 work is needed to complete the capstone.
- Preserve checkpoint continuity. Treat the existing checkpoints as: 1 Ollama connection (completed); 2 YouTube API search (completed); 3 Pydantic curriculum generation/error handling (in progress); 4 curriculum-to-video integration; 5 end-to-end terminal application; 6 tests/documentation/presentation. Begin V2 at checkpoint 7 and adjust only after checking actual repository state. Never mark an unverified step complete.
- Current code uses `src/youtube_university/llm.py` and `src/youtube_university/youtube.py`, `uv`, local Ollama `llama3.2:3b`, Pydantic `Curriculum`/`Module`, and a `scratch/` folder for experiments. The public product name can change to LearningPath AI without requiring immediate Python package/module renaming. Do not invent completed integrations or files.
- V2 minimal acceptance scenario: a small permitted/user-supplied transcript collection is indexed locally; the user asks a question; the system retrieves relevant chunks, generates an answer using those chunks, and identifies the supporting source; it admits insufficient evidence rather than inventing an answer. Explain that YouTube Data API v3 does not provide general public transcript access to arbitrary videos; design a legal, dependable fallback rather than relying on brittle scraping.
- For V2 choose one small, practical embedding approach and one local vector store appropriate for CPU/12 GB RAM, but explain alternatives briefly. Avoid requiring paid APIs, a GPU, LangChain, or agents without a demonstrated need.
- Engineering workflow: keep `scratch/` Git-ignored for exploratory code; commit focused automated tests under `tests/`; keep `docs/dev_log.md` for meaningful observations/decisions; use Ruff formatting, small logical Git commits, and mocks for external LLM/API dependencies when appropriate. Don't let documentation/testing ceremonies block the first working vertical slice.
- Teach through pair programming: give small tasks, let me implement them, explain Python-specific syntax and AI concepts, and use short experiments and debugging checkpoints. Do not provide full project files or a massive code dump. Distinguish what's already built from what is proposed.
- Streamlit and FAE-inspired question generation, scoring, progress, and reporting belong to Version 3 after the minimal RAG system works. Preserve a note about reusing FAE assessment concepts, but do not redesign or merge its database yet.
- Maintain one repository and one versioned roadmap, with V1 Git-tagged for reproducibility. Separate version-specific checklists and avoid resetting checkpoint numbers.