# ╔════════════════════════════════════════════════════════════╗
# ║ 👷 PIPELINE
# ╚════════════════════════════════════════════════════════════╝
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from rag.prompts import chatModel, prompt
from rag.vectorstore import retriever


def build_rag_pipeline():
    question_answer = create_stuff_documents_chain(chatModel, prompt)
    rag = create_retrieval_chain(retriever, question_answer)

    return rag
