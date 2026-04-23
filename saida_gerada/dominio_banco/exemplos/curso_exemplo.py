import random
import string
import sqlite3

# Importa a estrutura do Framework do Trabalho 1
from dominio_banco.entidades.curso import Curso
from dominio_banco.dados.curso_dao import CursoDao

def gerar_string_aleatoria(tamanho=10):
    return ''.join(random.choices(string.ascii_letters, k=tamanho))

def executar_exemplo():
    print("="*50)
    print("EXEMPLO DE UTILIZAÇÃO GERADO AUTOMATICAMENTE - CURSO")
    print("="*50)

    # Conexão de teste apontando para o banco em uso
    conexao = sqlite3.connect("meu_banco.db")
    dao = CursoDao(conexao)

    print("\n1. GERANDO DADOS ALEATÓRIOS (Conforme exigência do Trabalho 2)...")
    novo_obj = Curso(
        id_curso=None,
        nome=gerar_string_aleatoria(15),
        duracao_semestres=random.randint(1, 1000),
        id_departamento=random.randint(1, 1000)
    )
    
    print(f"Objeto gerado na memória: {novo_obj}")

    print("\n2. TESTANDO INSERÇÃO (CREATE)...")
    dao.inserir(novo_obj)
    id_gerado = novo_obj.id_curso
    print(f"Objeto inserido com sucesso! ID gerado no banco: {id_gerado}")

    print("\n3. TESTANDO LEITURA (READ)...")
    lista = dao.listar_todos()
    print(f"Total de registros na tabela 'curso': {len(lista)}")
    for item in lista[-3:]: # Mostra os últimos 3 para não poluir o terminal
        print(f" - {item}")

    print("\n4. TESTANDO ALTERAÇÃO (UPDATE)...")
    novo_obj.nome = "VALOR_ATUALIZADO_TESTE"
    print(f"Alterando a propriedade 'nome' do objeto...")
    dao.alterar(novo_obj)
    print("Objeto alterado no banco de dados com sucesso.")

    print("\n5. TESTANDO EXCLUSÃO (DELETE)...")
    dao.excluir(id_gerado)
    print(f"Objeto com ID {id_gerado} foi excluído do banco.")
    
    conexao.close()
    print("\nTeste finalizado com sucesso!")

if __name__ == "__main__":
    executar_exemplo()