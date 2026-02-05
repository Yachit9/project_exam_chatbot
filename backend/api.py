from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_chain import answer_gate_question

app=FastAPI(
    title="gate exam bot api",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QuestionRequest(BaseModel):
    question:str
class Answerresponse(BaseModel):
    answer:str

@app.post("/ask",response_model=Answerresponse)
def ask_question(req: QuestionRequest):
    answer=answer_gate_question(req.question)
    return {"answer":answer}

@app.get("/health")
def health():
    return {"status":"ok"}