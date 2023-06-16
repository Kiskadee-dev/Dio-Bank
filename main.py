from datetime import datetime
from enum import Enum


class Operacoes(Enum):
    DEPOSITO = "Depósito"
    SAQUE = "Saque"


class Operacao:
    def __init__(self, valor: float, tipo: str):
        self.valor = valor
        self.tipo = tipo
        self.data = datetime.now()


class Bank:
    def __init__(self):
        self.saldo = 0
        self.limite = 500
        self.extrato = "====== EXTRATO ======"
        self.historico: list[Operacao] = []
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, num: float) -> None:
        self.saldo += num
        self.historico.append(Operacao(num, Operacoes.DEPOSITO.value))

    def saque(self, num: float) -> None:
        """
        Saca um valor da conta caso os requisitos sejam cumpridos
        :param num: O valor a ser sacado
        :return: None
        """
        excedeu_saldo = num > self.saldo
        excedeu_limite = num > self.limite
        excedeu_numero_saques = self.numero_saques > self.LIMITE_SAQUES - 1

        if excedeu_saldo:
            print("Falha! Saldo insuficiente para saque.")
        elif excedeu_limite:
            print("Falha! Limite excedido!")
        elif excedeu_numero_saques:
            print("Falha! Número de saques excedido!")
        elif num <= 0:
            print("Falha! Valor de saque inválido!")
        else:
            self.saldo -= num
            self.numero_saques += 1
            self.historico.append(Operacao(num, Operacoes.SAQUE.value))

    def exibir_extrato(self) -> None:
        """
        Exibe o extrato
        :return:
        """
        print(self.extrato)
        print(f"Data: {datetime.now()}")
        print(f"Saldo atual: {self.saldo:.2f}")
        if len(self.historico) > 0:
            for op in self.historico:
                print(f"{op.tipo}: R$ {op.valor:.2f} em {op.data}")
        else:
            print("Nenhuma transação efetuada.")
        print("=====================")


menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [d] Sair

==> """


def user_input(msg: str) -> float:
    """
    Returns the sanitized value from user input
    :param msg: string to be presented to user
    :return: the value
    """
    num = input(msg)
    while not num.isnumeric():
        print("Valor inválido!")
        num = input(msg)
    num = abs(float(num))
    return float(num)


banco = Bank()

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = user_input("Digite o valor a ser depositado: ")
        banco.depositar(valor)
    elif opcao == "s":
        valor = user_input("Digite o valor para saque: ")
        banco.saque(valor)
    elif opcao == "e":
        banco.exibir_extrato()
    elif opcao == "q":
        break
