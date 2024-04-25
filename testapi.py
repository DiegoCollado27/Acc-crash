import requests
from dotenv import load_dotenv
import os
from fastapi import FastAPI

load_dotenv()

url = "https://coinranking1.p.rapidapi.com/coins"

querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h","tiers[0]":"1","orderBy":"marketCap","orderDirection":"desc","limit":"50","offset":"0"}

headers = {
	"X-RapidAPI-Key": os.getenv("RAPID_KEY"),
	"X-RapidAPI-Host": os.getenv("RAPID_HOST")
}

response = requests.get(url, headers=headers, params=querystring)

#print(response.json())

#print(type(response.json()))
for element in response.json()['data']['coins']:
    if element['name'] == 'Bitcoin':
        
        uuid = element['uuid']
        price =  element['price']
        break

app = FastAPI()


@app.get("/")
async def price():
    return { "message" : f"el precio es {uuid} dolares"}

"""
url = "https://coinranking1.p.rapidapi.com/coin/" + uuid

querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}

headers = {
	"X-RapidAPI-Key": os.getenv("RAPID_KEY"),
	"X-RapidAPI-Host": os.getenv("RAPID_HOST")
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
"""