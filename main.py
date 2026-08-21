import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app:app", host="0.0.0.1", port=8003, reload=True)
