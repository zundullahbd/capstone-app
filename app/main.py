import firebase_admin
import pyrebase
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth, credentials
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from model.model import SignUpSchema, LoginSchema
import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from pydantic import BaseModel

# Load your model
f = "app/model/model_capstone.h5"
model = load_model(f)


# Define a Pydantic model for the input data
class InputData(BaseModel):
    text_list: str

app = FastAPI(
    description="This is the main app for the capstone project.",
    title="Capstone App",
    docs_url="/",
)


firebaseConfig = {
    "apiKey": "AIzaSyCYRgpEpLVcVvhGKl0O8gSr9syNIFJipN8",
    "authDomain": "capstone-ch2-ps127.firebaseapp.com",
    "projectId": "capstone-ch2-ps127",
    "storageBucket": "capstone-ch2-ps127.appspot.com",
    "messagingSenderId": "219059724934",
    "appId": "1:219059724934:web:5c3194bce427741d326707",
    "measurementId": "G-VJLZQWLXJL",
    "databaseURL": "",
}

if not firebase_admin._apps:
    cred = credentials.Certificate("app/capstone-key.json")
    firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)


@app.post("/signup")
async def signup(data: SignUpSchema):
    email = data.email
    password = data.password
    try:
        user = auth.create_user(
            email=email, email_verified=False, password=password, disabled=False
        )
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"User {user.uid} account created successfully",
            },
        )
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error creating user: {e}")


@app.post("/login")
async def login(data: LoginSchema):
    email = data.email
    password = data.password
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=password
        )
        token = user["idToken"]
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"User {user['localId']} logged in successfully",
                "token": token,
            },
        )
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Invalid Credentials {e}")


@app.post("/validate")
async def validate_token(request: Request):
    headers = request.headers
    jwt_token = headers.get("Authorization")

    user = auth.verify_id_token(jwt_token)

    return user["user_id"]


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(data: InputData):
    # Extract the text from the input data
    text = data.text_list

    # Tokenize the input string
    tokenizer = Tokenizer(num_words=10000)
    tokenizer.fit_on_texts([text])
    sequences = tokenizer.texts_to_sequences([text])

    # Pad the sequences to the maximum length
    padded_sequences = pad_sequences(sequences, maxlen=1426, padding="post")

    # Now you can pass padded_sequences to your model
    prediction = model.predict(padded_sequences)

    # Return the prediction
    return {"prediction": prediction.tolist()}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
