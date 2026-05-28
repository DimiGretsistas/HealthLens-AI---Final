# HealthLens AI

AI-powered YouTube Health Video Q&A Assistant built with FastAPI, LangChain, ChromaDB, OpenAI, and Vanilla JavaScript.

Users can:

* Ask questions about a pasted YouTube video
* Ask questions across a preloaded video library
* Use voice input (speech-to-text)
* Listen to AI answers (text-to-speech)
* View timestamped source citations from videos

---

# Features

* YouTube transcript retrieval using Supadata
* Retrieval-Augmented Generation (RAG)
* Chroma vector database
* Multi-video library retrieval
* Timestamp source generation
* AI agent with multiple tools
* LangChain integration
* LangSmith tracing and evaluation
* Speech recognition
* Text-to-speech
* FastAPI backend
* Vanilla JavaScript frontend
* Render deployment

---

# Model

The project uses **GPT-4o mini** for:

* answer generation
* tool routing
* LLM-as-a-judge evaluation

---

# Tech Stack

## Backend

* Python
* FastAPI
* LangChain
* OpenAI
* ChromaDB
* Supadata
* Whisper (fallback transcription support)

## Frontend

* HTML
* Tailwind CSS
* Vanilla JavaScript

## AI / RAG

* OpenAI Embeddings
* Chroma Vector Store
* LangChain Agents
* Retrieval-Augmented Generation (RAG)

---

# Agent Tools

The assistant uses a LangChain-based agent/router with multiple tools:

* `video_qa_tool`
* `summary_tool`
* `ingredient_extraction_tool`
* `macro_calculator_tool`
* `health_safety_tool`
* `meal_suggestion_tool`
* `shopping_list_tool`

---

# Project Structure

```txt
backend/
frontend/
chroma_db/
requirements.txt
README.md
```

---

# Main Functionality

## 1. Single Video Mode

Users paste a YouTube URL.

The system:

1. Loads transcript
2. Splits transcript into chunks
3. Stores embeddings in ChromaDB
4. Retrieves relevant chunks
5. Generates grounded AI answers
6. Returns timestamp sources

---

## 2. Video Library Mode

The system supports a preloaded health video library.

Users can ask:

* nutrition questions
* sleep questions
* sauna questions
* longevity questions
* fast food questions

without uploading a video.

---

# AI Features

## RAG Pipeline

The assistant uses Retrieval-Augmented Generation:

* transcript chunking
* embedding generation
* vector similarity search
* grounded answer generation

## Hallucination Protection

The assistant avoids unsupported answers.

If information is missing:

```txt
The preloaded video library does not contain enough information.
```

## Source Citations

Answers include:

* YouTube timestamps
* direct source links
* originating video title

---

# Speech Features

## Speech-to-Text

Users can ask questions using microphone input.

## Text-to-Speech

The assistant can read answers aloud.
Speech can also be stopped during playback.

---

# Evaluation

The project uses an **LLM-as-a-judge** evaluation approach with **GPT-4o mini**.

The evaluator scores each answer using:

* Faithfulness
* Relevance
* Clarity
* Hallucination Safety

The evaluation compares:

* the user question
* the generated answer
* the retrieved timestamp sources

The project also uses LangSmith for:

* tracing
* debugging
* latency monitoring
* token monitoring
* evaluation logging

---

# Deployment

Frontend and backend are deployed on Render.

---

# Installation

## Clone Repository

```bash
git clone <repo-url>
cd HealthLens-AI---Final
```

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_key
SUPADATA_API_KEY=your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

---

# Run Backend

```bash
uvicorn backend.api:app --reload
```

---

# Evaluation Commands

## Single Video Evaluation

```bash
python -u -m backend.evaluate_openai
```

## Video Library Evaluation

```bash
python -u -m backend.evaluate_library_openai
```

---

# Current Capabilities

* Single-video YouTube Q&A
* Multi-video library retrieval
* Voice input
* Voice output
* Timestamp citations
* Agent-based routing
* LangSmith tracing
* Automated evaluations
* Hallucination protection
* Web deployment

---

# Future Improvements

* improved cross-video reasoning
* streaming responses
* authentication
* larger video libraries
* mobile optimization

---

# Author

Dimitrios Gretsistas
