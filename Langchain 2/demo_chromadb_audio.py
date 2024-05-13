import os
from dotenv import load_dotenv

from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
import streamlit as st
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")


# Cargar variables de entorno
load_dotenv()

speech_file_path = '../data/speech.mp3'
# Ubicación del archivo de la base de datos

loader = CSVLoader(file_path='../data/combined_info_movies.csv')
movies = loader.load()
database_file = 'data/chroma.sqlite3'

if os.path.exists(database_file):

    db = Chroma(persist_directory='../data/', embedding_function=OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY")), collection_name='movies_chroma.db')
    db.get()
    st.status("Cargada DB", expanded=False, state="complete")
else:
    # Crear la base de datos desde documentos si no existe
    db = Chroma.from_documents(movies, OpenAIEmbeddings(api_key=os.getenv(
        "OPENAI_API_KEY")), persist_directory='../data/', collection_name='movies_chroma.db')
    # Guardar la base de datos
    db.persist()
    st.status("Creada DB", expanded=False, state="complete")


def process_movie_speech(movie):
    """ Usa openai speech para describir la película

    Args:
        movie (_type_): _description_

    Returns:
        _type_: _description_
    """
    docs = db.similarity_search(movie)

    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=f"The movie you a referring to probably is: {docs[0].page_content}"
    )
    response.write_to_file(speech_file_path)
    return speech_file_path


query = "Someone called Tony that works for a secret Agency"

movie = st.text_input('Describe la película', query)

if movie:
    # Llamar a la función con el título de la película y obtener la ruta del archivo de audio
    speech_file_path = process_movie_speech(movie)

    # Mostrar el archivo de audio en Streamlit
    st.audio(str(speech_file_path), format='audio/mp3')
