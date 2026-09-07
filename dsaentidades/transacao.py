from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transacao:
    """Modelo imutável para histórico de movimentações bancárias (Value Object)."""

    data_hora: datetime
    tipo: str
    valor: float

    def __str__(self) -> str:
        return f"- {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}: {self.tipo} de R${self.valor:.2f}"