import random
import string
import sqlite3

# Importa a estrutura do Framework do Trabalho 1
from dominio_banco.entidades.professor import Professor
from dominio_banco.dados.professor_dao import ProfessorDao

def gerar_string_aleatoria(tamanho=10):
    return ''.join(random.choices(string.ascii_letters, k=tamanho))

def executar_exemplo():
    print("="*50)
    print("EXEMPLO DE UTILIZAÇÃO GERADO AUTOMATICAMENTE - PROFESSOR")
    print("="*50)

    # Conexão de teste apontando para o banco em uso
    conexao = sqlite3.connect("meu_banco.db")
    dao = ProfessorDao(conexao)

    print("\n1. GERANDO DADOS ALEATÓRIOS (Conforme exigência do Trabalho 2)...")
    novo_obj = Professor(
        id_professor=None,
        nome=gerar_string_aleatoria(15),
        titulacao=gerar_string_aleatoria(15),
        id_departamento=random.randint(1, 1000)
    )
    
    print(f"Objeto gerado na memória: {novo_obj}")

    print("\n2. TESTANDO INSERÇÃO (CREATE)...")
    dao.inserir(novo_obj)
    id_gerado = novo_obj.id_professor
    print(f"Objeto inserido com sucesso! ID gerado no banco: {id_gerado}")

    print("\n3. TESTANDO LEITURA (READ)...")
    lista = dao.listar_todos()
    print(f"Total de registros na tabela 'professor': {len(lista)}")
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