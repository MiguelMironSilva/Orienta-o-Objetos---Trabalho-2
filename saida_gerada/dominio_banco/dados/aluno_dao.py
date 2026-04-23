from saida_gerada.infra.dados.dao.dao_base import DaoBase
from saida_gerada.dominio_banco.entidades.aluno import Aluno
from typing import List, Optional

class AlunoDao(DaoBase):
    """
    DAO gerado automaticamente para a tabela 'aluno'.
    Herda as capacidades de conexão de infra.dados.dao.dao_base.DaoBase.
    """

    def inserir(self, obj: Aluno) -> None:
        sql = """
            INSERT INTO aluno (
                nome,
                cpf,
                data_ingresso,
                matricula_ativa
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """
        valores = (
            obj.nome,
            obj.cpf,
            obj.data_ingresso,
            obj.matricula_ativa,
        )
        # Assumindo que DaoBase possui self.conexao ou um método executar()
        cursor = self.conexao.cursor()
        cursor.execute(sql, valores)
        self.conexao.commit()
        obj.id_aluno = cursor.lastrowid  # Atualiza o ID do objeto após o insert

    def alterar(self, obj: Aluno) -> None:
        sql = """
            UPDATE aluno SET
                nome = ?,
                cpf = ?,
                data_ingresso = ?,
                matricula_ativa = ?
            WHERE id_aluno = ?
        """
        valores = (
            obj.nome,
            obj.cpf,
            obj.data_ingresso,
            obj.matricula_ativa,
            obj.id_aluno,
        )
        self.conexao.cursor().execute(sql, valores)
        self.conexao.commit()

    def excluir(self, id_obj: int) -> None:
        sql = "DELETE FROM aluno WHERE id_aluno = ?"
        self.conexao.cursor().execute(sql, (id_obj,))
        self.conexao.commit()

    def listar_todos(self) -> List[Aluno]:
        sql = "SELECT * FROM aluno"
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        linhas = cursor.fetchall()
        
        resultados = []
        for linha in linhas:
            # Desempacota a linha do banco na entidade
            obj = Aluno(*linha)
            resultados.append(obj)
        return resultados