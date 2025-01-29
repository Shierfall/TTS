# server.py
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

# Remove the if __name__ == "__main__": block when using Procfile
