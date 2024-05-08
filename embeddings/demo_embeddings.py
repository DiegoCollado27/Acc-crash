from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Crear un stemmer en español
stemmer = SnowballStemmer('spanish')
nltk.download('punkt')
nltk.download('stopwords')
# Lista de stopwords en español
stop_words = set(stopwords.words('spanish'))

def limpiar_texto(texto):
    # Tokenizar el texto
    palabras = word_tokenize(texto)
    # Quitar puntuación y stopwords
    palabras_filtradas = [stemmer.stem(palabra.lower()) for palabra in palabras if palabra.isalpha() and palabra.lower() not in stop_words]
    return palabras_filtradas

# Ejemplo de datos: nombres de películas y sus descripciones
peliculas = [
    "El Padrino: Don Vito Corleone es el respetado y temido jefe de una de las cinco familias de la mafia de Nueva York en los años 40. El hombre tiene cuatro hijos: Connie, Sonny, Fredo y Michael, que no quiere saber nada de los negocios sucios de su padre. Cuando otro capo, Sollozzo, intenta asesinar a Corleone, empieza una cruenta lucha entre los distintos clanes.",
    "Toy Story: Los juguetes de Andy, un niño de seis años, temen que un nuevo regalo les sustituya en el corazón de su dueño. Woody, un vaquero que ha sido hasta ahora el juguete favorito, trata de tranquilizarlos hasta que aparece Buzz Lightyear. Lo peor es que el arrogante Buzz se cree que es una auténtico astronauta en plena misión para regresar a su planeta.",
    "Forrest Gump: Sentado en un banco en Savannah, Georgia, Forrest Gump espera al autobús. Mientras éste tarda en llegar, el joven cuenta su vida a las personas que se sientan a esperar con él. Aunque sufre un pequeño retraso mental, esto no le impide hacer cosas maravillosas. Sin entender del todo lo que sucede a su alrededor, Forrest toma partido en los eventos más importantes de la historia de los Estados Unidos.",
    "La lista de Schindler: Oskar Schindler, un empresario alemán, salva la vida de más de mil judíos polacos durante el Holocausto al emplearlos en sus fábricas. La película narra su evolución desde un oportunista indiferente a un héroe improbable y compasivo.",
    "El Señor de los Anillos: La Comunidad del Anillo: En la Tierra Media, Frodo Bolsón, un joven hobbit, es encargado de destruir un anillo poderoso y malvado antes de que caiga en manos del oscuro señor Sauron. La formación de la Comunidad del Anillo tiene como objetivo ayudar a Frodo en su misión.",
    "Matrix: Thomas A. Anderson es un programador de día y un hacker llamado Neo de noche. Sospechando que algo anda mal con el mundo, Neo descubre la verdad sobre la Matrix, una simulación virtual creada para someter a la humanidad, y se une a la lucha contra sus controladores.",
    "Amelie: En París, Amelie Poulain, una joven camarera, decide cambiar la vida de las personas a su alrededor para mejor, mientras lucha con su propia soledad. Sus buenas acciones provocan una cadena de eventos inesperados.",
    "Pulp Fiction: Las vidas de dos sicarios, un boxeador, la esposa de un mafioso y dos bandidos se entrelazan en cuatro historias de violencia y redención.",
    "El club de la lucha: Un empleado de oficina insomne y un carismático vendedor de jabón forman un club de lucha clandestino que se convierte en algo mucho más grande. La película explora temas de consumismo, insatisfacción y la búsqueda de identidad.",
    "Gladiator: En el año 180, el general romano Maximus Decimus Meridius es traicionado cuando el hijo del emperador asesina a su propio padre y se apodera del trono. Reducido a la esclavitud, Maximus se convierte en gladiador y lucha por su venganza.",
    "Interestelar: En un futuro cercano, la Tierra está siendo devastada por desastres naturales. Un equipo de astronautas viaja a través de un agujero de gusano en busca de un nuevo hogar para la humanidad. La película explora temas de amor, sacrificio y la lucha por la supervivencia."
]

peliculas_limpia = [limpiar_texto(pelicula) for pelicula in peliculas]
# Entrenar el modelo Word2Vec
modelo = Word2Vec(peliculas_limpia, vector_size=100, window=5, min_count=1, workers=4, sg=1)

# Ejemplo de uso: encontrar palabras similares a 'familia'
palabras_similares = modelo.wv.most_similar(stemmer.stem('familia'), topn=5)
print(palabras_similares)
