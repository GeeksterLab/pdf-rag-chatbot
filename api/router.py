"""
POST/ answer →

"""

# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
from core.config import settings

# ╔════════════════════════════════════════════════════════════╗
# ║ 🌐 API
# ╚════════════════════════════════════════════════════════════╝
from fastapi import APIRouter

medicalquestion = APIRouter()

# ╔════════════════════════════════════════════════════════════╗
# ║ 🛣️ ROUTES
# ╚════════════════════════════════════════════════════════════╝
from api.schemas import QuestionInput, ResponseChatBot

from pathlib import Path
from functools import lru_cache


# Build the pipeline once then reuse it
@lru_cache(maxsize=1)
def get_rag_pipeline():
    from rag.pipeline import build_rag_pipeline

    return build_rag_pipeline()


@medicalquestion.post(
    "/medicalquestion",
    response_model=ResponseChatBot,
    tags=["Medical-Question"],
)
def question(input: QuestionInput) -> ResponseChatBot:

    rag = get_rag_pipeline()
    response = rag.invoke({"input": input.text})

    return ResponseChatBot(
        answer=response["answer"],
        source=[
            Path(doc.metadata.get("source", "")).stem for doc in response["context"]
        ],  # Path().stem extract the filename without its directory and extension
        pages=[doc.metadata.get("page", 0) for doc in response["context"]],
    )
