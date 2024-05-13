from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar el motor de OpenAI
engine = "gpt-4"
api_key = os.getenv("OPENAI_API_KEY")

# Inicializar el modelo de OpenAI con la clave de API
model = ChatOpenAI(model=engine, api_key=api_key, temperature=0)
output_parser = CommaSeparatedListOutputParser()

format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | model | output_parser

response = chain.invoke({"subject": "tonos de color azul"})

print(response)
# tratamos como un stream
#for s in chain.stream({"subject": "tonos de color azul"}):
#    print(s)