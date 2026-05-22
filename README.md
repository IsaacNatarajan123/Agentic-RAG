# 🔍 WikiRAG Assistant

A **Retrieval-Augmented Generation (RAG)** chatbot that answers questions using a custom **Wikipedia knowledge base**.  
Built with **LangChain, ChromaDB, Ollama, and Streamlit**.

---

## 🚀 Features

- Scrapes Wikipedia data (Python, LangChain, etc.)
- Splits content into optimized chunks
- Generates embeddings using Ollama
- Fast semantic retrieval using ChromaDB
- Interactive chatbot using Streamlit
- Smart query routing:
  - General chat → LLM
  - Math questions → LLM
  - Knowledge queries → Vector DB (RAG)

## ⚙️ Tech Stack

- LangChain  
- ChromaDB  
- Ollama  
- Streamlit  
- Wikipedia API  

---

## 📥 Installation

### 1. Clone the Repository

git clone https://github.com/<your-username>/Agentic-RAG.git
cd Agentic-RAG

**2. Install Dependencies**

pip install langchain langchain-core langchain-community langchain-chroma langchain-ollama streamlit chromadb wikipedia

**3. Install Ollama**

Download from: https://ollama.com

**4. Pull Required Models**

ollama pull llama3.2:3b
ollama pull mxbai-embed-large

📚 Pipeline
🥇 Step 1: Scrape Data
python scraping.py
Fetches Wikipedia articles
Stores raw content

🥈 Step 2: Chunk Data
python chunking.py
Splits text into chunks (better retrieval)

🥉 Step 3: Create Embeddings
python embedding.py
Converts chunks → vectors
Stores in my_vector_db/

▶️ Step 4: Run Chatbot
streamlit run chatbot.py

Open:

http://localhost:8501
