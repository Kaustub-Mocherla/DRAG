import fitz
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
docs = fitz.open("/home/ghostface/Desktop/23STUCHH011056/Special_porject/Papers/1.pdf")
full_text = ""

for page in docs:
    full_text+=page.get_text()

chunk_size = 1000
chunk_overlap = 200
chunks = []
index = []
for idx in range(0,len(full_text),chunk_size - chunk_overlap):
    chunks.append(full_text[idx : idx+chunk_size])
    index.append(f"id{idx}")

chroma_client = chromadb.Client()
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = chroma_client.create_collection(
    name="my_collection",
    embedding_function=embedding_function
)


collection.upsert(
    ids=index,
    documents=chunks
)

print(collection.count())








