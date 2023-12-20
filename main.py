from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf


app = FastAPI()

print("Loading model...")