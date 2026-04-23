from saida_gerada.infra.dados.dao.dao_base import DaoBase
from saida_gerada.dominio_banco.entidades.matricula import Matricula
from typing import List, Optional

class MatriculaDao(DaoBase):
    """
    DAO gerado automaticamente para a tabela 'matricula'.
    Herda as capacidades de conexão de infra.dados.dao.dao_base.DaoBase.
    """

    def inserir(self, obj: Matricula) -> None:
        sql = """
            INSERT INTO matricula (
                id_aluno,
                id_curso,
                data_matricula,
                status
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """
        valores = (
            obj.id_aluno,
            obj.id_curso,
            obj.data_matricula,
            obj.status,
        )
        # Assumindo que DaoBase possui self.conexao ou um método executar()
        cursor = self.conexao.cursor()
        cursor.execute(sql, valores)
        self.conexao.commit()
        obj.id_matricula = cursor.lastrowid  # Atualiza o ID do objeto após o insert

    def alterar(self, obj: Matricula) -> None:
        sql = """
            UPDATE matricula SET
                id_aluno = ?,
                id_curso = ?,
                data_matricula = ?,
                status = ?
            WHERE id_matricula = ?
        """
        valores = (
            obj.id_aluno,
            obj.id_curso,
            obj.data_matricula,
            obj.status,
            obj.id_matricula,
        )
        self.conexao.cursor().execute(sql, valores)
        self.conexao.commit()

    def excluir(self, id_obj: int) -> None:
        sql = "DELETE FROM matricula WHERE id_matricula = ?"
        self.conexao.cursor().execute(sql, (id_obj,))
        self.conexao.commit()

    def listar_todos(self) -> List[Matricula]:
        sql = "SELECT * FROM matricula"
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        linhas = cursor.fetchall()
        
        resultados = []
        for linha in linhas:
            # Desempacota a linha do banco na entidade
            obj = Matricula(*linha)
            resultados.append(obj)
        return resultados