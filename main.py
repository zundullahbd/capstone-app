<<<<<<< HEAD
import uvicorn
import pyrebase
import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from model.model import SignUpSchema, LoginSchema
=======
import pickle

import uvicorn
from fastapi import FastAPI
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from pydantic import BaseModel

# Load your model
with open("model/model_capstone.pkl", "rb") as f:
    model = pickle.load(f)


# Define a Pydantic model for the input data
class InputData(BaseModel):
    text_list: str

>>>>>>> 153b03a8a11ff1cfeca515534312ab2eedf39304

app = FastAPI(
    description="This is the main app for the capstone project.",
    title="Capstone App",
    docs_url="/",
)

<<<<<<< HEAD
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
=======

@app.post("/signup")
async def create_account():
    pass


@app.post("/login")
async def access_token():
>>>>>>> 153b03a8a11ff1cfeca515534312ab2eedf39304
    pass


@app.post("/validate")
async def validate_token():
    pass


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
