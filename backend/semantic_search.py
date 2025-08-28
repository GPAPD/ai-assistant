from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

INDEX_NAME = "document-reader"


def search_item(query: str):
    # 1. Create embedding and vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    search_products = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    # 2. Perform similarity search
    results = search_products.similarity_search_with_score(query, k=5)
    output = []
    for doc, score in results:
        output.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score
        })
    return {"results": output}


