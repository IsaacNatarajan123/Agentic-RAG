from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langgraph.prebuilt import create_react_agent
import streamlit as st

# -------------------------
# STREAMLIT UI
# -------------------------
st.set_page_config(page_title="WikiRAG Assistant", page_icon="🔍")
st.title("🔍 WikiRAG Assistant")

# -------------------------
# LOAD AGENT (CACHED)
# -------------------------
@st.cache_resource(show_spinner=False)
def load_agent():
    # Embeddings
    embeddings_model = OllamaEmbeddings(model="mxbai-embed-large")

    # Vector DB
    db = Chroma(
        persist_directory="./my_vector_db",
        collection_name="wiki_collection",
        embedding_function=embeddings_model
    )

    retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10})

    # -------------------------
    # CUSTOM TOOL (NO create_retriever_tool)
    # -------------------------
    def search_wikipedia(query: str):
        query = query.lower()
        docs = retriever.invoke(query)
        print("DEBUG: Retrieved docs =", len(docs))

        if not docs:
            return "NO_RESULTS"

        results = []
        for d in docs:
            content = d.page_content
            url = d.metadata.get("url", "No URL available")
            results.append(f"{content}\nSOURCE: {url}")

        return "\n\n".join(results)

    tool = Tool(
        name="wikipedia_search",
        func=search_wikipedia,
        description="Search Wikipedia knowledge base and return content with source URLs."
    )

    # LLM
    llm = ChatOllama(model="llama3.1:8b", temperature=0)

    # System Prompt
    system_prompt = SystemMessage(content="""
You are a strict retrieval-based assistant.

RULES:
1. You MUST use the tool 'wikipedia_search' before answering.
2. ONLY answer using retrieved content.
3. If tool returns NO_RESULTS, say:
   "I could not find information on this topic in my knowledge base."
4. Keep answer under 3 sentences.
5. ALWAYS include source URL.
6. NEVER make up information.
""")

    # Agent
    agent = create_react_agent(llm, [tool], prompt=system_prompt)
    return agent

# -------------------------
# LOAD AGENT INSTANCE
# -------------------------
with st.spinner("Loading model..."):
    try:
        agent_executor = load_agent()
    except Exception as e:
        st.error(f"Error loading agent: {e}")
        st.stop()

# -------------------------
# SESSION STATE (CHAT MEMORY)
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# -------------------------
# USER INPUT
# -------------------------
user_question = st.chat_input("Ask about Python or LangChain...")

if user_question:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    # Save user message
    st.session_state.messages.append(HumanMessage(content=user_question))

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                result = agent_executor.invoke({
                    "messages": st.session_state.messages
                })
                ai_message = result["messages"][-1].content
            except Exception as e:
                ai_message = f"Error: {str(e)}"

        st.markdown(ai_message)

    # Save AI message
    st.session_state.messages.append(AIMessage(content=ai_message))