from apidb_manager import ApiDb
from datetime import date

Conta = {
    'pessoa': {'idPessoa': 1},
    'saldo': 10,
    'limiteSaqueDiario': 100,
    'flagAtivo': True,
    'tipoConta': 'CC',
    'dataCriacao': date.today()
}
pessoa = {
    'nome': 'Ricardo',
    'cpf': '11122233312',
    'dataNascimento': date.today()
}

transacao = {
    'conta': {'idConta': 1},
    'valor': 100,
    'dataTransacao': date.today()
}

if __name__ == '__main__':
    apiDb = ApiDb()
    apiDb.criar_schema()
    apiDb.inserir_pessoa(pessoa)
    apiDb.close_connection()