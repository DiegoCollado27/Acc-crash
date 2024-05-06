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
      {"role": "system", "content": "Eres un asistente, que realizas traducciones y cambias estilos de textos."},
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return completion

texto_en_ingles = """The mysterious forest was shrouded in a thick mist, obscuring the path ahead. Ancient trees towered high, \
    their branches weaving a canopy above, while the distant sound of a waterfall whispered secrets of the land. In this realm, \
    where time seemed to stand still, legends spoke of an enchanted crystal hidden deep within the heart of the woods, \
    guarded by creatures of old lore. The journey to find this crystal was not just a quest for a treasure, but a voyage \
    into the very soul of the forest, a test of courage and wisdom for any brave adventurer daring to uncover its mysteries."""

prompt_tolkien_style = (
    f"Primero, traduce el siguiente texto del inglés al español: '{texto_en_ingles}'. "
    "Luego, adapta la traducción al estilo de J.R.R. Tolkien, utilizando un lenguaje formal y arcaico, "
    "con descripciones detalladas y elementos de fantasía, manteniendo la esencia del texto original."
)

prompt_slang_style = (
    f"No traduzcas el texto y reescribe el siguiente texto en un estilo de 'slang' americano, manteniendo la historia y los elementos principales, "
    f"pero utilizando expresiones y lenguaje coloquial típicos del slang moderno de Estados Unidos: '{texto_en_ingles}'"
)

respuesta = get_completion(prompt_slang_style)
print(respuesta.choices[0].message.content)

