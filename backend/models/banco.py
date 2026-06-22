class Cliente:
    def __init__(self, nome: str):
        self.nome = nome

class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str):
        super().__init__(nome)
        self.cpf = cpf

class PessoaJuridica(Cliente):
    def __init__(self, nome: str, cnpj: str):
        super().__init__(nome)
        self.cnpj = cnpj

class Conta:
    def __init__(self, numero: str, agencia: str, cliente: Cliente, saldo: float = 0.0):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = saldo

    def sacar(self, valor: float) -> bool:
        if valor > 0 and self.saldo >= valor:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor: float) -> None:
        if valor > 0:
            self.saldo += valor

class ContaCorrente(Conta):
    def __init__(self, numero: str, agencia: str, cliente: Cliente, saldo: float = 0.0, limite: float = 0.0):
        super().__init__(numero, agencia, cliente, saldo)
        self.limite = limite

    def sacar(self, valor: float) -> bool:
        if valor > 0 and (self.saldo + self.limite) >= valor:
            self.saldo -= valor
            return True
        return False

class ContaPoupanca(Conta):
    def __init__(self, numero: str, agencia: str, cliente: Cliente, saldo: float = 0.0):
        super().__init__(numero, agencia, cliente, saldo)
