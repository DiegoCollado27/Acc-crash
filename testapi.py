import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://coinranking1.p.rapidapi.com/coins"

querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h","tiers[0]":"1","orderBy":"marketCap","orderDirection":"desc","limit":"50","offset":"0"}

headers = {
	"X-RapidAPI-Key": os.getenv("RAPID_KEY"),
	"X-RapidAPI-Host": os.getenv("RAPID_HOST")
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

print(type(response.json()))
for element in response.json()['data']['coins']:
    if element['name'] == 'Bitcoin':
        print(element['uuid'])
        uuid = element['uuid']
print("/n")

import requests

url = "https://coinranking1.p.rapidapi.com/coin/" + uuid

querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}

headers = {
	"X-RapidAPI-Key": os.getenv("RAPID_KEY"),
	"X-RapidAPI-Host": os.getenv("RAPID_HOST")
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())