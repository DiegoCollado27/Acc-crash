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
prompt_template = PromptTemplate(
    template="Responde con un chiste a la solicitud del usuario.\n{query}\n",
    input_variables=["query"]
)

chain = prompt_template | model | parser

# Invocar la cadena con el parámetro dinámico
queries = [{"query": "¿cómo se llama el mayor ladrón de china?"}, {"query": "¿Cómo se llama el mejor mecánico árabe?"}]


responses = chain.batch(queries, config={"max_concurrency": 5})

for query, response in zip(queries, responses):
    print(f"Pregunta: {query['query']}\nRespuesta: {response}\n")