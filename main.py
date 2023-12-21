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


app = FastAPI(
    description="This is the main app for the capstone project.",
    title="Capstone App",
    docs_url="/",
)


@app.post("/signup")
async def create_account():
    pass


@app.post("/login")
async def access_token():
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
