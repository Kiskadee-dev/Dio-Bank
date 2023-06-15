class Bank:
    def __init__(self):
        self.saldo = 0
        self.limite = 500
        self.extrato = "==EXTRATO=="
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, num: float) -> None:
        self.saldo += num
        self.extrato += f"\nDEPÓSITO: R$ {num:.2f}"

    def saque(self, num: float) -> None:
        """
        Saca um valor da conta caso os requisitos sejam cumpridos
        :param num: O valor a ser sacado
        :return: None
        """
        excedeu_saldo = num > self.saldo
        excedeu_limite = num > self.limite
        excedeu_numero_saques = self.numero_saques > self.LIMITE_SAQUES

        if excedeu_saldo:
            print("Falha! Saldo insuficiente para saque.")
        elif excedeu_limite:
            print("Falha! Limite excedido!")
        elif excedeu_numero_saques:
            print("Falha! Número de saques excedido!")
        else:
            self.saldo -= num
            self.extrato += f"\nSAQUE: R$ {num:.2f}"
            self.numero_saques += 1

    def exibir_extrato(self) -> None:
        print(self.extrato)


menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [d] Sair

==>"""


def user_input(msg: str) -> float:
    """
    Returns the sanitized value from user input
    :param msg: string to be presented to user
    :return: the value
    """
    num = input(msg)
    while not num.isnumeric():
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
