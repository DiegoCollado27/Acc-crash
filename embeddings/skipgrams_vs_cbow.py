from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Ejemplo de datos: frases sobre tecnología
datos = [
    "La inteligencia artificial está transformando el mundo.",
    "Las redes neuronales pueden identificar patrones complejos.",
    "El aprendizaje profundo es una técnica clave en IA.",
    "Python es popular en la ciencia de datos."
]

# Lista de stopwords en español
stop_words = set(stopwords.words('spanish'))

# Tokenización de las frases y eliminación de stopwords
datos_tokenizados = [[palabra for palabra in word_tokenize(frase.lower()) if palabra not in stop_words]
                     for frase in datos]

# Entrenamiento del modelo Word2Vec con Skip-grams
modelo_skip_grams = Word2Vec(sentences=datos_tokenizados, vector_size=100, window=5, min_count=1, workers=4, sg=1)

# Entrenamiento del modelo Word2Vec con CBOW
modelo_cbow = Word2Vec(sentences=datos_tokenizados, vector_size=100, window=5, min_count=1, workers=4, sg=0)

# Ejemplo de uso con Skip-grams - Más lento, mejor con palabras raras o contextos más complejos
vector_palabra_sg = modelo_skip_grams.wv['python']
palabras_similares_sg = modelo_skip_grams.wv.most_similar('python')

# Ejemplo de uso con CBOW - Más rápido, mejor con palabras comunes
vector_palabra_cbow = modelo_cbow.wv['python']
palabras_similares_cbow = modelo_cbow.wv.most_similar('python')

print("Skip-grams - Vector de 'python':", vector_palabra_sg)
print("Skip-grams - Palabras similares a 'python':", palabras_similares_sg)
print("CBOW - Vector de 'python':", vector_palabra_cbow)
print("CBOW - Palabras similares a 'python':", palabras_similares_cbow)
