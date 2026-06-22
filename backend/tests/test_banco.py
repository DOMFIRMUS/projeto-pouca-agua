import pytest
from models.banco import Cliente, PessoaFisica, PessoaJuridica, Conta, ContaCorrente, ContaPoupanca

def test_cliente_criacao():
    c = Cliente("João")
    assert c.nome == "João"

def test_pessoa_fisica_criacao():
    pf = PessoaFisica("Ana", "123.456.789-00")
    assert pf.nome == "Ana"
    assert pf.cpf == "123.456.789-00"

def test_pessoa_juridica_criacao():
    pj = PessoaJuridica("Empresa X", "12.345.678/0001-90")
    assert pj.nome == "Empresa X"
    assert pj.cnpj == "12.345.678/0001-90"

def test_conta_basica():
    pf = PessoaFisica("Carlos", "111.222.333-44")
    conta = Conta("1234", "001", pf, 100.0)
    assert conta.numero == "1234"
    assert conta.agencia == "001"
    assert conta.cliente == pf
    assert conta.saldo == 100.0

def test_conta_depositar():
    pf = PessoaFisica("Carlos", "111.222.333-44")
    conta = Conta("1234", "001", pf, 100.0)
    conta.depositar(50.0)
    assert conta.saldo == 150.0

def test_conta_sacar_sucesso():
    pf = PessoaFisica("Carlos", "111.222.333-44")
    conta = Conta("1234", "001", pf, 100.0)
    resultado = conta.sacar(40.0)
    assert resultado is True
    assert conta.saldo == 60.0

def test_conta_sacar_falha():
    pf = PessoaFisica("Carlos", "111.222.333-44")
    conta = Conta("1234", "001", pf, 100.0)
    resultado = conta.sacar(150.0)
    assert resultado is False
    assert conta.saldo == 100.0

def test_conta_corrente_limite_sucesso():
    pj = PessoaJuridica("Loja Y", "98.765.432/0001-10")
    cc = ContaCorrente("5678", "002", pj, 100.0, 500.0)
    resultado = cc.sacar(300.0)
    assert resultado is True
    assert cc.saldo == -200.0

def test_conta_corrente_limite_falha():
    pj = PessoaJuridica("Loja Y", "98.765.432/0001-10")
    cc = ContaCorrente("5678", "002", pj, 100.0, 500.0)
    resultado = cc.sacar(700.0)
    assert resultado is False
    assert cc.saldo == 100.0

def test_conta_poupanca():
    pf = PessoaFisica("Maria", "999.888.777-66")
    cp = ContaPoupanca("9012", "003", pf, 50.0)
    assert cp.saldo == 50.0
    cp.depositar(10.0)
    assert cp.saldo == 60.0
    resultado = cp.sacar(70.0)
    assert resultado is False
    assert cp.saldo == 60.0
