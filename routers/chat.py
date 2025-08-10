from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from .model import ask_question as chat_model  # async function

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class ChatRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(question: ChatRequest) -> dict:
    """
    Ask a question to the chat model and get a response.
    """
    try:
        response = await chat_model(question.question)  # ✅ Correct usage
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
