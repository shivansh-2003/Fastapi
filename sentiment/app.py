from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
nlp_pipeline = pipeline("sentiment-analysis")

class TextInput(BaseModel):
    text: str

@app.post("/predict_sentiment")
def predict_sentiment(input: TextInput):
    text = input.text
    result = nlp_pipeline(text)[0]
    return {"text": text, "sentiment": result["label"], "confidence": result["score"]}
