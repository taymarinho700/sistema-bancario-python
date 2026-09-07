import re
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from dsaentidades.conta import Conta


class Cliente:
    """Entidade que representa o cliente do banco com validações de integridade."""

    def __init__(self, nome: str, cpf: str) -> None:
        nome_limpo = nome.strip()

        # 1. Validação de quantidade de palavras (Nome + Sobrenome)
        if len(nome_limpo.split()) < 2:
            raise ValueError("O nome do cliente deve conter nome e sobrenome.")

        # 2. Nova validação: verifica se contém números ou caracteres especiais
        # Permite apenas letras (incluindo acentuadas) e espaços
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome_limpo):
            raise ValueError("O nome do cliente deve conter apenas letras e espaços (sem números).")

        # Validação do CPF
        cpf_numerico = re.sub(r"\D", "", cpf)
        if len(cpf_numerico) != 11 or cpf_numerico == cpf_numerico[0] * 11:
            raise ValueError("CPF inválido! O documento deve conter exatamente 11 dígitos válidos.")

        self._nome: str = nome_limpo.title()
        self._cpf: str = cpf_numerico
        self.contas: List["Conta"] = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cpf(self) -> str:
        return self._cpf

    def adicionar_conta(self, conta: "Conta") -> None:
        """Associa uma nova conta ao cliente."""
        if conta not in self.contas:
            self.contas.append(conta)

    def __str__(self) -> str:
        cpf_fmt = f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"
        return f"Cliente: {self._nome} (CPF: {cpf_fmt})"