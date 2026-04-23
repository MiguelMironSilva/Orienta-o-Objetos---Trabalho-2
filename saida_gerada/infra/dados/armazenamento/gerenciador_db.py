# framework_universidade/infra/dados/armazenamento/gerenciador_db.py

import sqlite3
from typing import List, Tuple, Any, Optional

class GerenciadorDB:
    """
    Gerenciador de Conexão com o Banco de Dados.
    Implementa o padrão Singleton para garantir uma única instância de conexão
    ativa em toda a aplicação, otimizando o uso de recursos.
    """
    
    _instancia = None

    def __new__(cls):
        """
        Método mágico do Python para implementar o Singleton.
        Se a instância já existe, retorna ela mesma. Se não, cria uma nova.
        """
        if cls._instancia is None:
            cls._instancia = super(GerenciadorDB, cls).__new__(cls)
            cls._instancia.conexao = None
        return cls._instancia

    def conectar(self, nome_banco: str = "banco.db"):
        """Abre a conexão com o banco de dados (se já não estiver aberta)."""
        if self.conexao is None:
            # check_same_thread=False previne erros caso a interface rode em threads separadas
            self.conexao = sqlite3.connect(nome_banco, check_same_thread=False)
            
            # TRUQUE DE MESTRE: Configura o cursor para retornar linhas como dicionários!
            # Isso nos permite fazer row["nome"] ao invés de row[1], facilitando muito a vida dos DAOs.
            self.conexao.row_factory = sqlite3.Row
            
            # Ativa o suporte a chaves estrangeiras (Foreign Keys) no SQLite
            self.conexao.execute("PRAGMA foreign_keys = ON")

    def desconectar(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def executar_leitura(self, query: str, parametros: Tuple = ()) -> List[sqlite3.Row]:
        """
        Executa consultas SQL de leitura (SELECT).
        Retorna uma lista de linhas (Rows).
        """
        cursor = self.conexao.cursor()
        cursor.execute(query, parametros)
        return cursor.fetchall()

    def executar_escrita(self, query: str, parametros: Tuple = ()) -> Optional[int]:
        """
        Executa comandos SQL de escrita (INSERT, UPDATE, DELETE).
        Gerencia automaticamente o Commit (salvar) e Rollback (desfazer em caso de erro).
        Retorna o ID da última linha inserida (útil para INSERTs).
        """
        cursor = self.conexao.cursor()
        try:
            cursor.execute(query, parametros)
            self.conexao.commit()
            return cursor.lastrowid
        except Exception as e:
            # Se der qualquer erro (ex: violação de Unique, Foreign Key), desfaz a transação!
            self.conexao.rollback()
            raise e  # Repassa a exceção para o DAO ou Formulário tratar amigavelmente

    def inicializar_banco_via_script(self, caminho_script: str):
        """
        Lê um arquivo .sql (como o nosso schema.sql) e o executa no banco.
        Ideal para criar as tabelas na primeira vez que o sistema rodar.
        """
        try:
            with open(caminho_script, 'r', encoding='utf-8') as arquivo:
                script_sql = arquivo.read()
                
            cursor = self.conexao.cursor()
            cursor.executescript(script_sql)
            self.conexao.commit()
        except FileNotFoundError:
            print(f"[Erro] Arquivo de script {caminho_script} não encontrado.")
        except Exception as e:
            print(f"[Erro Crítico] Falha ao inicializar o banco de dados: {e}")