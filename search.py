import chromadb
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("my_collection")
results = collection.query(
    query_texts=["distributed rag"], 
    n_results=10
)
print(results)