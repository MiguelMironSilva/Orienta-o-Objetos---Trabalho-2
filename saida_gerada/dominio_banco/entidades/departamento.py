from dataclasses import dataclass
from typing import Optional

@dataclass
class Departamento:
    """
    Classe gerada automaticamente representando a tabela 'departamento'.
    """
    id_departamento: Optional[int] = None  # Chave Primária (Auto-incremento)
    nome: str
    sigla: str