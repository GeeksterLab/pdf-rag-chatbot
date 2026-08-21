# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
from pydantic import BaseModel
from typing import List


class QuestionInput(BaseModel):
    """
    Answer request structure.
    """

    text: str


class ResponseChatBot(BaseModel):
    """
    Chatbot answer structure.
    """

    answer: str
    source: List[str]
    pages: List[int]
