# -*- coding: utf-8 -*-
"""glove_embeddings.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CHBXMuoYAMWHbU3WfrJ14vzBpyWU95Me
"""

from gensim.models import KeyedVectors
import os

# Cargar el modelo GloVe (Asegúrate de ajustar la ruta al archivo GloVe)
from gensim.scripts.glove2word2vec import glove2word2vec

#glove_input_file = glove_filename
word2vec_file = 'drive/MyDrive/Colab Notebooks/data/glove.6B.100d.txt'
model_file = 'drive/MyDrive/Colab Notebooks/data/glove_model'
if os.path.exists(model_file):
    model = KeyedVectors.load(model_file)
else:
    try:
        model = KeyedVectors.load_word2vec_format(word2vec_file, binary=False, no_header=True)
        model.save(model_file)
    except:
        print('No encuentro el modelo')

# Realizar la operación vectorial
mother_prueba = model['father'] - model['man'] + model['woman']

# Encontrar las palabras más cercanas al vector resultante
palabras_mas_similares = model.similar_by_vector(mother_prueba)

print("Las palabras más similares son:")
for word, similaridad in palabras_mas_similares:
    print(f"{word}: {similaridad}")

#print('king: ',model.get_vector('king'))

result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)

print('Palabras más similares para King + Woman - Man: ', result)

frase = model.most_similar(positive=['the', 'man', 'that', 'rules', 'boss'])
print('Palabras más similares para frase: ', frase)

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1. Selección de Palabras
palabras = ['king', 'queen', 'man', 'woman', 'prince', 'princess', 'tiger', 'lion', 'monkey', 'tree']

# 2. Extracción de Vectores
vectores = [model[word] for word in palabras]

# 3. Reducción de Dimensionalidad
pca = PCA(n_components=2)
vectores_reducidos = pca.fit_transform(vectores)

# 4. Visualización
plt.figure(figsize=(10, 8))
for palabra, vector in zip(palabras, vectores_reducidos):
    plt.scatter(vector[0], vector[1])
    plt.text(vector[0] + 0.05, vector[1] + 0.05, palabra)

plt.title('Representación 2D de Palabras en el Espacio Vectorial')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.grid(True)
plt.show()

pca = PCA(n_components=3)  # Cambia n_components a 3 para reducir a 3 dimensiones
vectores_reducidos = pca.fit_transform(vectores)

# 4. Visualización en 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')  # Configura el subplot para 3D

# Descompone los vectores reducidos en sus tres componentes
x = vectores_reducidos[:, 0]
y = vectores_reducidos[:, 1]
z = vectores_reducidos[:, 2]

ax.scatter(x, y, z, depthshade=True, s=50)  # Dibuja los puntos en 3D

# Etiqueta cada punto con su palabra correspondiente
for i, palabra in enumerate(palabras):
    ax.text(x[i], y[i], z[i], palabra)

ax.set_title('Representación 3D de Palabras en el Espacio Vectorial')
ax.set_xlabel('Componente Principal 1')
ax.set_ylabel('Componente Principal 2')
ax.set_zlabel('Componente Principal 3')
plt.show()

"""### Usando tokenizador y frase"""

import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# Frases a analizar
frases = ["A dragon lives in a deep cave near the village",
          "In a hole in the ground there lived a hobbit."]

# calcular el vector promedio de una frase
def vector_promedio_frase(frase, modelo):
    # Tokenización simple por espacios

    palabras = frase.lower().split()
    vectores = []

    for palabra in palabras:
        if palabra not in stop_words:  # Filtra stopwords
            try:
                vectores.append(modelo[palabra])
            except KeyError:
                # Si la palabra no está en el modelo, la omitimos
                continue

    # Si no se encontraron vectores válidos, regresa un vector de ceros
    if len(vectores) == 0:
        return np.zeros(modelo.vector_size)

    # Calcula el promedio de los vectores
    vector_promedio = np.mean(vectores, axis=0)
    return vector_promedio

# Calcular vectores promedio para cada frase
vectores_promedio_frases = [vector_promedio_frase(frase, model) for frase in frases]

# Ahora, para demostración, buscar palabras similares al vector promedio de cada frase
for i, vector in enumerate(vectores_promedio_frases):
    palabras_mas_similares = model.similar_by_vector(vector)
    print(f"Palabras más similares a la frase {i+1}:")
    for palabra, similaridad in palabras_mas_similares:
        print(f"{palabra}: {similaridad}")
    print("\n")