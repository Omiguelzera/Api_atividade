from http.client import responses
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usario
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#USUARIO = {
#    'Miguel' : '123',
#    'Lucas' : '123'
#}
#
#@auth.verify_password
#def verification(login, senha):
#    if not(login, senha):
#        return False
#    return USUARIO.get(login)== senha

@auth.verify_password
def verification(login, senha):
    if not(login, senha):
        return False
    return Usario.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response={
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados=request.json
        if 'nome' in dados :
            pessoa.nome = dados['nome']
        if 'idade' in dados :
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome' : pessoa.nome,
            'idade': pessoa.idade

        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).fisrt()
        pessoa.delete()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        return {'status' : 'sucesso', 'mensagem': mensagem}

class ListaPessoas(Resource):
    def get(self):
        pessoa = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade' : i.idade} for i in pessoa]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id' : pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class ListaAtividade(Resource):
    def get(self):
        atividade = Atividades.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'status': i.status,  'pessoa': i.pessoa.nome } for i in atividade]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()

        status = dados.get('status', 'Pendente')
        if status not in ['Pendente', 'Concluido']:
            return {'error': 'Invalid status. Must be "Pendente" or "Concluido".'}, 400

        atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=status)
        atividade.save()
        response = {
            'pessoa' : atividade.pessoa.nome,
            'nome' : atividade.nome,
            'status': atividade.status,
            'id' : atividade.id
        }
        return response

class Atividade(Resource):
    def delete(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        atividade.delete()
        mensagem = 'Atividade {} exlcuida com sucesso' .format(atividade.id)
        return {'status': 'sucesso', 'Mensagem': mensagem}

    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        try:
            response = {
                'id' : atividade.id,
                'status' : atividade.status
            }
        except AttributeError:
            response = {
                'status' : 'erro',
                'mensagem' : 'atividade nao encontrada'
            }

        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividade, '/atividade/')
api.add_resource(Atividade, '/atividade/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
