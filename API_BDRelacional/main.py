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

# ---------------------------------------------------------------------
# METODO 2 - GET por Id
@app.route('/carros/<id_carro>', methods=['GET'])
def seleciona_carro_id(id_carro):
    carro_selecionado = Carros.query.filter_by(id_carro=id_carro).first()
    carro_json = carro_selecionado.to_json()
    return gera_resposta(200, "Carro por Id", carro_json)

# ---------------------------------------------------------------------
# METODO 3 - POST
@app.route('/carros', methods=['POST'])
def inserir_carro():
    requisicao = request.get_json()
    try:
        carro = Carros(
            id_carro= requisicao['id_carro'],
            marca= requisicao['marca'],
            modelo = requisicao['modelo'],
            ano= requisicao['ano'],
            valor= requisicao['valor'],
            cor= requisicao['cor'],
            nuemro_vendas= requisicao['numero_vendas'],
        )
        
        # Adicionar ao banco
        mybd.session.add(carro)
        mybd.session.commit()
        
        return gera_resposta(201, "Novo carro inserido com sucesso", carro.to_json())
    except Exception as e:
     print('Erro', e)
     return  gera_resposta(400, {}, "Erro ao Cadastrar!")
 
# ---------------------------------------------------------------------
# METODO 4 - DELETE
@app.route('/carros/<id_carro>', methods=['DELETE'])
def deletar_carro(id_carro):
    carro = Carros.query.filter_by(id_carro=id_carro).first()
    
    try:
        mybd.session.delete(carro)
        mybd.session.commit()
        return gera_resposta(200, 'Carro exluido com sucesso!', carro.to_json())
    except Exception as e:
        print('Erro', e)
        
        return  gera_resposta(400, {}, "Erro ao Excluir!")

# ---------------------------------------------------------------------
# METODO 5 - PUT
@app.route('/carros/<id_carro>', methods=['PUT'])
def atualizar_carro(id_carro):
    requisicao = request.get_json()
    try:
        carro_atualizado = Carros(
            id_carro= id_carro,
            marca= requisicao['marca'],
            modelo = requisicao['modelo'],  
            ano= requisicao['ano'],
            valor= requisicao['valor'],
            cor= requisicao['cor'],
            nuemro_vendas= requisicao['numero_vendas'],
        )
        
        carro_antigo = Carros.query.filter_by(id_carro=id_carro).first()
        
        carro_antigo.marca = carro_atualizado.marca if carro_atualizado.marca != "" else carro_antigo.marca
        carro_antigo.modelo = carro_atualizado.modelo if carro_atualizado.modelo != "" else carro_antigo.modelo
        carro_antigo.ano = carro_atualizado.ano if carro_atualizado.ano != "" else carro_antigo.ano
        carro_antigo.valor  = carro_atualizado.valor if carro_atualizado.valor != "" else carro_antigo.valor
        carro_antigo.cor = carro_atualizado.cor if carro_atualizado.cor != "" else carro_antigo.valor
        carro_antigo.nuemro_vendas = carro_atualizado.nuemro_vendas if carro_atualizado.nuemro_vendas != "" else carro_antigo.nuemro_vendas
        
        
        # Adicionar ao banco
        mybd.session.commit()
        
        return gera_resposta(201, "Carro atualizado com sucesso", carro_antigo.to_json())
    except Exception as e:
     print('Erro', e)
     return  gera_resposta(400, {}, "Erro ao Cadastrar!")


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