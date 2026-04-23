from dataclasses import dataclass
from typing import Optional

@dataclass
class Matricula:
    """
    Classe gerada automaticamente representando a tabela 'matricula'.
    """
    id_matricula: Optional[int] = None  # Chave Primária (Auto-incremento)
    id_aluno: int
    id_curso: int
    data_matricula: str
    status: str