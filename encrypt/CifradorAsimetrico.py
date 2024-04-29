from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

class CifradorAsimetrico:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.clave_publica, self.clave_privada = self.generar_par_claves()

    def generar_par_claves(self):
        clave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
        )
        clave_publica = clave_privada.public_key()
        return clave_publica, clave_privada

    def cifrar_nombre(self, nombre):
        nombre_codificado = nombre.encode()
        nombre_cifrado = self.clave_publica.encrypt(
            nombre_codificado,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return nombre_cifrado

    def descifrar_nombre(self, nombre_cifrado):
        nombre_descifrado = self.clave_privada.decrypt(
            nombre_cifrado,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return nombre_descifrado.decode()

# Uso de la clase
encryption = CifradorAsimetrico()
cliente_cifrado = encryption.cifrar_nombre("Carlos Garcia")
print("Nombre Cifrado:", cliente_cifrado)

cliente_descifrado = encryption.descifrar_nombre(cliente_cifrado)
print("Nombre Descifrado:", cliente_descifrado)
