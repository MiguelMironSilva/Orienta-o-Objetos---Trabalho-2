from saida_gerada.infra.dados.dao.dao_base import DaoBase
from saida_gerada.dominio_banco.entidades.curso import Curso
from typing import List, Optional

class CursoDao(DaoBase):
    """
    DAO gerado automaticamente para a tabela 'curso'.
    Herda as capacidades de conexão de infra.dados.dao.dao_base.DaoBase.
    """

    def inserir(self, obj: Curso) -> None:
        sql = """
            INSERT INTO curso (
                nome,
                duracao_semestres,
                id_departamento
            ) VALUES (
                ?,
                ?,
                ?
            )
        """
        valores = (
            obj.nome,
            obj.duracao_semestres,
            obj.id_departamento,
        )
        # Assumindo que DaoBase possui self.conexao ou um método executar()
        cursor = self.conexao.cursor()
        cursor.execute(sql, valores)
        self.conexao.commit()
        obj.id_curso = cursor.lastrowid  # Atualiza o ID do objeto após o insert

    def alterar(self, obj: Curso) -> None:
        sql = """
            UPDATE curso SET
                nome = ?,
                duracao_semestres = ?,
                id_departamento = ?
            WHERE id_curso = ?
        """
        valores = (
            obj.nome,
            obj.duracao_semestres,
            obj.id_departamento,
            obj.id_curso,
        )
        self.conexao.cursor().execute(sql, valores)
        self.conexao.commit()

    def excluir(self, id_obj: int) -> None:
        sql = "DELETE FROM curso WHERE id_curso = ?"
        self.conexao.cursor().execute(sql, (id_obj,))
        self.conexao.commit()

    def listar_todos(self) -> List[Curso]:
        sql = "SELECT * FROM curso"
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        linhas = cursor.fetchall()
        
        resultados = []
        for linha in linhas:
            # Desempacota a linha do banco na entidade
            obj = Curso(*linha)
            resultados.append(obj)
        return resultados