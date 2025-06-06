from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///oficina.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Clientes(Base):
    __tablename__ = 'TAB_CLIENTES'
    nome = Column(String, nullable=False)
    id_cliente = Column(Integer, primary_key=True)
    cpf = Column(Integer, nullable=False, unique=True)
    telefone = Column(String, nullable=False, unique=True)
    endereco = Column(String, nullable=False)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_cliente(self):
        dados_cliente = {
            "Nome": self.nome,
            "ID Cliente": self.id_cliente,
            "CPF": self.cpf,
            "telefone": self.telefone,
            "Endereco": self.endereco


        }

        return dados_cliente


class Veiculos(Base):
    __tablename__ = 'TAB_VEICULOS'
    marca = Column(String,nullable=False)
    id_veiculo = Column(Integer, primary_key=True)
    modelo = Column(String, nullable=False)
    placa = Column(String, nullable=False, unique=True)
    ano_fabri = Column(Integer, nullable=False)
    id_cliente = Column(Integer, ForeignKey('TAB_CLIENTES.id_cliente'), nullable=False)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_veiculo(self):
        dados_veiculos = {
            "Marca": self.marca,
            "ID Veiculo": self.id_veiculo,
            "Modelo": self.modelo,
            "placa": self.placa,
            "ano_fabri ": self.ano_fabri,
            "id_cliente": self.id_cliente


        }

        return dados_veiculos


class Ordens(Base):
    __tablename__ = 'TAB_ORDENS'
    veiculo = Column(String, nullable=False)
    id_veiculo = Column(Integer, ForeignKey('TAB_VEICULOS.id_veiculo'), nullable=False)
    id_orden = Column(Integer, primary_key=True)
    data_abertura = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    status = Column(String, nullable=False)
    valor = Column(Float, nullable=False)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_orden(self):
        dados_ordem = {
            "veiculo": self.veiculo,
            "id_veiculo": self.id_veiculo,
            "data_abertura": self.data_abertura,
            "Descricao": self.descricao,
            "status": self.status,
            "valor": self.valor,
            "ID Serviço": self.id_orden
        }

        return dados_ordem


def init_db():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()