# acts as a coordinator between nodes, finds the matching chunks of the query from the nodes and passes to ollama to summarise the retrived data
import requests
from ollama import chat
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
app = FastAPI()
class QueryRequest(BaseModel):
    query: str

NODES = [
    "http://localhost:8001/query",
    "http://localhost:8002/query",
]

@app.post('/search')
def search(request: QueryRequest):
    

    all_chunks = []
    all_metadatas = []

    for node in NODES:
        try:
            response = requests.post(node, json={"query": request.query}, timeout=10)
            data = response.json()
            all_chunks.extend(data['chunks'])
            all_metadatas.extend(data['metadatas'])
        except Exception:
            pass  # this skips the nodes that are unreachable/crashed

    sources = list(set(m.get("source", "") for m in all_metadatas if m))

    context = "\n\n".join(all_chunks[:5])

    prompt = f"""Answer the question using ONLY the context below. If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question:
{request.query}

Answer:"""

    def generate():
        stream = chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )
        for chunk in stream:
            yield chunk['message']['content']

    return StreamingResponse(
    generate(),
    media_type="text/plain",
    headers={"X-Sources": ",".join(sources)}
)