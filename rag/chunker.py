# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝

from langchain_text_splitters import RecursiveCharacterTextSplitter


def text_splitter(minimal_documents, chunk_size: int = 500, chunk_overlap=30):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    texts_chunk = text_splitter.split_documents(minimal_documents)

    return texts_chunk
