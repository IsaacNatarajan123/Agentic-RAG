# 🔍 WikiRAG Assistant

A **Retrieval-Augmented Generation (RAG)** chatbot that answers questions using a custom **Wikipedia knowledge base**.  
Built with **LangChain, ChromaDB, Ollama, and Streamlit**.

---

## 🚀 Features

- 📚 Scrapes Wikipedia data (Python, LangChain, etc.)
- ✂️ Splits content into optimized chunks
- 🧠 Generates embeddings using Ollama
- ⚡ Fast semantic retrieval using ChromaDB
- 💬 Interactive chatbot using Streamlit
- 🔀 Smart query routing:
  - General chat → LLM
  - Math questions → LLM
  - Knowledge queries → Vector DB (RAG)
