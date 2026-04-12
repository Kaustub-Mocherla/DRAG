import chromadb
from ollama import chat

def searching(res):
    chroma_client = chromadb.PersistentClient(path="/home/ghostface/Desktop/DRAG/chroma_db")
    collection = chroma_client.get_collection("my_collection")

    results = collection.query(
        query_texts=[res], 
        n_results=10
    )
    context = "\n\n".join(results['documents'][0])

    prompt = f"""Answer the question using ONLY the context below. If the answer is not in the context, say "I don't have enough information."

    Context:
    {context}

    Question:
    {res}

    Answer:"""
    print("Retrieved context:")
    print(context)
    print("---")
    stream = chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content':prompt}],
        
        stream=True,
    )
    print("responding...")
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    return stream