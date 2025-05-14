from fastapi import FastAPI
from pydantic import BaseModel
from backend.core import run_llm
from backend.ingestion import ingest_docs

# Create FastAPI app
app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/update-faiss")
def update_faiss():
    ingest_docs()
    return True

# send query to the LLM
@app.post("/chat")
def chat(query: Query):
    user_message = query.message
    res = run_llm(query=user_message)

    return {
        "query": res["query"],
        "response": res["result"].content
    }