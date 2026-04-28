from .base_errors import RegistroNaoEncontradoError, ErroDeValidacao

# Define os módulos exportados ao utilizar 'from infra.entidades import *'
__all__ = [
    "RegistroNaoEncontradoError",
    "ErroDeValidacao"
]