from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model('heart_disease_model.h5')

# Initialize FastAPI app
app = FastAPI()

# Define input data model
class HeartDiseaseInput(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float

# Define the prediction endpoint
@app.post("/predict")
def predict(data: HeartDiseaseInput):
    input_data = np.array([[data.age, data.sex, data.cp, data.trestbps, data.chol, data.fbs, data.restecg,
                            data.thalach, data.exang, data.oldpeak, data.slope, data.ca, data.thal]])
    
    # Make prediction
    prediction = model.predict(input_data)
    predicted_class = int(prediction[0][0] > 0.5)
    return {"prediction": predicted_class}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
