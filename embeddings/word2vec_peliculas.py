from gensim.models import Word2Vec, FastText
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Cargar datos
df = pd.read_excel('excel_movies.xlsx')
peliculas = df['combined_text'].apply(lambda x: x.split())  # Asegurarse de que cada película sea una lista de palabras

# Inicializar el modelo Word2Vec sin entrenar
modelo_word2vec = Word2Vec(vector_size=150, window=5, min_count=1, workers=4)
modelo_word2vec.build_vocab(peliculas)
# Entrenar el modelo Word2Vec
modelo_word2vec.train(peliculas, total_examples=modelo_word2vec.corpus_count, epochs=10)  # Ajusta el número de épocas según sea necesario

# Inicializar el modelo FastText sin entrenar
modelo_fasttext = FastText(vector_size=150, window=5, min_count=1, workers=4)
modelo_fasttext.build_vocab(peliculas)
# Entrenar el modelo FastText
modelo_fasttext.train(peliculas, total_examples=modelo_fasttext.corpus_count, epochs=10)  # Ajusta el número de épocas según sea necesario

def obtener_vector_pelicula(palabras_pelicula, modelo_param):
    vectores = [modelo_param.wv[palabra] for palabra in palabras_pelicula if palabra in modelo_param.wv]
    if not vectores:
        return np.zeros(modelo_param.vector_size)
    vector_pelicula = np.mean(vectores, axis=0)
    return vector_pelicula

# Asegúrate de seleccionar el modelo correcto aquí, por ejemplo, `modelo_fasttext` o `modelo_word2vec`
vectores_peliculas_word2vec = np.array([obtener_vector_pelicula(pelicula, modelo_word2vec) for pelicula in peliculas])
vectores_peliculas_fasttext = np.array([obtener_vector_pelicula(pelicula, modelo_fasttext) for pelicula in peliculas])

# Función para encontrar películas similares (se puede reutilizar sin cambios)
def peliculas_similares(index, vectores_peliculas_param):
    similitudes = cosine_similarity([vectores_peliculas_param[index]], vectores_peliculas_param)[0]
    indices_similares = np.argsort(similitudes)[::-1][1:6]
    return [(indice, similitudes[indice]) for indice in indices_similares]

# Ejemplo de uso con FastText (cambia `vectores_peliculas_fasttext` a `vectores_peliculas_word2vec` si quieres usar Word2Vec)
indice_pelicula = 0  # Cambiar por el índice de la película de interés
print(f"... buscando similares a '{df.iloc[indice_pelicula]['title']}' con FastText:")
peliculas_sim = peliculas_similares(indice_pelicula, vectores_peliculas_fasttext)
for pelicula_idx in peliculas_sim:
    print(df.iloc[pelicula_idx[0]]['title'])


print(f"... buscando similares a '{df.iloc[indice_pelicula]['title']}' con Word2Vec:")
peliculas_sim = peliculas_similares(indice_pelicula, vectores_peliculas_word2vec)
for pelicula_idx in peliculas_sim:
    print(df.iloc[pelicula_idx[0]]['title'])

