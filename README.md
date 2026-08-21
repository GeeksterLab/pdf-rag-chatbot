# Medical RAG Chatbot

![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
[![Click Here](https://img.shields.io/badge/Click%20Here-blue?style=for-the-badge)](https://medicalragpdfchatbot.streamlit.app/)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571.svg?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge\&logo=jupyter\&logoColor=white)

Medical chatbot based on a **Retrieval-Augmented Generation (RAG)** pipeline.

The assistant answers medical questions using only information retrieved from indexed PDF documents.
If the required information is not available in the retrieved context, the assistant is instructed not to invent an answer.

---

## Objective

The project demonstrates a simple document-grounded RAG architecture:

- load medical PDF documents;
- split them into smaller chunks;
- generate embeddings;
- store and retrieve vectors with Pinecone;
- send the retrieved context to an LLM;
- return an answer with document sources and PDF pages;
- expose the pipeline through FastAPI and Streamlit.

---

## RAG Pipeline

```text
Medical PDF
    ↓
Document Loader
    ↓
Chunking
    ↓
Embeddings
    ↓
Pinecone
    ↓
Similarity Retrieval
    ↓
LLM
    ↓
Answer + Sources
```

Current configuration:

```text
Embedding model : sentence-transformers/all-MiniLM-L6-v2
Embedding size  : 384
Chunk size      : 500
Chunk overlap   : 30
Retrieval       : similarity
Top-k           : 3
Vector store    : Pinecone
LLM             : gpt-4o-mini
```

---

## API

The FastAPI backend exposes the RAG pipeline.

### Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/health` | Checks the API status |
| `POST` | `/medicalquestion` | Sends a medical question to the RAG pipeline |

Example request:

```json
{
  "text": "What is acne?"
}
```

Example response:

```json
{
  "answer": "Acne is a common skin disease...",
  "source": [
    "Medical_book",
    "Medical_book",
    "Medical_book"
  ],
  "pages": [
    39,
    37,
    38
  ]
}
```

---

## Streamlit Interface

The Streamlit application provides two sections:

### Chatbot

Users can ask medical questions and receive:

- a document-grounded answer;
- retrieved document sources;
- associated PDF pages.

### Knowledge Base

The interface also displays information about the local document collection:

- number of PDF files;
- document names;
- number of pages;
- vector database;
- embedding model;
- chunk configuration;
- retrieval configuration.

Live demo:

**https://medicalragpdfchatbot.streamlit.app/**

---

## Project Structure

```text
.
├── api/
│   ├── app.py
│   ├── router.py
│   └── schemas.py
│
├── core/
│   └── config.py
│
├── data/
│   └── Medical_book.pdf
│
├── rag/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── loader.py
│   ├── pipeline.py
│   ├── prompts.py
│   └── vectorstore.py
│
├── streamlit/
│   └── streamlit_app.py
│
├── notebook.ipynb
├── pyproject.toml
└── README.md
```

---

## Run Locally

### FastAPI

```bash
uv run uvicorn api.app:app --port 8003 --reload
```

Swagger documentation:

```text
http://127.0.0.1:8003/docs
```

### Streamlit

```bash
uv run streamlit run streamlit/streamlit_app.py
```

---

## Environment Variables

Create a `.env` file containing:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

---

## Stack

```text
Python
LangChain
HuggingFace Embeddings
Sentence Transformers
Pinecone
OpenAI
FastAPI
Pydantic
Streamlit
PyPDF
```

---

## Limitations

- The assistant is limited to information available in the indexed documents.
- Retrieved PDF page numbers may differ from the printed page numbers inside a book.
- The application is for demonstration and informational purposes only.
- It does not provide medical diagnosis or replace a healthcare professional.

---

## Next Step

This project serves as the RAG foundation for a future **Agentic Medical Assistant** integrating routing, safety guardrails and tool calling.
