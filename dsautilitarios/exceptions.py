class BancoError(Exception):
    """Classe base para exceções do sistema bancário."""
    pass


class SaldoInsuficienteError(BancoError):
    """Exceção lançada quando uma operação excede o saldo/limite disponível."""

    def __init__(self, saldo_atual: float, valor_solicitado: float, mensagem: str = "Saldo insuficiente.") -> None:
        self.saldo_atual = saldo_atual
        self.valor_solicitado = valor_solicitado
        super().__init__(
            f"{mensagem} (Saldo/Limite disponível: R${saldo_atual:.2f}, Solicitado: R${valor_solicitado:.2f})"
        )


class ContaInexistenteError(BancoError):
    """Exceção para buscas por contas que não existem no sistema."""
    pass