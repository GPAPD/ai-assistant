from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from openai import embeddings, vector_stores

load_dotenv()

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import  PineconeVectorStore


from langchain_openai import ChatOpenAI, OpenAIEmbeddings

INDEX_NAME = "document-reader"

def format_docs(docs):
    print(docs)
    return "\n\n".join(doc.page_content for doc in docs)


def run_llm(query: str, chat_history: List[Dict[str,Any]]=[]):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    #llm = ChatOpenAI(verbose=True, temperature=0)
    llm = ChatOllama(model="llama3")

    #retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    # stuff_documents_chain = create_stuff_documents_chain(llm, retrival_qa_chat_prompt)
    #
    # qa = create_retrieval_chain(
    #     retriever=docsearch.as_retriever(),combine_docs_chain=stuff_documents_chain
    # )
    #
    # result= qa.invoke(input={"input":query})

    #custom user prompt
    template = """ Use the following pieces of context to answer the question at the end.
     if you don't know the answer, just say that you dont know or we do sell that item, don't try to make up an answer.
     use three sentences maximum and keep the answer as concise as possible.
     always say "thanks for asking" at the end o the answer

      Chat history:
      {chat_history}
    
      Context:
      {context}
    
      Question: {question}

      Helpful Answer: 
      """

    def format_chat_history(chat_history: List[Dict[str, Any]]) -> str:
        if not chat_history:
            return ""

        history = ""
        for turn in chat_history:
            if isinstance(turn, dict):  # ✅ Make sure it's a dict
                user = turn.get("user", "")
                assistant = turn.get("assistant", "")
                history += f"User: {user}\nAssistant: {assistant}\n"
            else:
                history += f"{turn}\n"  # fallback if it's malformed
        return history.strip()

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

    # custom_rag_prompt = PromptTemplate.from_template(template)
    # rag_chain = (
    #     {"context": docsearch.as_retriever() | format_docs, "question": RunnablePassthrough()}
    #     | custom_rag_prompt
    #     | llm
    # )

    result = rag_chain.invoke(query)

    new_result = {
    "query": query,
    "result": result.content,
    }

    return new_result
