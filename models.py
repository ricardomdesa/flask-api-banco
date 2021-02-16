import sqlite3

conn = sqlite3.connect('conta.db')


def db_init():
    global conn
    # definindo um cursor
    cursor = conn.cursor()
    criaTabelas(cursor)


# criando a tabela (schema)
def criaTabelas(cursor):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
                idPessoa INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                dataNascimento DATE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
                idConta INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                idPessoa INTEGER NOT NULL,            
                saldo DOUBLE NOT NULL,
                limiteSaqueDiario DOUBLE NOT NULL,
                flagAtivo BOOLEAN NOT NULL,
                tipoConta INTEGER,
                dataCriacao DATE NOT NULL,
                FOREIGN KEY (idPessoa) REFERENCES Pessoas(idPessoa)
        );""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
                idTransacao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                idConta INTEGER NOT NULL,
                valor DOUBLE NOT NULL,
                dataTransacao DATE NOT NULL,
                FOREIGN KEY (idConta) REFERENCES contas(idConta)
        );
        """)


def inserePessoa(pessoa):
    global conn
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pessoas (nome, cpf, dataNascimento)
    VALUES (?,?,?);
    """, (pessoa['nome'], pessoa['cpf'], pessoa['dataNascimento']))
    conn.commit()

    print('Dados inseridos com sucesso.')

def insereConta(conta):
    global conn
    cursor = conn.cursor()

    # inserindo dados na tabela
    cursor.execute("""
    INSERT INTO contas (idPessoa, saldo, limiteSaqueDiario, flagAtivo, tipoConta, dataCriacao)
    VALUES (?,?,?,?,?,?);
    """, (conta['pessoa']['idPessoa'], conta['saldo'], conta['limiteSaqueDiario'], conta['flagAtivo'], conta['tipoConta'], conta['dataCriacao']))

    conn.commit()

    print('Dados inseridos com sucesso.')

    # conn.close()


def insereTransacao(trans):
    global conn
    cursor = conn.cursor()

    # inserindo dados na tabela
    cursor.execute("""
    INSERT INTO transacoes (idConta, valor, dataTransacao)
    VALUES (?,?,?);
    """, (trans['conta']['idConta'], trans['valor'], trans['dataTransacao']))

    conn.commit()

    print('Dados inseridos com sucesso.')

def getContas():
    global conn
    cursor = conn.cursor()
    dados = []
    cursor.execute("""
        SELECT * FROM contas;
    """)
    for i in cursor.fetchall():
        dados.append(i)
    return dados


def getPessoas():
    global conn
    cursor = conn.cursor()
    dados = []
    cursor.execute("""
        SELECT * FROM pessoas;
    """)
    for i in cursor.fetchall():
        dados.append(i)
    return dados


def getTransacoes():
    global conn
    cursor = conn.cursor()
    dados = []
    cursor.execute("""
        SELECT * FROM transacoes;
    """)
    for i in cursor.fetchall():
        dados.append(i)
    return dados