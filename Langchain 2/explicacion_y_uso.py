class MiCadena:
    def __init__(self, next_process=None):
        self.next_process = next_process

    def __or__(self, other):
        self.next_process = other
        return other

    def process(self, data):
        raise NotImplementedError(
            "This method should be implemented by subclasses.")


class PromptTemplate(MiCadena):
    def process(self, data):
        data = f"Prompt procesado: {data}"
        if self.next_process:
            return self.next_process.process(data)
        return data


class Model(MiCadena):
    def process(self, data):
        data = f"Salida del modelo: {data}"
        if self.next_process:
            return self.next_process.process(data)
        return data


class Parser(MiCadena):
    def process(self, data):
        data = f"Datos procesados salida: {data}"
        if self.next_process:
            return self.next_process.process(data)
        return data


# Creando instancias de cada componente
prompt = PromptTemplate()
model = Model()
parser = Parser()

# Encadenando compontes
chain = prompt | model | parser

# Utilizando la cadena para procesar un input
result = prompt.process("Hola mundo")
# IMporime el resultado
print(result)
