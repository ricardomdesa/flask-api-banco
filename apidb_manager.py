from connect_db import Connect
import sqlite3
from datetime import datetime


class ApiDb(object):

    tb_name = 'contas'

    def __init__(self):
        self.db = Connect('apidb.db')

    def close_connection(self):
        self.db.close_db()

    def criar_schema(self, schema_name='sql/api_schema.sql'):
        print("Criando tabela %s ..." % self.tb_name)

        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error:
            print("Aviso: A tabela %s já existe." % self.tb_name)
            return False

        print("Tabela %s criada com sucesso." % self.tb_name)

    def inserir_pessoa(self, pessoa):
        self.nome = pessoa['nome']
        self.cpf = pessoa['cpf']
        self.dataNasc = pessoa['dataNascimento']
        try:
            self.db.cursor.execute("""
            INSERT INTO pessoas (nome, cpf, dataNascimento)
            VALUES (?,?,?);
            """, (self.nome, self.cpf, self.dataNasc))

            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O cpf deve ser único.")
            return False

    def inserir_conta(self, conta):
        self.idPessoa = conta['pessoa']['idPessoa']
        self.saldo = conta['saldo']
        self.limite = conta['limiteSaqueDiario']
        self.flag = conta['flagAtivo']
        self.tipo = conta['tipoConta']
        self.dataCriacao = conta['dataCriacao']

        try:
            self.db.cursor.execute("""
                    INSERT INTO contas (idPessoa, saldo, limiteSaqueDiario, flagAtivo, tipoConta, dataCriacao)
                    VALUES (?,?,?,?,?,?);
                    """, (self.idPessoa, self.saldo, self.limite, self.flag, self.tipo, self.dataCriacao))

            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O registro deve ser único.")
            return False

    def inserir_transacao(self, transacao):
        self.idConta = transacao['idConta']
        self.valor = transacao['valor']
        self.dataTransacao = transacao['dataTransacao']

        try:
            self.db.cursor.execute("""
                  INSERT INTO transacoes (idConta, valor, dataTransacao)
                  VALUES (?,?,?);
                  """, (self.idConta, self.valor, self.dataTransacao))

            self.db.commit_db()
            print("Um registro inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O registro deve ser único.")
            return False

    # localizar uma conta
    def localizar_conta(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM contas WHERE idConta = ?', (id,))
        obj = r.fetchone()
        if obj:
            return {'idConta': obj[0], 'idPessoa': obj[1], 'saldo': obj[2], 'limiteSaqueDiario': obj[3],
                    'flagAtivo': obj[4], 'tipoConta': obj[5], 'dataCriacao': obj[6], 'status': 'sucesso'}
        else:
            return {'status': 'erro'}

    def localizar_pessoa(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM pessoas WHERE idPessoa = ?', (id,))
        obj = r.fetchone()
        if obj:
            return {'idPessoa': obj[0], 'nome': obj[1], 'cpf': obj[2], 'dataNascimento': obj[3]}
        else:
            return {}

    def localizar_transacao(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM transacoes WHERE idTransacao = ?', (id,))
        obj = r.fetchone()
        if obj:
            return {'idTransacao': obj[0], 'idConta': obj[1], 'valor': obj[2], 'dataTransacao': obj[3]}
        else:
            return {}

    # Atualizar conta
    def atualizar_conta(self, conta):
        try:
            c = self.localizar_conta(conta['idConta'])
            if c:
                self.saldo = conta['saldo']
                self.flag = conta['flagAtivo']
                self.id = conta['idConta']
                self.db.cursor.execute("""
                    UPDATE contas
                    SET saldo = ?, flagAtivo = ?
                    WHERE idConta = ?
                    """, (self.saldo, self.flag, self.id,))
                # gravando no bd
                self.db.commit_db()
                print("Saldo atualizado com sucesso.")
            else:
                print('Não existe conta com o id informado.')
        except Exception:
            raise Exception


    #   Deletar conta
    def deletar_conta(self, id):
        try:
            c = self.localizar_conta(id)
            # verificando se existe conta com o ID passado, caso exista
            if c:
                self.db.cursor.execute("""
                DELETE FROM contas WHERE id = ?
                """, (id,))
                # gravando no bd
                self.db.commit_db()
                print("Registro %d excluído com sucesso." % id)
            else:
                print('Não existe cliente com o código informado.')
        except Exception:
            raise Exception

    def get_transacoes_por_conta(self, id):
        sql = 'SELECT * FROM transacoes WHERE idConta = ?'
        r = self.db.cursor.execute(sql, (id,))
        objs = r.fetchall()
        if objs:
            return [{'idTransacao': o[0], 'idConta': o[1], 'valor': o[2], 'dataTransacao': o[3]} for o in objs]
        else:
            return []


if __name__ == '__main__':
    apidb = ApiDb()
    apidb.criar_schema()
    p = {
        'nome': 'Ricardo',
        'cpf': '11122233312',
        'dataNascimento': datetime.strptime('01/02/2021', '%d/%m/%Y').date()
    }
    apidb.inserir_pessoa(p)
    apidb.close_connection()