import requests
from ollama import chat
query = input("query :")
response = requests.post("http://localhost:8000/query",json={"query":query})

context = "\n\n".join(response.json()['chunks'])

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
