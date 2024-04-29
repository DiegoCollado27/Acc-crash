import hashlib
import os

def generar_salt(longitud=16):
    # Retorna un salt aleatorio con la longitud especificada
    return os.urandom(longitud)

def hash_con_salt(nombre, apellido):
    nombre_completo = nombre + " " + apellido
    nombre_completo_codificado = nombre_completo.encode()

    salt = generar_salt()
    # Combinar el nombre completo codificado con el salt
    entrada_con_salt = nombre_completo_codificado + salt

    # Crear el hash
    hash_objeto = hashlib.sha256(entrada_con_salt)
    hash_hex = hash_objeto.hexdigest()

    return hash_hex

# Ejemplo de uso
nombre_anonimizado = hash_con_salt("Juan", "Pérez")
print(nombre_anonimizado)