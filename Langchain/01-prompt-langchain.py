from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os



# Cargar variables de entorno
load_dotenv()

# Configurar el motor de OpenAI 
engine = "gpt-4"
api_key=os.getenv("OPENAI_API_KEY")

# Inicializar el modelo de OpenAI con la clave de API

model = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()
prompt_template = PromptTemplate.from_template("Cuéntame un chiste de padre")
prompt_template.format()

chain = prompt_template | model | parser

print(chain.invoke({}))