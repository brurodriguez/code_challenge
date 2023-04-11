import requests

cpfUsuario = input('Por favor, insira seu CPF: ')

cadastro = 0
while cadastro == 0:
    url = 'http://localhost:5000/consultaUsuario'

    consultaCpf = requests.get(url, json={"nuCpf": str(cpfUsuario)})

    if consultaCpf.text == "1":
        print("Seu CPF foi encontrado em nossa base!")
        senhaUsuario = input('Qual sua Senha? ')
        urlLogin = 'http://localhost:5000/loginConsulta'
        loginConsulta = requests.get(urlLogin, json={"cpfUsuario": str(cpfUsuario),"senhaUsuario": str(senhaUsuario)})

        if(loginConsulta.text == "1"):
            print('Login feito com sucesso!', '\n')
            cadastro = 1
            pass
        else:
            print("Sua senha está incorreta! Por favor tente novamente.", '\n')
            cadastro = 0
            pass
    elif consultaCpf.text == "0":
        def SimNao():
            criarConta = input('Não há nenhuma conta no seu CPF, gostaria de criar uma nova? Digite SIM ou NAO: ')
            return criarConta


        criarConta = SimNao()
        i = 0
        while i < 1:
            if (criarConta).upper() != 'SIM' and (criarConta).upper() != 'NAO':
                print('Por favor, insira um valor válido!')
                criarConta = SimNao()
            else:
                i += 1
                if (criarConta).upper() == 'SIM':
                    nomeUsuario = input('Qual seu Nome Completo? ')
                    senhaUsuario = input('Digite a sua senha: ')
                    senhaConfirmacao = input('Repita a sua senha: ')
                    if senhaUsuario == senhaConfirmacao:
                        urlCadastro = 'http://localhost:5000/abrirConta'
                        cadastroUsuario = requests.post(urlCadastro, json={"NomeCompleto":str(nomeUsuario),"nuCpf": str(cpfUsuario),"senha":str(senhaUsuario)})

                        if(cadastroUsuario.text == "1"):
                            print('Usuário e Senha cadastrado!')
                            cadastro = 0
                            pass
                        else:
                            print("Ocorreu um erro! Por favor tente novamente.")
                            break
                    else:
                        print("Sua confirmação de senha, está incorreta! Por favor, insira novamente.", '\n')
                        n = 0
                        while n == 0:
                            senhaUsuario = input('Insira novamente a senha: ')
                            senhaConfirmacao = input('Repita a sua senha: ')

                            if senhaUsuario == senhaConfirmacao:
                                urlCadastro = 'http://localhost:5000/abrirConta'
                                cadastroUsuario = requests.get(urlCadastro, json={"NomeCompleto":str(nomeUsuario),"nuCpf": str(cpfUsuario),"senha":str(senhaUsuario)})
                                if(cadastroUsuario.text == "1"):
                                    print('Usuário e Senha cadastrado!', '\n')
                                    cadastro = 0
                                    pass
                                else:
                                    print("Ocorreu um erro! Por favor tente novamente.", '\n')
                                    break
                                n = 1
                                break
                            else:
                                print("Não foi possível prosseguir!")
                                n = 0
                                pass
                elif (criarConta).upper() == 'NAO':
                    print('Você optou por não abrir uma conta.')
                    exit(1)

while cadastro == 1:
    print("Qual operação deseja realizar? ")
    print("Apenas números são reconhecidos, escolha uma das opções abaixo: ")
    escolhaOperacao = input('1-TRANSAÇÃO, 2-SALDO, 3-DEPOSITAR, 4-SACAR, 5-SAIR: ')

    if escolhaOperacao == "1":
        print("Você escolheu a opção Transação. ", '\n')
        contaficticia = input('Insira a conta para quem enviará o depósito: ')
        valorTransferido = input('Qual será o valor transferido?  R$')
        if (float(valorTransferido) <= 2000):
            urlTransacoesConta = 'http://localhost:5000/transacoesConta'
            Transacao = requests.get(urlTransacoesConta, json={"contaficticia":str(contaficticia),"nuCpf": str(cpfUsuario),"valorTransferido":str(valorTransferido)})
            if Transacao.text == "1":
                print("Transferência realizada com sucesso!")
                cadastro = 1
                pass
            else:
                print(Transacao.text)
                cadastro = 1
                pass 
        else:
            print("O Valor R${} está acima do permitido".format(float(valorTransferido)))
            cadastro = 1
            pass

    elif escolhaOperacao == "2":    
        print("Você escolheu a opção Saldo. ", '\n')
        urlConsultaSaldo = 'http://localhost:5000/consultasaldo'
        saldo = requests.get(urlConsultaSaldo, json=dict(nuCpf=str(cpfUsuario)))
        print(f"Seu saldo atual é de R${saldo.text} ", '\n')


    elif escolhaOperacao == "3":   
        print("Você escolheu a opção Depósito. ", '\n')
        valorDeposito = input('Quanto você deseja depositar?  R$')
        urlDepositarConta = 'http://localhost:5000/depositarConta'
        deposito = requests.post(urlDepositarConta, json={"valorDeposito":str(valorDeposito),"nuCpf": str(cpfUsuario)})
        if(deposito.text == "1"):
            print('Seu deposito foi feito com sucesso!', '\n')
            cadastro = 1
            pass
        else:
            print("Ocorreu um erro! Por favor tente novamente.", '\n')
            cadastro = 1
            pass

    elif escolhaOperacao == "4":
        print("Você escolheu a opção Saque. ", '\n')
        valorSaque = input('Qual valor para saque? R$')
        urlPodeSacar = 'http://localhost:5000/saqueconta'
        saque = requests.post(urlPodeSacar, json={"valorSaque":str(valorSaque),"nuCpf": str(cpfUsuario)})
        if(saque.text == "1"):
            print('Saque feito com sucesso!', '\n')
            cadastro = 1
            pass
        elif (saque.text == "0"):
            print("Saldo insuficiente para saque!", '\n')
            cadastro = 1
            pass
        else:
            print("Ocorreu um erro! Por favor tente novamente.", '\n')
            cadastro = 1
            pass

    elif escolhaOperacao == "5":
        print("Agradeçemos a sua presença, até a próxima! ", '\n')
        break
    else:
        print("Favor escolher entre: '1-TRANSAÇÃO, 2-SALDO, 3-DEPOSITAR, 4-SACAR, 5-SAIR': ")
else:
    print('Ocorreu um erro, por favor, faça login ou cadastro novamente.', '\n')
    exit(1)



