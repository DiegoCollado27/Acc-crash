from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
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
parser = JsonOutputParser()

# Modificar el PromptTemplate para incluir un placeholder para el tipo de chiste
prompt_template = PromptTemplate(
    template="Responde con un chiste a la solicitud del usuario.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | model | parser

# Invocar la cadena con el parámetro dinámico
response = chain.invoke({"query": "Por qué los científicos no confían en los átomos?"})
print(response)
