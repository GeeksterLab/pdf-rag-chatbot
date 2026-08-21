# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
from core.config import settings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from rag.embeddings import download_embeddings
from rag.chunker import text_splitter

# ── API Keys ──────────────────────────────────────────────────
PINECONE_API_KEY = settings.PINECONE_API_KEY
OPENAI_API_KEY = settings.OPENAI_API_KEY


# ── Check our pinecone account ──────────────────────────────────────────────────
pinecone_api_key = PINECONE_API_KEY
pinecone_account = Pinecone(api_key=PINECONE_API_KEY)

# ── Create our index here instead of in the Picone console ──────────────────────────────────────────────────
index_name = "basicalmedicalagent"

if not pinecone_account.has_index(index_name):
    pinecone_account.create_index(
        name=index_name,
        dimension=384,  # Corresponding to dimension of the embeddings → len(Test_1)
        metric="cosine",  # Cosine similarity
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
index = pinecone_account.Index(index_name)

# ── Store our chunks in our Pinecone index ──────────────────────────────────────────────────
embedding = download_embeddings()

docsearch = PineconeVectorStore(
    index=index,
    embedding=embedding,
)

# ── Config our retriever ──────────────────────────────────────────────────
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
