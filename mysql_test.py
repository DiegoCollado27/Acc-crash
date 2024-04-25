from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
import os

load_dotenv()

Base = declarative_base()

userdb = os.getenv("DB_USER")
passdb = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
database = os.getenv("DATABASE")


def conectar_a_bd():
    URL = f"mysql://{userdb}:{passdb}@{host}/{database}"
    engine = create_engine(URL, echo=True)
    Base.metadata.create_all(engine)  # Crea las tablas si no existen
    Session = sessionmaker(bind=engine)
    return Session()


session = conectar_a_bd()


class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    id_fiscal = Column(String(50), unique=True, nullable=False)
    facturas = relationship("Factura", back_populates="cliente")


class Factura(Base):
    __tablename__ = 'facturas'

    id_factura = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey(
        'clientes.id_cliente'), nullable=False)
    importe = Column(Numeric(10, 2), nullable=False)
    concepto = Column(String(200), nullable=False)
    cliente = relationship("Cliente", back_populates="facturas")

    def __str__(self):
        return f"Factura {self.id_factura}: {self.importe} - {self.concepto} (Cliente {self.id_cliente})"

def crear_cliente(id_cliente,nombre, apellidos, id_fiscal):
    nuevo_cliente = Cliente(
        id_cliente =  id_cliente, nombre=nombre, apellidos=apellidos, id_fiscal=id_fiscal)
    session.add(nuevo_cliente)
    session.commit()
    return nuevo_cliente.id_cliente


def obtener_cliente_por_id(id_cliente):
    cliente = session.query(Cliente).filter(
        Cliente.id_cliente == id_cliente).first()
    return cliente


def actualizar_cliente(id_cliente, nombre, apellidos, id_fiscal):
    cliente = session.query(Cliente).filter(
        Cliente.id_cliente == id_cliente).first()
    if cliente:
        cliente.nombre = nombre
        cliente.apellidos = apellidos
        cliente.id_fiscal = id_fiscal
        session.commit()
        return True
    return False


def eliminar_cliente(id_cliente):
    cliente = session.query(Cliente).filter(
        Cliente.id_cliente == id_cliente).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        return True
    return False


def crear_factura(id_cliente, importe, concepto):
    nueva_factura = Factura(id_cliente=id_cliente,
                            importe=importe, concepto=concepto)
    session.add(nueva_factura)
    session.commit()
    return nueva_factura.id_factura


def obtener_facturas_por_cliente(id_cliente):
    facturas = session.query(Factura).filter(
        Factura.id_cliente == id_cliente).all()
    return facturas


if __name__ == "__main__":
    

    #crear_cliente(3,"diego2", "collado", "3454")
    #crear_cliente(6,"diego3", "collado", "343354")
    #crear_cliente(54,"diego4", "collado", "34334354")
    #crear_factura(3,400, "factura de diego")
    for item in obtener_facturas_por_cliente(3):
        print(str(item))
        print(type(item))