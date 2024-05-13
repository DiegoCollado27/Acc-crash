import sys
import asyncio
from langchain_openai import ChatOpenAI
import tiktoken
# Primero autenticamos el usuario :

from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv()
encoding = tiktoken.encoding_for_model("gpt-4")

# Configurar el motor de OpenAI
engine = "gpt-4"
api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=api_key)

chunks = []


async def chatear():
    """demo chatear asincrono
    """
    token_count = 0
    async for chunk in model.astream("hello. tell me something about yourself"):
        # Contar los tokens en el chunk actual

        tokens_in_chunk = len(encoding.encode(chunk.content))

        token_count += tokens_in_chunk
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)
        print(f" [Tokens hasta ahora: {token_count}]|", flush=True)

asyncio.run(chatear())
