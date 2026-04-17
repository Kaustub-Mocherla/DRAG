
import fitz
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pathlib import Path
import argparse
def ingest(pdf_dir, db_path, collection_name):
    directory = Path(pdf_dir)
    pdf_files = directory.glob("*.pdf")   

    chunk_size = 500
    chunk_overlap = 100
    chunks = []
    index = []
    metadatas = []

    for file in pdf_files:
        docs = fitz.open(file)
        pdf_metadata = docs.metadata 
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

    chroma_client = chromadb.PersistentClient(path=db_path)
    embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection_name = args.collection
    try:
        chroma_client.delete_collection(name=collection_name)
    except:
        pass
    
    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )


    collection.upsert(
        ids=index,
        documents=chunks,
        metadatas=metadatas,
    )

    print(collection.count())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", required=True, help="Path to PDF folder")
    parser.add_argument("--db-path", required=True, help="Path to ChromaDB storage")
    parser.add_argument("--collection", default="my_collection")
    args = parser.parse_args()
    
    ingest(args.pdf_dir, args.db_path, args.collection)