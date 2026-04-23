# framework_universidade/infra/__init__.py

"""
Infra Package
Este pacote contém o mini-framework base para aplicações CRUD.
Ele é agnóstico de domínio e pode ser reutilizado em qualquer sistema.
"""

# 1. Importações da Camada de Entidades
from .entidades import Registro

# 2. Importações da Camada de Dados
from .dados import DAOBase, GerenciadorDB


# Define explicitamente o que é exportado quando alguém usa `from infra import *`
__all__ = [
    "Registro",
    "DAOBase",
    "GerenciadorDB"
]