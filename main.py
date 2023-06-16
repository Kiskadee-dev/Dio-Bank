from datetime import datetime
from enum import Enum
from typing import Any


class TiposOperacoes(Enum):
    DEPOSITO = "Depósito"
    SAQUE = "Saque"


class Operacao:
    def __init__(self, valor: float, tipo: str):
        self.valor = valor
        self.tipo = tipo
        self.data = datetime.now()


def sanitize_cpf_input(string: str) -> str:
    """
    Sanitiza uma string de CPF, remove barras e pontos
    :param string:
    :return:
    """
    return string.replace("-", "").replace(".", "").strip()


def buscar_usuario(cpf: str, usuarios: dict[str, Any]):
    """
    Busca e retorna um usuário
    :param cpf: O cpf
    :param usuarios: dicionario de usuarios
    :return: O usuário, se existir, None se não existir.
    """
    return usuarios.get(cpf)


class Bank:
    class Usuario:
        def __init__(self, cpf, nome, data_nascimento, endereco):
            self.cpf = cpf
            self.nome = nome
            self.data_nascimento = data_nascimento
            self.endereco = endereco

    class Conta:
        def __init__(self, agencia, numero_conta, cpf_usuario):
            self.agencia = agencia
            self.numero_conta = numero_conta
            self.cpf_usuario = cpf_usuario

    def __init__(self):
        self.AGENCIA = "1234"
        self.saldo = 0
        self.limite = 500
        self.extrato = "====== EXTRATO ======"
        self.historico: list[Operacao] = []
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

        self.repo_contas: list = []
        self.repo_usuarios: dict = {}

    def criar_usuario(self):
        """
        Cria um usuário
        :return: None
        """
        cpf = sanitize_cpf_input(input("Informe o CPF: "))
        while not cpf.isdigit():
            print("Insira um cpf válido!")
            cpf = sanitize_cpf_input(input("Informe o CPF: "))

        if buscar_usuario(cpf, self.repo_usuarios):
            print("@@@ Já existe um usuário com este CPF! @@@")
            return

        nome = input("Insira um nome: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-ano): ")
        endereco = input("Informe o endereco: ")

        usuario = self.Usuario(
            cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco
        )
        self.repo_usuarios[cpf] = usuario
        print("== Usuário criado com sucesso! ==")

    def criar_conta(self):
        """
        Cria uma conta bancária para um usuário
        :return: None
        """

        cpf = sanitize_cpf_input(input("Informe o CPF do usuário: "))
        while not cpf.isdigit():
            print("Insira um cpf válido! ")
            cpf = sanitize_cpf_input(input("Informe o CPF do usuário: "))
        usuario = buscar_usuario(cpf, self.repo_usuarios)
        if not usuario:
            print("@@@ Usuário não encontrado! encerrando criação de conta @@@")
            return
        numero_conta = len(self.repo_contas) + 1
        conta = self.Conta(
            agencia=self.AGENCIA, numero_conta=numero_conta, cpf_usuario=cpf
        )
        self.repo_contas.append(conta)
        print("=== Conta criada com sucesso ===")

    def listar_contas(self):
        """
        Lista as contas de determinado usuario
        :param cpf: o cpf do usuário
        :return: None
        """
        for conta in self.repo_contas:
            print(f"""
            Agência:\t{conta.agencia}
            C/C:\t{conta.numero_conta}
            Titular:\t{self.repo_usuarios[conta.cpf_usuario].nome}
            """)

    def depositar(self, num: float) -> None:
        self.saldo += num
        self.historico.append(Operacao(num, TiposOperacoes.DEPOSITO.value))

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
            self.historico.append(Operacao(num, TiposOperacoes.SAQUE.value))

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


def menu():
    menu = """
    [d]\t\tDepositar
    [s]\t\tSacar
    [e]\t\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Conta
    [q]\t\tSair

    ==>\t"""
    print(menu)


def user_money_input(msg: str) -> float:
    """
    Returns the sanitized value from user input
    :param msg: string to be presented to user
    :return: the float value
    """
    num = input(msg)
    while not num.isnumeric():
        print("Valor inválido!")
        num = input(msg)
    num = abs(float(num))
    return float(num)


banco = Bank()

while True:
    menu()
    opcao = input()

    if opcao == "d":
        valor = user_money_input("Digite o valor a ser depositado: ")
        banco.depositar(valor)
    elif opcao == "s":
        valor = user_money_input("Digite o valor para saque: ")
        banco.saque(valor)
    elif opcao == "e":
        banco.exibir_extrato()
    elif opcao == "nu":
        banco.criar_usuario()
    elif opcao == "nc":
        banco.criar_conta()
    elif opcao == "lc":
        banco.listar_contas()
    elif opcao == "q":
        break
