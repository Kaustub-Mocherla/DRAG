
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os
db_path = os.getenv("DB_PATH", "./chroma_db")
collection_name = os.getenv("COLLECTION", "my_collection")
app = FastAPI()


embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=db_path)
collection = chroma_client.get_collection(collection_name, embedding_function=embedding_function)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def get_res(request: QueryRequest):
    results = collection.query(query_texts=[request.query], n_results=10)
    return {"chunks": results["documents"][0], "metadatas": results["metadatas"][0]}