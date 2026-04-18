# DKSS — Distributed Knowledge Search System

A fully local, privacy-preserving organizational search system. Multiple isolated nodes each hold their own documents. A coordinator fans queries across all nodes, and a local LLM summarizes the merged results into a natural-language answer — with a Google-style web UI.

---

## What It Does

Imagine Google Search, but private, local, and for your organization. HR documents never leave HR's machine. Legal documents never leave Legal's machine. But any employee can search across all of them and get one coherent answer.

```
[Streamlit UI]  →  [FastAPI Coordinator]  →  [FastAPI Node 1 (HR docs)]
                                          →  [FastAPI Node 2 (Legal docs)]
                                          →  [FastAPI Node N ...]
```

---

## Prerequisites

Install these before proceeding:

- Python 3.10+
- [Ollama](https://ollama.com/) — local LLM server
- Git

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd DRAG
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn streamlit requests chromadb sentence-transformers pymupdf ollama pydantic
```

### 4. Pull the LLM model

```bash
ollama pull llama3.2:1b
```

---

## Ingesting Documents

Each node needs its own ChromaDB vector database built from a folder of PDFs. Run `ingest.py` once per node.

```bash
# Node 1 — e.g., HR documents
python core/ingest.py \
  --pdf-dir /path/to/hr_docs \
  --db-path ./chroma_db_node1 \
  --collection my_collection

# Node 2 — e.g., Legal documents
python core/ingest.py \
  --pdf-dir /path/to/legal_docs \
  --db-path ./chroma_db_node2 \
  --collection my_collection
```

This creates `chroma_db_node1/` and `chroma_db_node2/` in your project folder.

---

## Running the System

You need **4 terminals**, all with the virtual environment activated (`source .venv/bin/activate`).

```bash
# Terminal 1 — Node 1
DB_PATH=./chroma_db_node1 uvicorn core.node:app --port 8001

# Terminal 2 — Node 2
DB_PATH=./chroma_db_node2 uvicorn core.node:app --port 8002

# Terminal 3 — Coordinator
uvicorn core.coordinator:app --port 9000

# Terminal 4 — UI
streamlit run ui/app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Adding More Nodes

1. Ingest documents into a new ChromaDB path (e.g., `./chroma_db_node3`).
2. Start the node on a new port:
   ```bash
   DB_PATH=./chroma_db_node3 uvicorn core.node:app --port 8003
   ```
3. Add the new node URL to the `NODES` list in `core/coordinator.py`:
   ```python
   NODES = [
       "http://localhost:8001/query",
       "http://localhost:8002/query",
       "http://localhost:8003/query",  # ← add this
   ]
   ```

For **multi-machine deployment**, replace `localhost` with the actual IP address of each machine. No other changes needed.

---

## Project Structure

```
project/
├── core/
│   ├── ingest.py        ← PDF → ChromaDB pipeline (run once per node)
│   ├── node.py          ← FastAPI node server (one instance per node)
│   └── coordinator.py   ← FastAPI coordinator (orchestrates everything)
├── ui/
│   └── app.py           ← Streamlit UI (calls coordinator only)
├── .gitignore
└── README.md
```

> `chroma_db_*/` folders and PDF files are excluded from git — they stay local to each node by design.

---

## Tech Stack

| Component | Technology |
|---|---|
| PDF extraction | PyMuPDF (fitz) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector database | ChromaDB (PersistentClient) |
| Node & coordinator APIs | FastAPI + uvicorn |
| Local LLM inference | Ollama (`llama3.2:1b`) |
| Web UI | Streamlit |

Everything runs **fully locally** — no cloud, no API keys, no data leaves your machine.

---

## Known Limitations

- **Speed:** LLM inference on CPU averages 15–25 seconds. This is a hardware constraint — no GPU is used.
- **Chunking:** Fixed-size character chunking (1000 chars, 200 overlap) can split related content across boundaries. Structured documents like tables may retrieve poorly.
- **No cross-node re-ranking:** Chunks from all nodes are merged by concatenation, not by relevance score.
- **Single coordinator:** The coordinator is a single point of failure. A peer-to-peer routing protocol (like TARW from DRAG) would be the proper long-term solution.
- **Metadata queries:** Questions like "who is the author of X?" cannot be answered by semantic search alone and require metadata filtering.

---

## Development Notes

- Tested on: AMD Ryzen CPU, 8 GB RAM, no discrete GPU, Arch Linux (ML4W), Python 3.13
- Virtual environment: `.venv/` (excluded from git)
- LangChain was evaluated and discarded — direct `fitz` + manual chunking proved simpler and more reliable
- `all-mpnet-base-v2` was evaluated and discarded — 10+ minute ingestion on CPU; `all-MiniLM-L6-v2` is used instead

---

## Research Context

DKSS is grounded in a gap identified across 15 research papers on distributed and federated RAG. The most relevant is DRAG (Xu et al., 2025 — arXiv:2505.00443), which proposes peer-to-peer distributed RAG evaluated in simulation only. No existing paper simultaneously addresses:

- Real hardware implementation
- A working user interface
- Real organizational documents
- A fully local LLM
- No central document server

DKSS addresses all five.