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
      {"role": "system", "content": "Eres un asistente, que realizas resúmenes concisos y proporcionas la ideas principales de un texto. \
          Estas ideas las proporciones en un objeto json con la propiedad 'analisis', que contendrá un array 'ideas' con esas ideas. Finalmente agregas una conclusión \
          general a partir de la idea principal del texto y lo agregas al objeto json en una propiedad llamada 'conclusion'. El objeto json deberá incluir un metadato con \
          la version 1.0 llamado 'version' y la licencia que será 'CC-BY-SA 4.0'."},
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return completion

text = f"""
La propiedad de una vivienda probablemente marca la diferencia en este gráfico, ya que las personas en algunos países prefieren ser propietarios de su casa en  \
lugar de alquilarla. Pero esto demuestra que la casa en la que vives no es realmente una inversión porque no puedes sacar provecho de ella a menos que la vendas y te \
mudes a un lugar más barato, o decidas alquilar. Y seamos realistas, la mayoría de las personas no buscan vender su casa sólo porque su valor ha aumentado. Es una \
lástima que por una vez estemos superando a Alemania en la tabla de riqueza, pero eso no significa que tengamos más dinero para gastar.
"""
prompt = f"""
Resume el texto delimitado por triples acentos graves: 
```{text}```
"""
response = get_completion(prompt)
print(response.choices[0].message.content)

