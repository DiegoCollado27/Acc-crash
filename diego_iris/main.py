#create an api with fast api, use a pydantic model to validate the input data as text named PredictionRequest, add a route named /predict that receives a POST request with the input from Predictionrequest, that function should pass the input to numpy array, then load the prediction model an pass the prediction

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle

app = FastAPI()


"""
pydantic model to accept data types from a json with input and an array

 {
    "input": [5.1, 3.5, 1.4, 0.2]
}


"""
class PredictionRequest(BaseModel):
    input: list


@app.post("/predict")
def predict(request: PredictionRequest):
    text = request.input
    print(text)
    #load .sav model
    model = pickle.load(open("finalized_model.sav", "rb"))
    #make prediction for a losit of lists from the input
    value = np.array(text).reshape(1, -1)
    prediction = model.predict(value)
    print(type(prediction))
    prediction = int(prediction[0])
    print(prediction)
    return {"prediction": prediction}

#run the api with uvicorn

#import uvicorn

#if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8000)

#to run the service, use the command: uvicorn main:app --reload
