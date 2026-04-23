from saida_gerada.infra.dados.dao.dao_base import DaoBase
from saida_gerada.dominio_banco.entidades.professor import Professor
from typing import List, Optional

class ProfessorDao(DaoBase):
    """
    DAO gerado automaticamente para a tabela 'professor'.
    Herda as capacidades de conexão de infra.dados.dao.dao_base.DaoBase.
    """

    def inserir(self, obj: Professor) -> None:
        sql = """
            INSERT INTO professor (
                nome,
                titulacao,
                id_departamento
            ) VALUES (
                ?,
                ?,
                ?
            )
        """
        valores = (
            obj.nome,
            obj.titulacao,
            obj.id_departamento,
        )
        # Assumindo que DaoBase possui self.conexao ou um método executar()
        cursor = self.conexao.cursor()
        cursor.execute(sql, valores)
        self.conexao.commit()
        obj.id_professor = cursor.lastrowid  # Atualiza o ID do objeto após o insert

    def alterar(self, obj: Professor) -> None:
        sql = """
            UPDATE professor SET
                nome = ?,
                titulacao = ?,
                id_departamento = ?
            WHERE id_professor = ?
        """
        valores = (
            obj.nome,
            obj.titulacao,
            obj.id_departamento,
            obj.id_professor,
        )
        self.conexao.cursor().execute(sql, valores)
        self.conexao.commit()

    def excluir(self, id_obj: int) -> None:
        sql = "DELETE FROM professor WHERE id_professor = ?"
        self.conexao.cursor().execute(sql, (id_obj,))
        self.conexao.commit()

    def listar_todos(self) -> List[Professor]:
        sql = "SELECT * FROM professor"
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        linhas = cursor.fetchall()
        
        resultados = []
        for linha in linhas:
            # Desempacota a linha do banco na entidade
            obj = Professor(*linha)
            resultados.append(obj)
        return resultados