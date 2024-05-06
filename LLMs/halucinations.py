from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar el motor de OpenAI 
engine = "gpt-4"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt):
  completion = client.chat.completions.create(
  model=engine,
  messages=[
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return completion


prompt = f"""
Háblame de la función Eje pirandáculo central ponderada para la detección de amenazas en IBM QRadar"
"""

response = get_completion(prompt)
print(response.choices[0].message.content)