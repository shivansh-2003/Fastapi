## Integrating a Machine Learning Model
Let's assume you have a machine learning model trained and saved as a pickle file. Here's how you can integrate it with FastAPI:

### 1.Load the Model:

```
import pickle
from fastapi import FastAPI

app = FastAPI()

# Load the pre-trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
```
### 2. Create an Endpoint for Predictions:
```
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    # Add more features as needed

@app.post("/predict")
def predict(request: PredictionRequest):
    # Convert the request to a list of features
    features = [[request.feature1, request.feature2, request.feature3]]
    prediction = model.predict(features)
    return {"prediction": prediction[0]}
```
## Testing Your Endpoint
You can test your endpoint using tools like curl or Postman, or directly through the automatically generated Swagger UI provided by FastAPI at http://127.0.0.1:8000/docs.

For example, using curl:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "feature1": 1.0,
  "feature2": 2.0,
  "feature3": 3.0
}'
```
## Adding Async Capabilities
FastAPI allows you to write asynchronous code easily. This is particularly useful for I/O-bound tasks, such as loading large models or performing database operations.

```
from fastapi import FastAPI
import aiofiles

app = FastAPI()

@app.get("/")
async def read_root():
    async with aiofiles.open("somefile.txt", mode="r") as f:
        contents = await f.read()
    return {"file_contents": contents}
```
## Dependency Injection
FastAPI supports dependency injection, which can be useful for managing resources like database connections or shared services.

```
from fastapi import Depends

def get_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

@app.post("/predict")
def predict(request: PredictionRequest, model=Depends(get_model)):
    features = [[request.feature1, request.feature2, request.feature3]]
    prediction = model.predict(features)
    return {"prediction": prediction[0]}
```
## Handling File Uploads
If your model needs to handle file inputs, FastAPI makes it easy to handle file uploads.

```
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```
### Example: Full Application
Here is a complete example putting everything together:
```
import pickle
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class PredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float

def get_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

@app.post("/predict")
def predict(request: PredictionRequest, model=Depends(get_model)):
    features = [[request.feature1, request.feature2, request.feature3]]
    prediction = model.predict(features)
    return {"prediction": prediction[0]}
```
## Running the Application
Save the above code in a file named main.py and run it using:
```
uvicorn main:app --reload
```
