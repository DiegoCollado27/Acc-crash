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
    "Python es popular en la ciencia de datos.",
    "Los algoritmos de machine learning mejoran con el tiempo.",
    "La visión por computadora permite a las máquinas 'ver'.",
    "El procesamiento de lenguaje natural facilita la interacción humano-máquina.",
    "Los sistemas de recomendación personalizan la experiencia en línea.",
    "La robótica utiliza IA para realizar tareas complejas.",
    "Los vehículos autónomos emplean IA para navegar.",
    "La seguridad informática se fortalece mediante el uso de IA.",
    "La inteligencia artificial contribuye al desarrollo de la medicina personalizada.",
    "Las ciudades inteligentes utilizan IA para mejorar la vida urbana.",
    "La IA en la agricultura ayuda a optimizar la producción."
]

# Lista de stopwords en español
stop_words = set(stopwords.words('spanish'))

# Tokenización de las frases y eliminación de stopwords
datos_tokenizados = [[palabra for palabra in word_tokenize(frase.lower()) if palabra not in stop_words]
                     for frase in datos]

# Entrenamiento del modelo Word2Vec
modelo = Word2Vec(sentences=datos_tokenizados, vector_size=100, window=5, min_count=1, workers=4)

# Obtener el vector de una palabra
vector_palabra = modelo.wv['python']

# Encontrar palabras similares
palabras_similares = modelo.wv.most_similar('python')

print("Vector de 'python':", vector_palabra)
print("Palabras similares a 'python':", palabras_similares)
