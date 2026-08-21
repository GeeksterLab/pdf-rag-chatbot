# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.config import settings

# ╔════════════════════════════════════════════════════════════╗
# ║ ⚙️ CONFIG
# ╚════════════════════════════════════════════════════════════╝
chatModel = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.OPENAI_API_KEY,
)

# ── System prompt ──────────────────────────────────────────────────
SYSTEM_PROMPT = """

    You are a medical assistant specialized in question-answering from clinical documents.
    Use ONLY the context provided below to answer the user's question.
    If you do not find the answer in the context, respond "I do not have enough information in the provided documents to answer this question."
    Do NOT complete with general knowledge or assumptions outside the provided context.

    Rules:
    - Maximum 3 sentences.
    - Be clear, precise, and avoid medical jargon when it is possible.
    - Always cite your source: indicate the document name or section and if possible the pages.
    - Always add the Medical disclaimer after each response.

    Context:
    {context}

    ⚠️ Medical disclaimer: This response is generated from provided documents and is for informational purposes only.
    It does not constitute medical advice. Always consult a qualified healthcare professional for diagnosis or treatment.

"""

# ── prompt ──────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)
