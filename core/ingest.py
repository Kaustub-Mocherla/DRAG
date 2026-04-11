import fitz
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pathlib import Path
directory = Path("/home/ghostface/Desktop/23STUCHH011056/Special_porject/Papers")
pdf_files = directory.glob("*.pdf")   

chunk_size = 500
chunk_overlap = 100
chunks = []
index = []
metadatas = []

for file in pdf_files:
    docs = fitz.open(file)
    pdf_metadata = docs.metadata  # extract title, author etc.
    text = ""
    for page in docs:
        text += page.get_text()

    for idx in range(0, len(text), chunk_size - chunk_overlap):
        chunks.append(text[idx : idx + chunk_size])
        index.append(f"{file.name}_{idx}")
        metadatas.append({
            "source": file.name,
            "chunk_start": idx,
            "author": pdf_metadata.get("author", "unknown"),
            "title": pdf_metadata.get("title", "unknown")
        })

chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = chroma_client.create_collection(
    name="my_collection",
    embedding_function=embedding_function
)


collection.upsert(
    ids=index,
    documents=chunks,
    metadatas=metadatas,
)

print(f"Done embedding with {collection.count()} number of collections.")








