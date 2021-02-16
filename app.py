from flask import Flask, request
from flask_restful import Api, Resource
from apidb_manager import ApiDb
from datetime import datetime

app = Flask(__name__)
api = Api(app)
apidb = ApiDb()


class CriaConta(Resource):
    def post(self):
        dados = request.json
        pessoa = apidb.localizar_pessoa(dados['idPessoa'])
        if pessoa:
            conta = {
                'pessoa': {'idPessoa': dados['idPessoa']},
                'saldo': dados['saldo'],
                'limiteSaqueDiario': dados['limiteSaqueDiario'],
                'flagAtivo': dados['flagAtivo'],
                'tipoConta': dados['tipoConta'],
                'dataCriacao': datetime.strptime(dados['dataCriacao'], '%d/%m/%Y').date()
            }
            apidb.inserir_conta(conta)
            resp = {'status': 'sucesso', 'mensagem': 'Conta criada com sucesso'}
        return resp


class AddSaqueTransacao(Resource):
    def post(self, idConta):
        dados = request.json
        conta = apidb.localizar_conta(idConta)
        print(conta)
        if conta:
            transacao = {
                'idConta': idConta,
                'dataTransacao': datetime.strptime(dados['dataTransacao'], '%d/%m/%Y').date(),
                'valor': dados['valor']
            }
            print('saque')
            apidb.inserir_transacao(transacao)
            resp = {'sts': 'sucesso criar transacao'}
        return resp


class AddDepositoTransacao(Resource):
    def post(self, idConta):
        dados = request.json
        conta = apidb.localizar_conta(idConta)
        print(conta)
        if conta:
            transacao = {
                'conta': idConta,
                'dataTransacao': datetime.strptime(dados['dataTransacao'], '%d/%m/%Y').date(),
                'valor': dados['valor']
            }
            print('deposito')
            apidb.inserir_transacao(transacao)
            resp = {'sts': 'sucesso criar transacao'}
        return resp


class ListaTransacoes(Resource):
    def get(self, idConta):
        try:
            trasacoes = apidb.get_transacoes_por_conta(idConta)
            print(trasacoes)
            resp = [{'idConta': i[1], 'valor': i[2], 'dataTransacao': i[3]} for i in trasacoes]
        except Exception:
            resp = {'sts': 'erro'}
            raise Exception
        return resp


class SaldoConta(Resource):
    def get(self, idConta):
        try:
            conta = apidb.localizar_conta(idConta)
            print(conta)
            resp = {'idConta': idConta, 'saldo': conta[2]}
        except Exception:
            resp = {'sts': 'erro'}
            raise Exception
        return resp


class BloqueiaConta(Resource):
    def get(self, idConta):
        try:
            conta = apidb.localizar_conta(idConta)
            print(conta)
            resp = {}
        except Exception:
            resp = {'sts': 'erro'}
            raise Exception
        return resp


api.add_resource(CriaConta, '/api/cria-conta')
api.add_resource(AddSaqueTransacao, '/api/saque/<int:idConta>')
api.add_resource(AddDepositoTransacao, '/api/deposito/<int:idConta>')
api.add_resource(ListaTransacoes, '/api/extrato/<int:idConta>')
api.add_resource(SaldoConta, '/api/saldo/<int:idConta>')
api.add_resource(BloqueiaConta, '/api/bloqueia-conta/<int:idConta>')


if __name__ == '__main__':
    apidb.criar_schema()
    app.run(debug=True)