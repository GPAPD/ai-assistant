# app.py
import streamlit as st
import os
from typing import List, Dict, Any

# LangChain imports
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# ==============================
# 🔑 Load API Keys from Secrets
# ==============================
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
##PINECONE_ENVIRONMENT = st.secrets["PINECONE_ENVIRONMENT"]

# Set env variables so LangChain + Pinecone can see them
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
#os.environ["PINECONE_ENVIRONMENT"] = PINECONE_ENVIRONMENT

INDEX_NAME = "document-reader"

# ---------- Helper Functions ----------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def format_chat_history(chat_history: List[Dict[str, Any]]) -> str:
    if not chat_history:
        return ""
    history = ""
    for turn in chat_history:
        if isinstance(turn, dict):
            user = turn.get("user", "")
            assistant = turn.get("assistant", "")
            history += f"User: {user}\nAssistant: {assistant}\n"
        else:
            history += f"{turn}\n"
    return history.strip()

# ---------- Core LLM Function ----------
def run_llm(query: str, chat_history: List[Dict[str, Any]]=[]):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    llm = ChatOpenAI(verbose=True, temperature=0)

    template = """
    You are a Smart E-Commerce Assistant. Use the following context to answer the customer's question.

    Rules:
    - If you don't know the answer or we don't sell that item, reply: "I'm sorry, I couldn't find that information or say we don't sell that item in our site."
    - Keep answers concise (maximum three sentences).
    - Always include item_id, Name for products when available.
    - Always end the answer with: "Thanks for asking."

    Chat history:
    {chat_history}

    Context:
    {context}

    Question: {question}

    Helpful Answer:
    """

    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": docsearch.as_retriever() | format_docs,
            "question": RunnablePassthrough(),
            "chat_history": lambda x: format_chat_history(chat_history),
        }
        | custom_rag_prompt
        | llm
    )

    result = rag_chain.invoke(query)

    return {
        "query": query,
        "result": result.content,
    }

# ---------- Streamlit UI ----------
st.title("AI Assistant")
st.caption("Ask anything and get smart, context-aware answers.")

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # list of {"user": ..., "assistant": ...}

# Chat Input
user_input = st.chat_input("Type your message here...")

if user_input:
    with st.spinner("Generating response..."):
        response = run_llm(query=user_input, chat_history=st.session_state["chat_history"])
        answer = response.get("result", "I'm sorry, I couldn't find that information.")

    # Append to chat history
    st.session_state["chat_history"].append({"user": user_input, "assistant": answer})

# Chat Display
for chat in st.session_state["chat_history"]:
    st.chat_message("user").write(chat["user"])
    st.chat_message("assistant").write(chat["assistant"])



