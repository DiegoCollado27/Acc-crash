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

texto = f"""
En un día cálido de primavera, el prado se despliega como un tapiz de flores silvestres, \
pintando el campo con pinceladas de amarillo, rosa y azul. El aire está impregnado del \
dulce aroma de la lavanda y el jazmín. El lindero del bosque cercano proporciona un contraste \
sereno, con sus árboles altos y robustos que parecen susurrar secretos con el viento. La brisa \
suave acaricia tu piel, invocando una sensación de paz inmediata. El trino de los pájaros \
se mezcla con el murmullo de un arroyo cercano, creando una sinfonía natural que parece celebrar \
la renovación de la vida. El mundo aquí es un remanso de tranquilidad y belleza simple.
"""
prompt = f"""
Te proporcionaré un texto en comillas triples
Si contiene una secuencia de instrucciones, \
re-escribe esas instrucciones en el siguiente formato:

Paso 1 - ...
Paso 2 - …
…
Paso N - …

Si el texto no contiene una secuencia de instrucciones, \
entonces simplemente escribe \"No se proporcionan instrucciones.\"

\"\"\"{texto}\"\"\"
"""
response = get_completion(prompt)
print("Respuesta para texto:")
print(response)