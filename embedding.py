import json
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings_model = OllamaEmbeddings(model="mxbai-embed-large")

PERSIST_DIR = "./my_vector_db"
COLLECTION_NAME = "wiki_collection"
BATCH_SIZE = 100

with open('chunked_data.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

print(f"Starting to embed {len(chunks)} chunks...")

texts = [chunk['content'] for chunk in chunks]
metadatas = [chunk['metadata'] for chunk in chunks]
ids = [chunk['chunk_id'] for chunk in chunks]

db = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings_model,
    persist_directory=PERSIST_DIR
)

for i in range(0, len(texts), BATCH_SIZE):
    print(f"Processing batch {i} → {i+BATCH_SIZE}")

    db.add_texts(
        texts=texts[i:i+BATCH_SIZE],
        metadatas=metadatas[i:i+BATCH_SIZE],
        ids=ids[i:i+BATCH_SIZE]
    )

print(f"\n Done! Stored {len(chunks)} chunks in '{PERSIST_DIR}'")
