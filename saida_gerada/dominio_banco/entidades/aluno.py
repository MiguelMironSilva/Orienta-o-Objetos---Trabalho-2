from dataclasses import dataclass
from typing import Optional

@dataclass
class Aluno:
    """
    Classe gerada automaticamente representando a tabela 'aluno'.
    """
    id_aluno: Optional[int] = None  # Chave Primária (Auto-incremento)
    nome: str
    cpf: str
    data_ingresso: str
    matricula_ativa: int