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
      {"role": "system", "content": "Eres un experto arquitecto de software, to tarea es generar código de alta calidad, \
          considerando las mejores prácticas de programación, y seguridad en el código, con comentarios claros y un enfoque en la seguridad, eficiencia y la legibilidad."},
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return completion

prompt = (
    f"Necesito un snippet de código en Python para realizar una consulta SELECT en una base de datos MySQL. Debe incluir manejo de errores y usar la librería SQLAlchemy"
)


respuesta = get_completion(prompt)
print(respuesta.choices[0].message.content)