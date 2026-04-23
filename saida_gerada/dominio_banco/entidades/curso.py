from dataclasses import dataclass
from typing import Optional

@dataclass
class Curso:
    """
    Classe gerada automaticamente representando a tabela 'curso'.
    """
    id_curso: Optional[int] = None  # Chave Primária (Auto-incremento)
    nome: str
    duracao_semestres: int
    id_departamento: int