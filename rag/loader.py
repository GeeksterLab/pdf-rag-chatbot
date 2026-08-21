# ╔════════════════════════════════════════════════════════════╗
# ║ ➕ EXTRACTION
# ╚════════════════════════════════════════════════════════════╝
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_core.documents import Document

from core.config import settings


def load_pdf(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )

    documents = loader.load()

    return documents


# extracted_data = load_pdf("data")


# ╔════════════════════════════════════════════════════════════╗
# ║ ➕ FILTER
# ╚════════════════════════════════════════════════════════════╝
from typing import List


def filter_documents(documents: List[Document]) -> List[Document]:
    minimal_documents: List[Document] = []
    for doc in documents:
        src = doc.metadata.get("source")
        pages = doc.metadata.get("page")
        minimal_documents.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    "source": src,
                    "page": pages,
                },
            )
        )

    return minimal_documents


# minimal_documents = filter_documents(extracted_data)
