import os
import hashlib
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
print(os.getcwd())

# Obtener el salt del archivo .env
salt = os.environ.get("SALT").encode()

def hash_con_salt(nombre, apellido):
    nombre_completo = nombre + " " + apellido
    nombre_completo_codificado = nombre_completo.encode()

    # Combinar el nombre completo codificado con el salt
    entrada_con_salt = nombre_completo_codificado + salt

    # Crear el hash
    hash_objeto = hashlib.sha256(entrada_con_salt)
    hash_hex = hash_objeto.hexdigest()

    return hash_hex

# Ejemplo de uso
nombre_anonimizado = hash_con_salt("Juan", "Pérez")
print(nombre_anonimizado)