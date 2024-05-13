import re
import streamlit as st
from bs4 import BeautifulSoup
from scipy.spatial.distance import cosine
from text_processor import TextProcessor
import numpy as np
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer  # para tags
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
# nltk.download('wordnet')
app = FastAPI()

# Modelo para aceptar texto


def get_data_directory():
    if os.path.exists('data/'):
        return 'data/'  # Si se ejecuta desde Streamlit
    else:
        return '../data/'


data_directory = get_data_directory()


class TextData(BaseModel):
    text: str


def load_data():
    data_path = os.path.join(data_directory, 'train.csv')
    return pd.read_csv(data_path, index_col='Id')


df = load_data()
df = df[:2000]
# print(df.shape)
# print(df.head())

# Configurar el motor de OpenAI
engine = "gpt-3.5-turbo"
client = OpenAI()


def get_embedding(text):
    if isinstance(text, str) and len(text.strip()):
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text
        )
        # Obtener el embedding del primer elemento de la respuesta
        embedding = response.data[0].embedding
        return embedding
    else:
        return np.zeros(3072)


def separar_codigo(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')  # Obtener texto sin código
    # Encontrar todos los bloques de código
    code_blocks = soup.find_all('pre')  # Busca bloques 'pre'

    extracted_code = []

    # Extraemos solo los bloques que contienen 'code'
    for block in code_blocks:
        if block.find('code'):
            # Agregamos el texto del código que hemos encontrado
            extracted_code.append(block.get_text())
            block.decompose()  # Elimina el bloque del árbol de parseo

    code = ' '.join(extracted_code)
    text = soup.get_text(separator=' ')  # Obtener el texto restante

    return text, code


######################### ETIQUETAS ##########################


def limpiar_etiquetas(tags_str: str) -> str:
    # Eliminar los símbolos '<' y '>' y dividir en palabras individuales
    tags = tags_str.strip('><').split('><')
    return " ".join(tags)


def onehot_tags():
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tag_features = vectorizer.fit_transform(df_intermedio['Tags'])

    # Convertir tag_features a DataFrame
    tag_features_df = pd.DataFrame(tag_features.toarray(
    ), columns=vectorizer.get_feature_names_out(), index=df.index)

    return tag_features_df


def generate_code_description(code_snippet):
    if len(code_snippet.strip()):
        # Ensure to replace "code-davinci-002" with the latest model version if it has changed.
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Explain the following code:\n\n{(code_snippet[:3000])}\n\n",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    return ''


def generar_dataframe():

    data_path_xlsx = os.path.join(
        data_directory, 'stackoverflow_processed.xlsx')
    if os.path.exists(data_path_xlsx):
        print('El df intermedio xlsx existe')
        df_intermedio = pd.read_excel(data_path_xlsx)
    else:
        print('El df intermedio xlsx NO existe')
        resultado = df['Body'].apply(separar_codigo)
        df_intermedio = pd.DataFrame(resultado.tolist(), columns=[
                                     'Body', 'Code'], index=df.index)

        df_intermedio['Tags'] = df['Tags'].apply(limpiar_etiquetas)

        df_intermedio['Title'] = df['Title']
        df_intermedio['code_description'] = df_intermedio['Code'].apply(
            generate_code_description)

        df_intermedio.to_excel(data_path_xlsx)

    return df_intermedio


# Obtenemos los embeddings para los títulos

data_path_embeddings = os.path.join(
    data_directory, 'stackoverflow_embeddings.pkl')
if not os.path.exists(data_path_embeddings):

    print('El df procesado pkl NO existe')
    df_intermedio = generar_dataframe()
    df_intermedio['embedding_titles'] = df_intermedio['Title'].apply(
        get_embedding)
    df_intermedio['embedding_bodies'] = df_intermedio['Body'].apply(
        get_embedding)
    df_intermedio['embedding_tags'] = df_intermedio['Tags'].apply(
        get_embedding)
    df_intermedio['embedding_code'] = df_intermedio['code_description'].apply(
        get_embedding)
    # guardamos a un archivo para no tener que volver a pedir los embedding a openai
    df_intermedio.to_pickle(data_path_embeddings)
else:
    # cxargamos los embeddings guardados
    print('El df procesado pkl ya existe')
    df_intermedio = pd.read_pickle(data_path_embeddings)


def preprocesar(texto):
    processor = TextProcessor()
    tfidf_output = processor.process_text(texto, ngram_size=2)
    return tfidf_output.toarray()


def combine_embeddings(row):
    peso_titulos = 1.0
    peso_cuerpos = 1.0
    peso_etiquetas = 1.5
    peso_codigo = 0.8
    embedding_titulos = np.array(row['embedding_titles'])
    embedding_cuerpos = np.array(row['embedding_bodies'])
    embedding_etiquetas = np.array(row['embedding_tags'])
    embedding_codigo = np.array(row['embedding_code']) if len(
        row['embedding_code']) > 0 else np.zeros_like(embedding_etiquetas)

    combined = (embedding_titulos * peso_titulos +
                embedding_cuerpos * peso_cuerpos +
                embedding_etiquetas * peso_etiquetas +
                embedding_codigo * peso_codigo)
    return combined


df_intermedio['combined_embedding'] = df_intermedio.apply(
    combine_embeddings, axis=1)
# normalizamos los embeddings combinados
df_intermedio['combined_embedding'] = df_intermedio['combined_embedding'].apply(
    lambda x: normalize([x])[0])


@st.cache_data
def find_most_similar(new_embedding, all_embeddings):
    similarities = cosine_similarity([new_embedding], all_embeddings)
    most_similar_index = np.argmax(similarities)
    return most_similar_index


@st.cache_data
def find_top5_similar(new_embedding, all_embeddings):

    similarities = cosine_similarity([new_embedding], all_embeddings)[0]
    most_similar_indices = np.argsort(similarities)[::-1]
    return most_similar_indices[:5]


# preparamos los datos para comparación
all_embeddings = np.array(df_intermedio['combined_embedding'].tolist())


# titulo = "I want to build an obfuscator with python, substituting characters on a string, hwat is the best way to accomplish this?"
# embedding_titulo = get_embedding(titulo)
# most_similar_index = find_most_similar(
#    embedding_titulo, all_embeddings)

# most_similar_question = df.iloc[most_similar_index]

# Mostramos la pregunta más similar
# print("La pregunta más similar es:", most_similar_question['Title'])
# print("Detalles:", most_similar_question['Body'])
# Frontend
st.title('Buscador de Preguntas Similares')

# Entrada del usuario
user_question = st.text_input("Escribe tu pregunta aquí:")
if 'df_intermedio' not in st.session_state:
    st.session_state['df_intermedio'] = generar_dataframe()

if st.button('Buscar pregunta similar'):
    if user_question:
        # pedimos pregunta
        user_embedding = get_embedding(user_question)

        # lamamos funcion top5
        top5_similar_indices = find_top5_similar(
            user_embedding, all_embeddings)

        # iloc mas similares
        top5_similar_titles = df.iloc[top5_similar_indices]['Title']

        # mostrar pregunta en pagina
        most_similar_question = df.iloc[top5_similar_indices[0]]

        # mostrar info
        st.subheader("La pregunta más similar es:")
        st.write("Título:", most_similar_question['Title'])
        st.write(
            "Detalles:", most_similar_question['Body'], unsafe_allow_html=True)

        # extraemos e iteramos por tags
        tags = re.findall(r'<(.*?)>', most_similar_question['Tags'])

        st.write("Tags:")
        for tag in tags:
            st.markdown(
                f"<span style='display: inline-block; margin: 5px; padding: 3px; border-radius: 5px; background-color: #f1f1f1;'>{tag}</span>", unsafe_allow_html=True)
        st.sidebar.header("Top 5 Preguntas Similares")
        for title in top5_similar_titles:
            st.sidebar.write(title)
    else:
        st.error("Por favor, introduce una pregunta para buscar.")


@app.post("/find_most_similar/")
async def api_find_most_similar(text_data: TextData):
    new_embedding = get_embedding(text_data.text)
    most_similar_index = find_most_similar(new_embedding, all_embeddings)
    return df.iloc[most_similar_index].to_dict()


@app.post("/find_top5_similar/")
async def api_find_top5_similar(text_data: TextData):
    new_embedding = get_embedding(text_data.text)
    top5_indices = find_top5_similar(new_embedding, all_embeddings)
    results = df.iloc[top5_indices].to_dict('records')
    return {"data": results}
