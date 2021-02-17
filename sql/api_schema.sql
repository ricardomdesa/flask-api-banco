BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "pessoas" (
	"idPessoa"	INTEGER NOT NULL,
	"nome"	TEXT NOT NULL,
	"cpf"	TEXT NOT NULL UNIQUE,
	"dataNascimento"	DATE NOT NULL,
	PRIMARY KEY("idPessoa" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "contas" (
	"idConta"	INTEGER NOT NULL,
	"idPessoa"	INTEGER NOT NULL,
	"saldo"	DOUBLE NOT NULL,
	"limiteSaqueDiario"	DOUBLE NOT NULL,
	"flagAtivo"	BOOLEAN NOT NULL,
	"tipoConta"	INTEGER,
	"dataCriacao"	DATE NOT NULL,
	PRIMARY KEY("idConta" AUTOINCREMENT),
	FOREIGN KEY("idPessoa") REFERENCES "Pessoas"("idPessoa")
);
CREATE TABLE IF NOT EXISTS "transacoes" (
	"idTransacao"	INTEGER NOT NULL,
	"idConta"	INTEGER NOT NULL,
	"valor"	DOUBLE NOT NULL,
	"dataTransacao"	DATE NOT NULL,
	PRIMARY KEY("idTransacao" AUTOINCREMENT),
	FOREIGN KEY("idConta") REFERENCES "contas"("idConta")
);
COMMIT;
