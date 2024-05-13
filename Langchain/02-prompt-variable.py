from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar el motor de OpenAI
engine = "gpt-4"
api_key = os.getenv("OPENAI_API_KEY")

# Inicializar el modelo de OpenAI con la clave de API
model = ChatOpenAI(model=engine, api_key=api_key)
parser = StrOutputParser()

# Modificar el PromptTemplate para incluir un placeholder para el tipo de chiste
prompt_template = PromptTemplate.from_template("Cuéntame un chiste de {tipo}.")

# Suponiendo que queremos un chiste de padre
tipo_chiste = "padre"
#formatted_prompt = prompt_template.format(tipo=tipo_chiste)

chain = prompt_template | model | parser

# Invocar la cadena con el parámetro dinámico
response = chain.invoke({"tipo": tipo_chiste})
print(response)
