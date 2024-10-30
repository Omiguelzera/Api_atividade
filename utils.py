from sqlalchemy.util.typing import is_newtype

from app import USUARIO
from models import Pessoas, db_session, Usario

def insere_pessoas():
    pessoa = Pessoas(nome='Lucas', idade=26)
    print(pessoa)
    pessoa.save()

def consulta():
    pessoa = Pessoas.query.all()
    print(pessoa)

def altera():
    pessoa = Pessoas.query.filter_by(nome="Miguel").first()
    pessoa.idade = 30
    pessoa.save()

def delete():
    pessoa = Pessoas.query.filter_by(nome='Lucas').first()
    pessoa.delete()

def insere_usuario(login, senha):
    usuario = Usario(login=login, senha=senha)
    usuario.save()

def consulta_usuario():
    usuario = Usario.query.all()
    print(usuario)

if __name__ == '__main__':
    insere_usuario('Nezuko', '345')
    consulta_usuario()
    #insere_pessoas()
    #altera()
    #delete()
    #consulta()