from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generar_par_claves():
    # Generar una clave privada
    clave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Generar la clave pública correspondiente
    clave_publica = clave_privada.public_key()

    return clave_publica, clave_privada

clave_publica, clave_privada = generar_par_claves()

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def cifrar_nombre_asimetrico(nombre, clave_publica):
    nombre_codificado = nombre.encode()
    
    nombre_cifrado = clave_publica.encrypt(
        nombre_codificado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return nombre_cifrado

def descifrar_nombre_asimetrico(nombre_cifrado, clave_privada):
    nombre_descifrado = clave_privada.decrypt(
        nombre_cifrado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return nombre_descifrado.decode()

# Generar par de claves
clave_publica, clave_privada = generar_par_claves()

# Cifrar un nombre
nombre_cifrado = cifrar_nombre_asimetrico("Carlos Garcia", clave_publica)
print("Nombre Cifrado:", nombre_cifrado)

# Descifrar el nombre
nombre_descifrado = descifrar_nombre_asimetrico(nombre_cifrado, clave_privada)
print("Nombre Descifrado:", nombre_descifrado)
print("texto".encode())