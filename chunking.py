from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import re

# ------------------------
# LOAD DATA
# ------------------------
with open('wikipedia_big_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# ------------------------
# TEXT CLEANING FUNCTION
# ------------------------
def clean_text(text):
    text = re.sub(r"\[\d+\]", "", text)   # remove [1], [2]
    text = re.sub(r"\s+", " ", text)      # remove extra spaces
    return text.strip()

# ------------------------
# SAFE ID FUNCTION
# ------------------------
def safe_id(text):
    return re.sub(r'[^a-zA-Z0-9_]', '_', text)

# ------------------------
# SPLITTER
# ------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)

final_chunks = []

# ------------------------
# PROCESS
# ------------------------
for article in data:
    title = article.get('title', 'unknown')
    source = article.get('url', '')
    content = article.get('content', '')

    if not content:
        continue  # skip empty articles

    content = clean_text(content)

    chunks = splitter.split_text(content)

    for i, chunk_text in enumerate(chunks):
        final_chunks.append({
            "chunk_id": f"{safe_id(title)}_{i}",
            "metadata": {
                "title": title,
                "url": source
            },
            "content": chunk_text
        })

# ------------------------
# SAVE
# ------------------------
with open('chunked_data.json', 'w', encoding='utf-8') as f:
    json.dump(final_chunks, f, indent=4, ensure_ascii=False)

print(f"🔥 Done! Created {len(final_chunks)} clean chunks.")