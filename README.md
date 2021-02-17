# flask-api-banco
API de operações bancárias simples back-end, usando flask-restful e sqlite3

## instalação:

````
$ git clone
$ cd flask-api-banco
$ python -m venv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt
````

## Rodar projeto
```` 
$ python app.py
````

## api paths:
 
#### Cria uma nova conta
 
- POST: localhost:5000:/api/cria-conta
 
  ````
  Json = {
    "idPessoa": 1,
    "saldo": 300,
    "limiteSaqueDiario": 1000,
    "flagAtivo": 1,
    "tipoConta": "CC",
    "dataCriacao": "16/02/2021"
  }
  ````
  
#### Cria uma nova transacao de saque na conta

- POST: localhost:5000:/api/saque/**idConta**
  ````
  Json = {
    "valor": 3000,
    "dataTransacao": "16/02/2021"
  }
  ````
  
#### Cria uma nova transacao de deposito na conta

- POST: localhost:5000:/api/deposito/**idConta**

 ````
  Json = {
    "valor": 3000,
    "dataTransacao": "16/02/2021"
  }
  ````

#### Ver saldo da conta

- GET: localhost:5000:/api/saldo/**idConta**

#### Ver extrado de transacao da conta

- GET: localhost:5000:/api/extrato/**idConta**

#### Bloqueia a conta passada

- PUT: localhost:5000:/api/bloqueia-conta/**idConta**
