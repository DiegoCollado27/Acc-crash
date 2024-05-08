import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
from gensim.models import Word2Vec, FastText
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Cargar datos
df = pd.read_excel('excel_movies.xlsx')
df['overview'] = df['overview'].fillna(' ').astype('str')
# Preprocesamiento básico sin dividir en palabras
df['overview_clean'] = df['overview'].str.lower()  # Convertir a minúsculas

# Tokenización por frases (un ejemplo simple podría ser dividir por puntos)
# Esto es más un pseudocódigo, ajusta según tus necesidades
df['overview_frases'] = df['overview_clean'].apply(lambda x: x.split('. '))

# Ahora 'overview_phrases' contiene listas de frases
descripciones_frases = df['overview_frases'].tolist()

# Inicializar el modelo FastText sin entrenar
modelo_fasttext = FastText(vector_size=300, window=10, min_count=1, epochs=15, workers=4)
modelo_fasttext.build_vocab(descripciones_frases)
modelo_fasttext.train(descripciones_frases, total_examples=modelo_fasttext.corpus_count, epochs=modelo_fasttext.epochs)

def obtener_vector_pelicula(palabras_pelicula, modelo_param):
    vectores = [modelo_param.wv[palabra] for palabra in palabras_pelicula if palabra in modelo_param.wv]
    if not vectores:
        return np.zeros(modelo_param.vector_size)
    vector_pelicula = np.mean(vectores, axis=0)
    return vector_pelicula

vectores_peliculas_fasttext = np.array([obtener_vector_pelicula(pelicula, modelo_fasttext) for pelicula in descripciones_frases])

# Función para encontrar películas similares 
def peliculas_similares(index, vectores_peliculas_param):
    similitudes = cosine_similarity([vectores_peliculas_param[index]], vectores_peliculas_param)[0]
    indices_similares = np.argsort(similitudes)[::-1][1:6]
    return [(indice, similitudes[indice]) for indice in indices_similares]

# Ejemplo de uso con FastText 
indice_pelicula = 867  # Cambiar por el índice de la película de interés
print(f"... buscando similares a '{df.iloc[indice_pelicula]['title']}' con FastText:")
peliculas_sim = peliculas_similares(indice_pelicula, vectores_peliculas_fasttext)
for pelicula_idx in peliculas_sim:
    print(df.iloc[pelicula_idx[0]]['title'])
