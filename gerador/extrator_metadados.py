import sqlite3
from typing import List, Dict, Any

class ExtratorMetadadosSQLite:
    """
    Classe responsável por ler a estrutura de um banco de dados SQLite
    e extrair os metadados necessários para a geração de código.
    """
    
    def __init__(self, caminho_banco: str):
        self.caminho_banco = caminho_banco

    def _mapear_tipo_python(self, tipo_sql: str) -> str:
        """
        Converte o tipo de dado do SQLite para o tipo equivalente em Python.
        """
        tipo_sql = tipo_sql.upper()
        if "INT" in tipo_sql:
            return "int"
        elif "REAL" in tipo_sql or "FLOAT" in tipo_sql or "DOUBLE" in tipo_sql or "NUMERIC" in tipo_sql:
            return "float"
        elif "BOOL" in tipo_sql:
            return "bool"
        else:
            # TEXT, VARCHAR, CHAR, BLOB e tipos desconhecidos viram string por padrão
            return "str"

    def _formatar_nome_classe(self, nome_tabela: str) -> str:
        """
        Transforma 'tabela_clientes' em 'TabelaClientes' ou 'clientes' em 'Cliente'.
        Remove o 's' final de forma rudimentar para o singular (apenas para exemplo acadêmico).
        """
        # Divide por underline, capitaliza cada parte e junta tudo (CamelCase)
        partes = nome_tabela.split('_')
        nome_camel = "".join(palavra.capitalize() for palavra in partes)
        
        # Tentativa básica de deixar no singular (ex: Clientes -> Cliente)
        if nome_camel.endswith('s'):
            nome_camel = nome_camel[:-1]
            
        return nome_camel

    def extrair(self) -> List[Dict[str, Any]]:
        """
        Conecta ao banco, lê todas as tabelas e suas colunas, 
        retornando uma lista de dicionários pronta para o Jinja2.
        """
        try:
            conexao = sqlite3.connect(self.caminho_banco)
            cursor = conexao.cursor()

            # 1. Busca todas as tabelas do banco (ignorando tabelas internas do SQLite)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tabelas = [linha[0] for linha in cursor.fetchall()]

            resultado_metadados = []

            # 2. Para cada tabela, busca as informações das colunas
            for nome_tabela in tabelas:
                # O PRAGMA table_info retorna: (cid, name, type, notnull, dflt_value, pk)
                cursor.execute(f"PRAGMA table_info({nome_tabela});")
                info_colunas = cursor.fetchall()

                colunas_formatadas = []
                for col in info_colunas:
                    nome_coluna = col[1]
                    tipo_sql = col[2]
                    is_pk = bool(col[5])  # col[5] é 1 se for Primary Key, 0 se não for

                    colunas_formatadas.append({
                        "nome": nome_coluna,
                        "tipo_python": self._mapear_tipo_python(tipo_sql),
                        "is_pk": is_pk
                    })

                # 3. Monta o dicionário que o Jinja2 vai receber
                dados_tabela = {
                    "nome_tabela": nome_tabela,
                    "nome_classe": self._formatar_nome_classe(nome_tabela),
                    "colunas": colunas_formatadas
                }
                resultado_metadados.append(dados_tabela)

            return resultado_metadados

        except sqlite3.Error as e:
            raise Exception(f"Erro ao ler metadados do SQLite: {e}")
        finally:
            if 'conexao' in locals():
                conexao.close()