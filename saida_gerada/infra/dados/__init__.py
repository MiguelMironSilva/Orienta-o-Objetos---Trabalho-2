from .armazenamento import GerenciadorDB

from .dao import DAOBase

# Define explicitamente a API pública do pacote infra.dados
__all__ = [
	"GerenciadorDB",
	"DAOBase"
]