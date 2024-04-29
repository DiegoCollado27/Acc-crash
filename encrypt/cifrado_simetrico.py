from cryptography.fernet import Fernet

# Generar una clave simétrica
def generar_clave():
    return Fernet.generate_key()

clave = generar_clave()


def cifrar_nombre(nombre, clave):
    # Crear una instancia de Fernet con la clave proporcionada
    f = Fernet(clave)

    # Codificar el nombre y cifrarlo
    nombre_codificado = nombre.encode()
    nombre_cifrado = f.encrypt(nombre_codificado)

    return nombre_cifrado


def descifrar_nombre(nombre_cifrado, clave):
    # Crear una instancia de Fernet con la clave proporcionada
    f = Fernet(clave)

    # Descifrar y decodificar el nombre
    nombre_descifrado = f.decrypt(nombre_cifrado)
    nombre_original = nombre_descifrado.decode()

    return nombre_original

# Generar clave
clave = generar_clave()

# Cifrar un nombre
nombre_cifrado = cifrar_nombre("Carlos Garcia", clave)
print("Nombre Cifrado:", nombre_cifrado)

# Descifrar el nombre
nombre_descifrado = descifrar_nombre(nombre_cifrado, clave)
print("Nombre Descifrado:", nombre_descifrado)