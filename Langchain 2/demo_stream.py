from langchain_openai import ChatOpenAI
import asyncio
import time
# Primero autenticamos el usuario :
import sys

from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv()

# Configurar el motor de OpenAI 
engine = "gpt-3.5-turbo"
api_key=os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=api_key)

chunks = []

async def chatear():
    
    async for chunk in model.astream("hello. tell me something about yourself"):
        # print(len(chunk.content.split()))
        await asyncio.sleep(0.1)
        # cada chunk.content es una cadena de texto

        print(chunk.content, end="", flush=True)

   
        
asyncio.run(chatear())
