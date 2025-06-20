menu = """
Olá, bem vindo ao banco banco, como podemos ajudar?
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

""" 

saldo = 0 
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True: 
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor a ser depositado: "))

        if valor > 0: 
            saldo += valor
            extrato += f"Deposito: R$ {valor:.2f}\n"
        
        else:
            print("Falha na Operação! O valor informado é invalido")

    elif opcao == "2":
        valor = float(input("Informe o valor a ser sacado: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_limite_saque = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Erro na operação! Você não possui saldo suficiente para este saque")

        elif excedeu_limite:
            print("OPS! Só são possivéis saques no valor de até RS500,00")
        
        elif excedeu_limite_saque:
            print("OPS! você excedeu o limite de saques por hoje, volte amanhã ;)")
        
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        
        else: 
            print("ERRO! valor informado é inválido")

    elif opcao == "3":
        print(f"Saldo em conta: R${saldo:.2f}\n")

    elif opcao == "4":
        print("Agradecemos por escolher o banco banco, até a próxima!")
        break

    else: 
        print("Erro na operação! Tente novamente com um valor válido!")    





    