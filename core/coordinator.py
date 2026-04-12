import requests
from ollama import chat
query = input("query :")
nodes = [
    "http://localhost:8001/query",
    "http://localhost:8002/query"
]

all_chunks = []
for node in nodes:
    response = requests.post(node, json={"query": query})
    all_chunks.extend(response.json()['chunks'])

context = "\n\n".join(all_chunks)

prompt = f"""Answer the question using ONLY the context below. If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question:
{query}

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
