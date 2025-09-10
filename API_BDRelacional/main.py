# SQL_ALCHEMY
# PERMITE a conexão da API COM o banco de dados
# FLASK - Permite a criação da API com Python
# Response e Request -> Requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json 

app = Flask('carros')


# Rasrear as modificações realizadas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Configuração de conexão com o banco
# %40 -> faz o papel de @
# 1 - Usuario (root) 2 - Senha(Senai540134) 3 - localhost (127.0.0.1) 4 - nome do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_carro'

mybd = SQLAlchemy(app)

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class Carros(mybd.Model):
    __tablename__ = 'tb_carro'
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(255))
    modelo = mybd.Column(mybd.String(255))
    ano = mybd.Column(mybd.String(255))
    cor = mybd.Column(mybd.String(255))
    valor = mybd.Column(mybd.String(255))
    nuemro_vendas = mybd.Column(mybd.String(255))

# Esse metodo to_json vai ser usado para converter o objeto json
    def to_json(self):
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "cor": self.cor,
            "valor": float(self.valor),
            "numero_vendas": self.nuemro_vendas
        }
        
# ---------------------------------------------------------------------

# METODO 1 - GET
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    carro_selecionado = Carros.query.all()
    # Executa uma consulta no banco de dados ( SELECT * FROM tb_carro)
    carro_json = [carro.to_json()
                  for carro in carro_selecionado]
    return gera_resposta(200, "Lista de carros", carro_json)




# ------------------
# RESPOSTA PADRÄO
    # - status (200, 201)
    # nome do conteudo
    # conteudo
    # mensagem (opcional)
def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
        
    if (mensagem):
        body['mensagem'] = mensagem
        
    return Response(json.dumps(body), status=status, mimetype='applicatiob/json')
# Dumps - Converte o dicionario criado (body) em Json (json.dumps)




app.run(port=5000, host='localhost', debug=True)