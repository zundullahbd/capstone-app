import uvicorn
import pyrebase
import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from model.model import SignUpSchema, LoginSchema

app = FastAPI(
    description="This is the main app for the capstone project.",
    title="Capstone App",
    docs_url="/"
)

if not firebase_admin._apps:
    cred = credentials.Certificate("capstone-key.json")
    firebase_admin.initialize_app(cred)
    
firebaseConfig = {
  "apiKey": "AIzaSyCYRgpEpLVcVvhGKl0O8gSr9syNIFJipN8",
  "authDomain": "capstone-ch2-ps127.firebaseapp.com",
  "projectId": "capstone-ch2-ps127",
  "storageBucket": "capstone-ch2-ps127.appspot.com",
  "messagingSenderId": "219059724934",
  "appId": "1:219059724934:web:5c3194bce427741d326707",
  "measurementId": "G-VJLZQWLXJL",
  "databaseURL":"",
}

firebase = pyrebase.initialize_app(firebaseConfig)

@app.post('/signup')
async def create_account(user_data: SignUpSchema):
    pass

@app.post('/login')
async def access_token(user_data: LoginSchema):
    pass

@app.post('/validate')
async def validate_token():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
