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
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return completion

text = f"""
En un encantador pueblo, los hermanos Juan y Julia emprendieron \
una misión para buscar agua en un pozo situado en la cima de \
una colina. Mientras subían cantando alegremente, la desgracia \
les golpeó: Juan tropezó con una piedra y rodó \
cuesta abajo, seguido de Julia. \
Aunque un poco magullados, el par regresó a casa a \
abrazos reconfortantes. A pesar del contratiempo, \
su espíritu aventurero permaneció intacto, y continuaron \
explorando con alegría.
"""

# Ejemplo 1
prompt_1 = f"""
Realiza las siguientes acciones:
1 - Resume el siguiente texto delimitado por triples \
comillas invertidas en una sola oración.
2 - Traduce el resumen al francés.
3 - Enumera cada nombre en el resumen francés.
4 - Muestra un objeto json que contenga las siguientes \
claves: resumen_frances, num_nombres.

Separa tus respuestas con saltos de línea.

Texto:
```{text}```
"""

# Asumiendo que get_completion es una función definida para obtener la respuesta del modelo
response = get_completion(prompt_1)
print("Respuesta para el ejemplo 1:")
print(response.choices[0].message.content)
