from typing import Optional

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
from pydantic import BaseModel

from app.model.model import LoginSchema, SignUpSchema, jobData

f = "app/model/model_capstone.h5"
model = load_model(f)


class InputData(BaseModel):
    text_list: str


app = FastAPI(
    description="This is the main app for the capstone project.",
    title="Capstone App",
    docs_url="/",
)


# Firebase configuration
firebaseConfig = {
    "apiKey": "",
    "authDomain": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": "",
    "databaseURL": "",
}

# Initialize Firebase
if not firebase_admin._apps:
    # Load the Firebase credentials from a JSON file
    cred = credentials.Certificate("app/capstone-key.json")
    # Initialize the Firebase application with the loaded credentials
    firebase_admin.initialize_app(cred)

# Initialize Pyrebase with the Firebase configuration
firebase = pyrebase.initialize_app(firebaseConfig)


@app.post("/signup")
async def signup(data: SignUpSchema):
    """
    Sign up a new user.

    This endpoint accepts an email and password and creates a new user in Firebase.

    Args:
        data (SignUpSchema): The email and password of the new user.

    Returns:
        JSONResponse: A response with a status code and a message indicating whether the user was created successfully.
    """
    email = data.email
    password = data.password
    try:
        # Create a new user in Firebase
        user = auth.create_user(
            email=email, email_verified=False, password=password, disabled=False
        )
        # Return a success response
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"User {user.uid} account created successfully",
            },
        )
    except Exception as e:
        # Return an error response if there was an exception
        return HTTPException(status_code=400, detail=f"Error creating user: {e}")


@app.post("/login")
async def login(data: LoginSchema):
    """
    Log in a user.

    This endpoint accepts an email and password and logs in the user in Firebase.

    Args:
        data (LoginSchema): The email and password of the user.

    Returns:
        JSONResponse: A response with a status code, a success indicator, a message indicating whether the user was logged in successfully, and the user's token.
    """
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
    """
    Validate a user's token.

    This endpoint accepts a request with an Authorization header and validates the user's token.

    Args:
        request (Request): The request with the Authorization header.

    Returns:
        None. This function will raise an HTTPException if the token is invalid.
    """
    headers = request.headers
    jwt_token = headers.get("Authorization")

    user = auth.verify_id_token(jwt_token)

    return user["user_id"]


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(data: InputData):
    """
    Make a prediction based on the input data.

    This endpoint accepts either a single text list or several fields that are concatenated into a single text list. The text list is then tokenized, padded, and used to make a prediction.

    Args:
        data (InputData): The input data.

    Returns:
        dict: A dictionary with a "prediction" key and the prediction as the value.
    """
    if data.text_list is not None:
        text = data.text_list
    else:
        text = " ".join(
            [str(value) for key, value in data.dict().items() if value is not None]
        )

    tokenizer = Tokenizer(num_words=10000)
    tokenizer.fit_on_texts([text])
    sequences = tokenizer.texts_to_sequences([text])

    padded_sequences = pad_sequences(sequences, maxlen=1426, padding="post")

    prediction = model.predict(padded_sequences)

    return {"prediction": prediction.tolist()}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
