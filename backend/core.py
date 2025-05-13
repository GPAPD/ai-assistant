from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from openai import embeddings

load_dotenv()

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import  PineconeVectorStore


from langchain_openai import ChatOpenAI, OpenAIEmbeddings

INDEX_NAME = "document-reader"

def run_llm(query: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    # retrival_qa_chat_prompt.messages[0].prompt.template = (
    #     "You are a helpful and professional customer service representative. "
    #     "Answer questions politely and clearly using the retrieved documents below.\n\n"
    #     "Always display the item_id"
    #     "If the answer isn't found in the documents, say 'I'm sorry, I couldn't find that information.'"
    # )

    stuff_documents_chain = create_stuff_documents_chain(chat, retrival_qa_chat_prompt)

    qa = create_retrieval_chain(
        retriever=docsearch.as_retriever(),combine_docs_chain=stuff_documents_chain
    )

    result= qa.invoke(input={"input":query})

    new_result = {
    "query": result["input"],
    "result": result["answer"],
    "source_document":result["context"]
    }

    return new_result


# if __name__ == "__main__":
#     res = run_llm(query="What is the cheapest item you have?")
#     print(res["result"])