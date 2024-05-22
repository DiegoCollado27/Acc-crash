#having a dictionary with the test data and the expected results make an endpoint that receives a POST request with the key prediction that is a number and the input for the prediction, mappes it to the name and returns a json with the key result that is a string with the value "correct" if the prediction is correct or "incorrect" if the prediction is incorrect

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# the pydantic should check this format: json=("input_data": input_item, "prediction": prediction)
class PredictionRequest(BaseModel):
    input_data: list
    prediction: int

@app.post("/verify")
def verify(request: PredictionRequest):
    print(request)
    prediction = request.prediction
    print(prediction)
    prediction = map_prediction(prediction)
    print(prediction)
    input_data = request.input_data
    print(input_data)
    print(type(input_data))
    print(tuple(input_data))
    #based on the input data, get the expected result
    expected_result = test_data_dict[tuple(input_data)]
    result = "correct" if expected_result == prediction else "incorrect"
    return {"result": result}

def map_prediction(prediction):
    if prediction == int(0):
        return "setosa"
    elif prediction == int(1):
        return "versicolor"
    elif prediction == int(2):
        return "virginica"

test_data_dict = {
    (4.6, 3.4, 1.4, 0.3): "setosa", (7.2, 3.2, 6.0, 1.8): "virginica",
    (4.8, 3.0, 1.4, 0.1): "setosa", (6.1, 2.9, 4.7, 1.4): "versicolor",
    (4.9, 3.1, 1.5, 0.1): "setosa", (6.4, 2.8, 5.6, 2.2): "virginica",
    (5.0, 3.2, 1.2, 0.2): "setosa", (5.8, 2.7, 4.1, 1.0): "versicolor",
    (5.1, 3.3, 1.7, 0.5): "setosa", (7.1, 3.0, 5.9, 2.1): "virginica",
    (4.8, 3.4, 1.9, 0.2): "setosa", (6.2, 2.9, 4.3, 1.3): "versicolor",
    (4.9, 3.0, 1.4, 0.2): "setosa", (5.6, 2.5, 3.9, 1.1): "versicolor",
    (5.0, 3.5, 1.6, 0.6): "setosa", (6.3, 3.3, 4.7, 1.6): "versicolor",
    (5.1, 3.8, 1.9, 0.4): "setosa", (6.9, 3.1, 5.4, 2.1): "virginica",
    (4.7, 3.2, 1.6, 0.2): "setosa", (6.7, 3.3, 5.7, 2.5): "virginica",
    (5.9, 3.0, 4.2, 1.5): "versicolor", (6.8, 3.0, 5.5, 2.1): "virginica",
    (5.8, 2.7, 3.9, 1.2): "versicolor", (7.3, 2.9, 6.3, 1.8): "virginica",
    (6.0, 3.0, 4.5, 1.5): "versicolor", (6.7, 3.1, 5.6, 2.4): "virginica",
    (5.9, 3.2, 4.8, 1.8): "versicolor", (6.5, 3.0, 5.2, 2.0): "virginica",
    (6.1, 2.8, 4.0, 1.3): "versicolor", (6.3, 2.8, 5.1, 1.5): "virginica",
}

#if __name__ == "__main__":
 #   uvicorn.run(app, host="0.0.0.0", port=8002)

#to run the service, use the command: uvicorn verifier:app --reload