import hashlib

def hash_nombre_apellido(nombre, apellido):
    # Concatenar nombre y apellido
    nombre_completo = nombre + " " + apellido

    # Codificar el nombre completo para prepararlo para el hashing
    nombre_completo_codificado = nombre_completo.encode()

    # Crear el hash usando SHA-256
    hash_objeto = hashlib.sha256(nombre_completo_codificado)

    
    # Obtener el valor hash hexadecimal
    hash_hex = hash_objeto.hexdigest()

    return hash_hex

def hash_md5nombre_apellido(nombre, apellido):
    # Concatenar nombre y apellido
    nombre_completo = nombre + " " + apellido

    # Codificar el nombre completo para prepararlo para el hashing
    nombre_completo_codificado = nombre_completo.encode()

    # md5
    hash_objeto_md5 = hashlib.md5(nombre_completo_codificado)
    # Obtener el valor hash hexadecimal
    hash_hex = hash_objeto_md5.hexdigest()

    return hash_hex

nombre_anonimizado = hash_nombre_apellido("Carlos", "Garcia")
nombre_anonimizado_md5 = hash_md5nombre_apellido("Carlos", "Garcia")
print(nombre_anonimizado)  # Muestra el hash del nombre "Carlos García"
print(nombre_anonimizado_md5)