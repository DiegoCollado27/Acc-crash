from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar el motor de OpenAI 
engine = "gpt-3.5-turbo"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt):
  completion = client.chat.completions.create(
  model=engine,
  messages=[
      {"role": "system", "content": "Eres un experto en seguridad informática con más de 10 años de experiencia, \
          tu conocimiento se extiende por múltipleas aspectos de la seguridad informática y física y dispones de \
              numerosas certificaciones en este campo. Además eres experto en administración de sistemas."},
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return completion

prompt = (
    f"Explica cómo funcionan los firewalls en términos sencillos, como si estuvieras enseñando a un estudiante de primer año en informática."
)


respuesta = get_completion(prompt)
print(respuesta.choices[0].message.content)