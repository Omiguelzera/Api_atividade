from enum import unique

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base

# Create the engine
engine = create_engine('sqlite:///atividades.db')

# Set up the session
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

# Initialize declarative base
Base = declarative_base()

# Set up the query property
Base.query = db_session.query_property()

# Define models
class Pessoas(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)
    idade = Column(Integer)

    def __repr__(self):
        return f'Pessoa {self.nome}'
    def save(self):
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Atividades(Base):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key=True)
    nome = Column(String(60))
    status = Column(String(10))
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    pessoa = relationship("Pessoas")
    def __repr__(self):
        return f'Atividade {self.nome}'

    def save(self):
        if self.status not in ['Pendente', 'Concluido']:
            raise ValueError("Status must be either 'Pendente' or 'Concluido'")
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Usario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    senha = Column(String(30))

    def __repr__(self):
        return f'Usuario{self.login}'
    def save(self):
        db_session.add(self)
        db_session.commit()
    def delete(self):
        db_session.delete(self)
        db_session.commit()

# Initialize the database
def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()