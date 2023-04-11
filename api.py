import flask
from flask import request, jsonify,render_template
from flask import url_for
import os
from classes import GerenciamentoBanco

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    resultados = {'retorno': 'PaginaInicial'}
    return jsonify(resultados)

@app.route('/consultaUsuario', methods=['GET'])
def consultaUsuario():
  
    cpf = request.json['nuCpf']
    
    GerenciamentoBanco.BancoDados.create()

    cpfExiste = GerenciamentoBanco.BancoDados.consultaCPF(cpf)

    if str(cpfExiste) == "1":
        return "1"
    elif str(cpfExiste) == "0":
        return "0"

@app.route('/loginConsulta', methods=['GET'])
def loginConsulta():
  
    cpfUsuario = request.json['cpfUsuario']
    senhaUsuario = request.json['senhaUsuario']

    loginExiste = GerenciamentoBanco.BancoDados.consultaLogin(cpfUsuario,senhaUsuario)
    

    if str(loginExiste) == "1":
        return "1"
    elif str(loginExiste) == "0":
        return "0"        


@app.route('/abrirConta', methods=['POST'])
def abrirConta():
    NomeCompleto = request.json['NomeCompleto']
    nuCpf = request.json['nuCpf']
    senha = request.json['senha']
    
    ContaCriada = GerenciamentoBanco.BancoDados.insertCadastro(nuCpf,NomeCompleto,senha)

    if str(ContaCriada) == "1":
        return "1"
    elif str(ContaCriada) == "0":
        return "0"

@app.route('/consultasaldo', methods=['GET'])
def consultasaldo():
    nuCpf = request.json['nuCpf']

    saldoconta = GerenciamentoBanco.BancoDados.consultasaldo(nuCpf)

    return str(saldoconta[0])       

@app.route('/transacoesConta', methods=['GET'])
def transacoesConta():
    contaficticia = request.json['contaficticia']
    nuCpf = request.json['nuCpf']
    valorTransferido = request.json['valorTransferido']
    saldoconta = GerenciamentoBanco.BancoDados.consultasaldo(nuCpf)

    if float(str(saldoconta[0])) < float(valorTransferido):        
        return "Saldo insuficiente!"
    elif 'erro' in str(saldoconta[0]):
        return "Erro ao realizar transação."
    else:
        Transacao = GerenciamentoBanco.BancoDados.insertTransacoes(nuCpf,str(saldoconta[0]),float(valorTransferido),contaficticia)
        if str(Transacao) == "1":
            return "1"
        else:
            return "Erro ao realizar transação."
            

@app.route('/depositarConta', methods=['POST'])
def depositarConta():
    valorDeposito = request.json['valorDeposito']
    nuCpf = request.json['nuCpf']
    
    deposito = GerenciamentoBanco.BancoDados.insertDeposito(nuCpf,valorDeposito)

    if str(deposito) == "1":
        return "1"
    elif str(deposito) == "0":
        return "0"    

@app.route('/saqueconta', methods=['POST'])
def pode_sacar():
    valorSaque = request.json['valorSaque']
    nuCpf = request.json['nuCpf']

    saque = GerenciamentoBanco.BancoDados.insertSaque(nuCpf,valorSaque)

    if str(saque) == "1":
        return "1"
    elif str(saque) == "0":
        return "0"
    else:
        return str(saque)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))