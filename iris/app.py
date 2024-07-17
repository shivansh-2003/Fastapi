from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from typing import List

# Load the saved model
model = joblib.load('iris_model.pkl')

# Define FastAPI app
app = FastAPI()

# Define request body schema
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Define endpoint for prediction
@app.post("/predict")
def predict(data: List[IrisData]):
    predictions = []
    for entry in data:
        input_data = [[entry.sepal_length, entry.sepal_width, entry.petal_length, entry.petal_width]]
        prediction = model.predict(input_data).tolist()
        predictions.append(prediction)
    return {"predictions": predictions}
