import logging
from icecream import ic

if __name__ == "__main__":
    ic.configureOutput(prefix='🐞 Debug | ')
    
    logging.basicConfig(filename='mis_logs_dev.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8')
    logging.debug("Este es un mensaje de debug")
    logging.info("Información general")
    logging.warning("Advertencia: algo no está del todo bien")
    logging.error("Error: algo falló")
    logging.critical("Crítico: fallo grave")

    x = 10
    y = 20
    resultado = x + y

    ic(x)
    ic(y)
    ic(resultado)
    
    def suma(a, b):
        return a + b

    ic(suma(1, 2))
    
    def dividir(a, b):
        try:
            resultado_division = a / b
        except ZeroDivisionError as e:
            # Usando logging para registrar la excepción en un archivo
            logging.error("Error de división por cero: %s", str(e))
            # Usando ic para salida descriptiva en consola
            ic("No se puede dividir un numero entre 0")
            ic(e)
            return None
        return resultado_division

    # Ejemplo de llamada a la función
    dividir(10, 0)