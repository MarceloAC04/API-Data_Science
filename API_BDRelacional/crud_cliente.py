from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
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
    
    pets = relationship('Pets', back_populates='cliente')
    
    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }
        

class Pets(mybd.Model):
    __tablename__ = 'tb_pets'
    id_pet = mybd.Column(mybd.Integer, primary_key= True, autoincrement = True)
    nome = mybd.Column(mybd.String(255))
    tipo = mybd.Column(mybd.String(255))
    raca = mybd.Column(mybd.String(255))
    data_nascimento = mybd.Column(mybd.Date)
    id_cliente= mybd.Column(mybd.Integer, mybd.ForeignKey('tb_clientes.id_cliente'), nullable=False)
    idade = mybd.Column(mybd.Integer)
    
    cliente = relationship('Clientes', back_populates='pets')
    
    def to_json(self):
        dados_cliente = None
        if self.cliente:
            dados_cliente = {
                "id_cliente": self.cliente.id_cliente,
                "nome": self.cliente.nome,
                "endereco": self.cliente.endereco,
                "telefone": self.cliente.telefone
            }
        return {
            "id_pet": self.id_pet,
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "data_nascimento": str(self.data_nascimento),
            "id_cliente": self.id_cliente,
            "idade": self.idade,
            "cliente": dados_cliente
            }
        
#-------------------------------------------------------------------------------
# GET - CLIENTE
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
    

# GET - Pets
# Listar Pets
@app.route('/ListaPets', methods=['GET'])
def seleciona_pets():
    try:
        
        pet_selecionado = Pets.query.all()
    
        pets_json = [pet.to_json()
        for pet in pet_selecionado]
        
        return gera_resposta(200, 'Lista de pets', pets_json)
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao Buscar!", {})

# Listar Pets por Id
@app.route('/BuscarPetPorId/<id_pet>', methods=['GET'])
def buscar_pet_id(id_pet):
    try:
        
        pet_selecionado = Pets.query.filter_by(id_pet=id_pet).first()
        
        return gera_resposta(200, 'Lista de pets', pet_selecionado.to_json())
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao Buscar!", {})

    
# -----------------------------------------------------------------------------------------------------
# POST - CLIENTE
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

# POST - PET
@app.route('/petsInsert', methods=['POST'])
def inserir_pets():
    try:
        requisicao = request.get_json()
        
        pet = Pets(
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento= requisicao['data_nascimento'],
            id_cliente = requisicao['id_cliente'],
            idade = requisicao['idade']
        )
        
        mybd.session.add(pet)
        mybd.session.commit()
        
        return gera_resposta(201, 'Pet cadastrado com sucesso!', pet.to_json())
    except Exception as  e:
        print("Erro", e)
        return gera_resposta(400, "Erro ao Cadastrar!", {})
    

# -----------------------------------------------------------------------------------------------------
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
    
    
# Deletar Pets
@app.route('/petDelete/<id_pet>', methods=['DELETE'])
def deletar_pet(id_pet):
    try:
        pet_buscado = Pets.query.filter_by(id_pet=id_pet).first()
    
        mybd.session.delete(pet_buscado)
        mybd.session.commit()
        
        return gera_resposta(200, 'Pet deletado com sucesso!', pet_buscado.to_json())
    except Exception as e:
        print('Error:', e)
        return gera_resposta(400, "Erro ao Cadastrar!", {})


# -----------------------------------------------------------------------------------------------------
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
      
# Atualizar Pets
@app.route('/petUpdate/<id_pet>', methods=['PUT'])
def atualizar_pet(id_pet):
    try:
        requisicao = request.get_json()
        
        pet_atualizado = Pets.query.filter_by(id_pet=id_pet).first()
        pet_atualizado.nome = requisicao['nome'] if requisicao['nome'] != '' else pet_atualizado.nome
        pet_atualizado.tipo = requisicao['tipo'] if requisicao['tipo'] != '' else pet_atualizado.tipo
        pet_atualizado.raca = requisicao['raca'] if requisicao['raca'] != '' else pet_atualizado.raca
        pet_atualizado.data_nascimento = requisicao['data_nascimento'] if requisicao['data_nascimento'] != '' else pet_atualizado.data_nascimento
        pet_atualizado.id_cliente = requisicao['id_cliente'] if requisicao['id_cliente'] != '' else pet_atualizado.id_cliente
        pet_atualizado.idade = requisicao['idade'] if requisicao['idade'] != '' else pet_atualizado.idade
        
        mybd.session.commit()
        
        return gera_resposta(201, 'Pet atualizaddo com sucesso!', pet_atualizado.to_json())
    except Exception as e:
          print('Error:', e)
          return gera_resposta(400, "Erro ao Atualizar !", {})




def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
        
    if (mensagem):
        body['mensagem'] = mensagem
        
    return Response(json.dumps(body), status=status, mimetype='applicatiob/json')



app.run(port=5000, host='localhost', debug=True)