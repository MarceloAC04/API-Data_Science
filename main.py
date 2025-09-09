# pip install flask
from flask import Flask, request, make_response, jsonify

# Importação da base de dados
from bd import Carros


# Esse módulo do Flask vai subir a nossa API localmente
# Vamos instanciar o modulo Flask na nossa variavel app
app = Flask('carros')

# METODO 1 - Visualização de DADOS (GET)
# 1 - O que esse metodo vai fazer ?
# 2- Onde ele vai fazer ?

@app.route('/carrinho', methods=['GET'])
def get_carros():
    return Carros


# METODO 1.1 - Visualização de DADOS POR ID (GET)
@app.route('/carrinho/<int:id>', methods=['GET'])
def get_carros_id(id):
    for car in Carros:
        if car.get('id') == id:
            return jsonify(car)
        

# METODO 2 - CRIAR NOVOS REGISTROS (POST)
# VERIFICAR os dados que estão passados na requisição e armazenar na nossa base.
@app.route('/carrinho', methods=['POST'])
def criar_carro():
    car = request.json
    Carros.append(car)
    return make_response(
        jsonify(
            mensagem = 'Carro cadastrado com sucesso!!',
            carrinho = car
        )
    )

# METODO 3 - DELETAR REGISTROS (DELETE)
@app.route('/carrinho/<int:id>', methods=['DELETE'])
def excluir_carro(id):
    for indice, carro in enumerate(Carros):
        if carro.get('id') == id:
            del Carros[indice]
            return jsonify(
                {
                    'mensagem': "Carro excluído"
                }
            )
            
# METODO 4 - EDITAR OS REGISTROS (PUT)
@app.route('/carrinho/<int:id>', methods=['PUT'])
def editar_carro(id):
    alter_carro = request.get_json()
    for indice, carro in enumerate(Carros):
        if carro.get('id') == id:
            Carros[indice].update(alter_carro)
            return jsonify(Carros[indice])
            
app.run(port=5000, host='localhost', debug=True)