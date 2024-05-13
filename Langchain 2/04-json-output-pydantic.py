
from langchain_core.pydantic_v1 import BaseModel, Field
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

class Chiste(BaseModel):
    """Define la estructura de chiste

    Args:
        BaseModel (_type_): _description_
    """
    pregunta: str = Field(description="pregunta para preparar el chiste")
    respuesta: str = Field(description="respuesta para resolver el chiste")

joke_query = "Tell me a joke."

# Configura un parser + inyecta instrucciones en el prompt template.
parser = JsonOutputParser(pydantic_object=Chiste)

prompt = PromptTemplate(
    template="Responde de manera ingeniosa y divertida.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

response = chain.invoke({"query": joke_query})

print(response)