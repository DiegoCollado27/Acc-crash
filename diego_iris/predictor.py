from fastapi import FastAPI
import requests
import numpy as np
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class PredictionRequest(BaseModel):
    input_data: list

@app.post("/predict")
def predict(request: PredictionRequest):
    print(request)
    input_data = request.input_data
    print(input_data)
    #make a list of predictions

    predictions = []
    for input_item in input_data:
        print(input_item)
        # Send input to service on port 8001
        response1 = requests.post("http://model_service:8000/predict", json={"input": input_item})
        prediction = response1.json()["prediction"]
        #PRINT WHAT IS THE PREDICITON AND THE TYPE
        print(f"prediction: {prediction}")
        print(type(prediction))
        # Send prediction to service on port 8002 that takes input and prediction and returns a result
        response2 = requests.post("http://verifier_service:8002/verify", json={"input_data": input_item, "prediction": prediction})
        result = response2.json()["result"]
        predictions.append({"input": input_item, "prediction": prediction, "result": result})

    return {"predictions": predictions}

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8001)

    