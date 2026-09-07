from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple

from dsaentidades.cliente import Cliente
from dsaentidades.transacao import Transacao
from dsautilitarios.exceptions import SaldoInsuficienteError


class Conta(ABC):
    """Classe base abstrata para contas bancárias."""

    def __init__(self, numero: int, cliente: Cliente) -> None:
        self._numero = numero
        self._saldo = 0.0
        self._cliente = cliente
        self._historico: List[Transacao] = []

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Tuple[Transacao, ...]:
        """Retorna uma tupla imutável protegendo a lista original."""
        return tuple(self._historico)

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor de depósito deve ser estritamente positivo.")

        self._saldo += valor
        self._historico.append(Transacao(datetime.now(), "Depósito", valor))

    @abstractmethod
    def sacar(self, valor: float) -> None:
        pass

    def transferir(self, valor: float, conta_destino: "Conta") -> None:
        if conta_destino is self:
            raise ValueError("Não é possível realizar transferência para a mesma conta.")

        self.sacar(valor)
        conta_destino.depositar(valor)

        self._historico.append(Transacao(datetime.now(), f"Transferência Enviada (Conta {conta_destino.numero})", valor))
        conta_destino._historico.append(Transacao(datetime.now(), f"Transferência Recebida (Conta {self.numero})", valor))


class ContaCorrente(Conta):
    """Conta com limite de crédito especial."""

    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0) -> None:
        super().__init__(numero, cliente)
        if limite < 0:
            raise ValueError("O limite de crédito não pode ser negativo.")
        self._limite = limite

    @property
    def limite(self) -> float:
        return self._limite

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor de saque deve ser estritamente positivo.")

        saldo_disponivel = self._saldo + self._limite
        if valor > saldo_disponivel:
            raise SaldoInsuficienteError(saldo_disponivel, valor, "Saldo e limite insuficientes.")

        self._saldo -= valor
        self._historico.append(Transacao(datetime.now(), "Saque", valor))


class ContaPoupanca(Conta):
    """Conta poupança sem limite especial."""

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor de saque deve ser estritamente positivo.")

        if valor > self._saldo:
            raise SaldoInsuficienteError(self._saldo, valor, "Saldo insuficiente na conta poupança.")

        self._saldo -= valor
        self._historico.append(Transacao(datetime.now(), "Saque", valor))