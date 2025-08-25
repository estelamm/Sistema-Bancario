from abc import ABC, abstractmethod
from datetime import date, datetime


# ================= CLASSES DE CLIENTE =================

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"


# ================= CLASSES DE CONTA =================

class Conta:
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor: float) -> bool:
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        elif valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

        self.saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

        self.saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500, limite_saques: int = 3, agencia: str = "0001"):
        super().__init__(numero, cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor: float) -> bool:
        if valor > self.limite:
            print("\n@@@ Operação falhou! Valor excede limite. @@@")
            return False
        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Limite de saques atingido. @@@")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False

    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.cliente.nome}"


# ================= HISTÓRICO =================

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


# ================= TRANSAÇÕES =================

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ================= PROGRAMA PRINCIPAL =================

def main():
    clientes = []
    contas = []

    while True:
        opcao = input("""
        ================ MENU ================
        [nu] Novo usuário
        [nc] Nova conta
        [lc] Listar contas
        [d]  Depositar
        [s]  Sacar
        [e]  Extrato
        [q]  Sair
        => """)

        if opcao == "nu":
            nome = input("Nome completo: ")
            cpf = input("CPF: ")
            nascimento = input("Data de nascimento (dd-mm-aaaa): ")
            endereco = input("Endereço: ")

            cliente = PessoaFisica(nome, cpf, nascimento, endereco)
            clientes.append(cliente)
            print("\n=== Cliente criado com sucesso! ===")

        elif opcao == "nc":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            numero_conta = len(contas) + 1
            conta = ContaCorrente(numero=numero_conta, cliente=cliente)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")

        elif opcao == "lc":
            for conta in contas:
                print("=" * 60)
                print(conta)

        elif opcao in ["d", "s", "e"]:
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            if not cliente.contas:
                print("\n@@@ Cliente não possui contas! @@@")
                continue

            conta = cliente.contas[0]

            if opcao == "d":
                valor = float(input("Valor do depósito: "))
                cliente.realizar_transacao(conta, Deposito(valor))

            elif opcao == "s":
                valor = float(input("Valor do saque: "))
                cliente.realizar_transacao(conta, Saque(valor))

            elif opcao == "e":
                print("\n================ EXTRATO ================")
                for transacao in conta.historico.transacoes:
                    print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f}\t- {transacao['data']}")
                print(f"\nSaldo atual:\tR$ {conta.saldo_atual():.2f}")
                print("==========================================")

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida! @@@")


if __name__ == "__main__":
    main()
