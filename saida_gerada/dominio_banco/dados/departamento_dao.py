from saida_gerada.infra.dados.dao.dao_base import DaoBase
from saida_gerada.dominio_banco.entidades.departamento import Departamento
from typing import List, Optional

class DepartamentoDao(DaoBase):
    """
    DAO gerado automaticamente para a tabela 'departamento'.
    Herda as capacidades de conexão de infra.dados.dao.dao_base.DaoBase.
    """

    def inserir(self, obj: Departamento) -> None:
        sql = """
            INSERT INTO departamento (
                nome,
                sigla
            ) VALUES (
                ?,
                ?
            )
        """
        valores = (
            obj.nome,
            obj.sigla,
        )
        # Assumindo que DaoBase possui self.conexao ou um método executar()
        cursor = self.conexao.cursor()
        cursor.execute(sql, valores)
        self.conexao.commit()
        obj.id_departamento = cursor.lastrowid  # Atualiza o ID do objeto após o insert

    def alterar(self, obj: Departamento) -> None:
        sql = """
            UPDATE departamento SET
                nome = ?,
                sigla = ?
            WHERE id_departamento = ?
        """
        valores = (
            obj.nome,
            obj.sigla,
            obj.id_departamento,
        )
        self.conexao.cursor().execute(sql, valores)
        self.conexao.commit()

    def excluir(self, id_obj: int) -> None:
        sql = "DELETE FROM departamento WHERE id_departamento = ?"
        self.conexao.cursor().execute(sql, (id_obj,))
        self.conexao.commit()

    def listar_todos(self) -> List[Departamento]:
        sql = "SELECT * FROM departamento"
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        linhas = cursor.fetchall()
        
        resultados = []
        for linha in linhas:
            # Desempacota a linha do banco na entidade
            obj = Departamento(*linha)
            resultados.append(obj)
        return resultados