# DRAG

Distributed Retrieval-Augmented Generation (DRAG) is a lightweight local knowledge search system.
It ingests PDF documents into ChromaDB, queries multiple retrieval nodes, and uses Ollama to
stream a concise answer back to the Streamlit UI.

## Overview

The project is organized into three parts:

- `core/ingest.py` ingests PDFs into a persistent ChromaDB collection.
- `core/node.py` exposes a retrieval API for one Chroma-backed node.
- `core/coordinator.py` gathers results from all nodes and streams a final answer.
- `ui/app.py` provides the Streamlit frontend for searching the knowledge base.

## Features

- PDF ingestion into a local vector database.
- Distributed retrieval across multiple nodes.
- Streaming answer generation through Ollama.
- Simple Streamlit interface with source tracking.

## Requirements

- Python 3.10 or newer.
- [Ollama](https://ollama.com/) installed and running locally.
- The model `llama3.2:1b` pulled in Ollama, or another compatible chat model.

## Installation

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install streamlit fastapi uvicorn requests ollama chromadb pymupdf sentence-transformers
```

## Ingest Documents

Place your PDF files in a folder and build a ChromaDB collection:

```bash
python core/ingest.py --pdf-dir /path/to/pdfs --db-path ./core/chroma_db --collection my_collection
```

## Run the System

Start the retrieval node(s), coordinator, and UI in separate terminals.

### 1. Start retrieval nodes

By default, `core/node.py` reads `DB_PATH` and `COLLECTION` from the environment.

```bash
DB_PATH=./core/chroma_db COLLECTION=my_collection uvicorn core.node:app --port 8001
DB_PATH=./core/chroma_db COLLECTION=my_collection uvicorn core.node:app --port 8002
```

### 2. Start the coordinator

```bash
uvicorn core.coordinator:app --port 9000
```

### 3. Start the Streamlit UI

```bash
streamlit run ui/app.py
```

## How It Works

1. The UI sends a query to the coordinator.
2. The coordinator queries each retrieval node.
3. Each node searches its ChromaDB collection and returns matching chunks.
4. The coordinator sends the best chunks to Ollama for final response generation.
5. The answer is streamed back to the UI along with source metadata.

## Project Structure

```text
README.md
core/
	ingest.py
	node.py
	coordinator.py
	chroma_db/
ui/
	app.py
```

## Configuration

- `DB_PATH`: Path to the ChromaDB directory used by a node.
- `COLLECTION`: Chroma collection name to query.

## Notes

- The current coordinator expects nodes at `http://localhost:8001/query` and `http://localhost:8002/query`.
- The UI expects the coordinator to be available at `http://localhost:9000/search`.
- If you change ports or paths, update the corresponding URLs in the source files.

