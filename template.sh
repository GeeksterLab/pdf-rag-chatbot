mkdir -p api
touch api/__init__.py
touch api/app.py
touch api/schemas.py
touch api/pipeline.py

mkdir -p core
touch core/config.py

mkdir -p rag
touch rag/loader.py
touch rag/chunker.py
touch rag/embeddings.py
touch rag/vectorestore.py

mkdir -p data

mkdir -p notebooks
touch notebooks/notebook.ipynb


mkdir -p .streamlit
touch .streamlit/secrets.toml
touch .streamlit/secrets.toml.example

mkdir -p streamlit
touch streamlit/streamlit_app.py
touch streamlit/requirements.txt

touch main.py
touch Dockerfile
touch README.md
touch requirements.txt
touch .gitignore
touch .dockerignore
touch .env


echo "Directory and files created successfully"
