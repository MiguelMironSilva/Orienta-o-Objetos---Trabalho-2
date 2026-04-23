# framework_universidade/infra/dados/dao/dao_base.py

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Any, Dict
from infra.dados.armazenamento.gerenciador_db import GerenciadorDB
from infra.excecoes.base_errors import RegistroNaoEncontradoError

# Define um tipo genérico 'T' que representará as Entidades (Aluno, Curso, etc.)
T = TypeVar('T')

class DAOBase(ABC, Generic[T]):
    """
    Classe Abstrata Genérica para Acesso a Dados (DAO).
    Implementa automaticamente as instruções SQL de INSERT, UPDATE, DELETE e SELECT 
    para qualquer tabela, baseando-se nas configurações fornecidas pelas classes filhas.
    """

    def __init__(self):
        # Todos os DAOs obtêm a mesma instância Singleton da conexão
        self.db = GerenciadorDB()

    # =========================================================================
    # MÉTODOS ABSTRATOS (Contratos que as classes filhas DEVEM implementar)
    # =========================================================================

    @property
    @abstractmethod
    def _nome_tabela(self) -> str:
        """Deve retornar o nome da tabela no banco de dados (ex: 'aluno')."""
        pass

    @property
    @abstractmethod
    def _chave_primaria(self) -> str:
        """Deve retornar o nome da coluna de chave primária (ex: 'id_aluno')."""
        pass

    @abstractmethod
    def _mapear_linha_para_objeto(self, linha: Any) -> T:
        """Converte uma linha do banco (sqlite3.Row) em uma instância do @dataclass."""
        pass

    @abstractmethod
    def _extrair_dicionario(self, objeto: T) -> Dict[str, Any]:
        """
        Converte as propriedades do objeto em um dicionário {coluna: valor}.
        Isso permite que a classe pai monte os SQLs de Inserção e Alteração dinamicamente.
        """
        pass

    # =========================================================================
    # MÉTODOS CONCRETOS (O Framework faz o trabalho pesado)
    # =========================================================================

    def listar_todos(self) -> List[T]:
        """Busca todos os registros da tabela e os converte em uma lista de objetos."""
        query = f"SELECT * FROM {self._nome_tabela}"
        linhas = self.db.executar_leitura(query)
        
        # Usa list comprehension para mapear todas as linhas
        return [self._mapear_linha_para_objeto(linha) for linha in linhas]

    def buscar_por_id(self, id_registro: int) -> T:
        """Busca um único registro pelo seu ID."""
        query = f"SELECT * FROM {self._nome_tabela} WHERE {self._chave_primaria} = ?"
        linhas = self.db.executar_leitura(query, (id_registro,))
        
        if not linhas:
            raise RegistroNaoEncontradoError(f"Registro com ID {id_registro} não encontrado na tabela {self._nome_tabela}.")
            
        return self._mapear_linha_para_objeto(linhas[0])

    def excluir(self, id_registro: int) -> None:
        """Remove um registro do banco de dados (após verificar se ele existe)."""
        # Apenas para lançar o erro se não existir
        self.buscar_por_id(id_registro) 
        
        query = f"DELETE FROM {self._nome_tabela} WHERE {self._chave_primaria} = ?"
        self.db.executar_escrita(query, (id_registro,))

    def incluir(self, objeto: T) -> T:
        """
        Constrói dinamicamente um comando INSERT INTO baseando-se no dicionário
        de atributos do objeto.
        """
        dados = self._extrair_dicionario(objeto)
        
        # Remove a PK do dicionário se for None (pois o banco AUTOINCREMENT vai gerar)
        if self._chave_primaria in dados and dados[self._chave_primaria] is None:
            del dados[self._chave_primaria]

        # Monta a string do SQL dinamicamente: "col1, col2, col3" e "?, ?, ?"
        colunas = ", ".join(dados.keys())
        placeholders = ", ".join(["?"] * len(dados))
        valores = tuple(dados.values())

        query = f"INSERT INTO {self._nome_tabela} ({colunas}) VALUES ({placeholders})"
        novo_id = self.db.executar_escrita(query, valores)

        # Atualiza o objeto na memória com o novo ID gerado pelo banco
        setattr(objeto, self._chave_primaria, novo_id)
        return objeto

    def alterar(self, objeto: T) -> None:
        """
        Constrói dinamicamente um comando UPDATE baseando-se no dicionário
        de atributos do objeto.
        """
        dados = self._extrair_dicionario(objeto)
        id_valor = getattr(objeto, self._chave_primaria)

        # Remove a PK para não tentar dar UPDATE nela mesma
        if self._chave_primaria in dados:
            del dados[self._chave_primaria]

        # Monta a cláusula SET dinamicamente: "col1 = ?, col2 = ?"
        set_clause = ", ".join([f"{col} = ?" for col in dados.keys()])
        valores = tuple(dados.values()) + (id_valor,) # Adiciona o ID no final para o WHERE

        query = f"UPDATE {self._nome_tabela} SET {set_clause} WHERE {self._chave_primaria} = ?"
        self.db.executar_escrita(query, valores)