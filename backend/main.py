from fastapi import FastAPI
from pydantic import BaseModel
from backend.core import run_llm

# Create FastAPI app
app = FastAPI()

class Query(BaseModel):
    message: str


# send query to the LLM
@app.post("/chat")
def chat(query: Query):
    user_message = query.message
    res = run_llm(query=user_message)

    return res

    # return {
    #     # "query": res["query"],
    #     # "response": res["result"],
    #     # "source_document": res["source_document"]
    #
    # }