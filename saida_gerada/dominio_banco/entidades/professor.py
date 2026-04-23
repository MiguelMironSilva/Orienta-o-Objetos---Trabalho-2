from dataclasses import dataclass
from typing import Optional

@dataclass
class Professor:
    """
    Classe gerada automaticamente representando a tabela 'professor'.
    """
    id_professor: Optional[int] = None  # Chave Primária (Auto-incremento)
    nome: str
    titulacao: str
    id_departamento: int