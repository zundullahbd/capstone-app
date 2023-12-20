from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import uvicorn


app = FastAPI(
    description="This is the main app for the capstone project.",
    title="Capstone App",
    docs_url="/"
)

@app.post('/signup')
async def create_account():
    pass

@app.post('/login')
async def access_token():
    pass

@app.post('/validate')
async def validate_token():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
