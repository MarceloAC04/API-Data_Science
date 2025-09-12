from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json 

app = Flask("clientes")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_veterinaria'

mybd = SQLAlchemy(app)

class Clientes(mybd.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key= True)
    nome = mybd.Column(mybd.String(255))
    endereco = mybd.Column(mybd.String(255))
    telefone = mybd.Column(mybd.String(255))
    
    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }


# Listar Clientes
@app.route('/ListaClientes', methods=['GET'])
def seleciona_clientes():
    try:
        
        cliente_selecionado = Clientes.query.all()
    
        clientes_json = [cliente.to_json()
        for cliente in cliente_selecionado
        ]
    
        return gera_resposta(200, 'Lista de Clientes', clientes_json)
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao Cadastrar!", {})
    

# Buscar cliente por Id
@app.route('/BuscarCliente/<id_cliente>', methods=['GET'])
def seleciona_cliente_id(id_cliente):
    try: 
        cliente_selecionado = Clientes.query.filter_by(id_cliente=id_cliente).first()
    
        return gera_resposta(200, 'Cliente buscado', cliente_selecionado.to_json())
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao buscar !", {})
    
# Buscar cliente por nome
@app.route('/BuscarClientePorNome/<nome>', methods=['GET'])
def seleciona_cliente_nome(nome):
    try: 
        cliente_selecionado = Clientes.query.filter_by(nome=nome)
        
        clientes_nome = [cliente.to_json()
            for cliente in cliente_selecionado
        ]
    
        return gera_resposta(200, 'Cliente buscado', clientes_nome)
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao buscar !", {})


# Inserir Cliente
@app.route('/clientesInsert', methods=['POST'])
def inserir_clientes():
    try:
        requisicao = request.get_json()
        
        cliente = Clientes(
          id_cliente = requisicao['id_cliente'],
         nome = requisicao['nome'],
           endereco = requisicao['endereco'],
        telefone = requisicao['telefone']
        )
        
        mybd.session.add(cliente)
        mybd.session.commit()
        
        return gera_resposta(201, 'Cliente cadastrado com sucesso!', cliente.to_json())
    except Exception as  e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao Cadastrar!", {})
    
    
# Deletar Clientes
@app.route('/clienteDelete/<id_cliente>', methods=['DELETE'])
def deletar_cliente(id_cliente):
    try:
        cliente_buscado = Clientes.query.filter_by(id_cliente=id_cliente).first()
    
        mybd.session.delete(cliente_buscado)
        mybd.session.commit()
        
        return gera_resposta(200, 'Cliente deletado com sucesso!', cliente_buscado.to_json())
    except Exception as e:
        print('Error:', e)
        return gera_resposta(400, "Erro ao Cadastrar!", {})


# Atualizar Clientes
@app.route('/clienteUpdate/<id_cliente>', methods=['PUT'])
def atualizar_cliente(id_cliente):
    try:
        requisicao = request.get_json()
        
        cliente_atualizado = Clientes.query.filter_by(id_cliente=id_cliente).first()
        
        cliente_atualizado.nome = requisicao['nome'] if requisicao['nome'] != '' else cliente_atualizado.nome
        cliente_atualizado.endereco = requisicao['endereco'] if requisicao['endereco'] != '' else cliente_atualizado.endereco
        cliente_atualizado.telefone = requisicao['telefone'] if requisicao['telefone'] != '' else cliente_atualizado.telefone
        
        mybd.session.commit()
        
        return gera_resposta(201, 'Cliente atualizaddo com sucesso!', cliente_atualizado.to_json())
    except Exception as e:
          print('Error:', e)
          return gera_resposta(400, "Erro ao Cadastrar!", {})


def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
        
    if (mensagem):
        body['mensagem'] = mensagem
        
    return Response(json.dumps(body), status=status, mimetype='applicatiob/json')



app.run(port=5000, host='localhost', debug=True)