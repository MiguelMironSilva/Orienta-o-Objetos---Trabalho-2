import os
import sys
import argparse
from gerador import ExtratorMetadadosSQLite, GeradorArquivos

def exibir_banner():
    """Exibe um cabeçalho informativo no terminal."""
    print("="*60)
    print("       GERADOR DE CRUDS - TRABALHO 2 (ORIENTAÇÃO A OBJETOS)")
    print("       Baseado no Framework do Trabalho 1")
    print("="*60)

def main():
    exibir_banner()

    # 1. Configura o tratamento de argumentos de linha de comando
    # Ex: python main_gerador.py caminho/do/banco.db
    parser = argparse.ArgumentParser(
        description="Gera classes de Entidade, DAO e Exemplos a partir de um banco SQLite."
    )
    parser.add_argument(
        "banco", 
        help="Caminho para o arquivo .db do SQLite (ex: universidade.db)"
    )
    parser.add_argument(
        "--saida", 
        default="saida_gerada/dominio_banco",
        help="Diretório onde o código será gerado (Padrão: saida_gerada/dominio_banco)"
    )

    args = parser.parse_args()

    # 2. Validação da existência do banco de dados (Tratamento de Exceções)
    if not os.path.exists(args.banco):
        print(f"\n[ERRO] O arquivo de banco de dados '{args.banco}' não foi encontrado.")
        sys.exit(1)

    try:
        # 3. Passo: Extração de Metadados
        print(f"\n[1/3] Lendo metadados do banco: {args.banco}...")
        extrator = ExtratorMetadadosSQLite(args.banco)
        metadados = extrator.extrair()

        if not metadados:
            print("[AVISO] Nenhuma tabela encontrada no banco de dados informado.")
            sys.exit(0)

        print(f"      -> {len(metadados)} tabelas identificadas.")

        # 4. Passo: Geração de Ficheiros
        print(f"[2/3] Configurando ambiente de geração em '{args.saida}'...")
        gerador = GeradorArquivos(metadados, pasta_saida=args.saida)
        
        print("[3/3] Renderizando templates e gravando ficheiros...")
        gerador.gerar_tudo()

        # 5. Finalização
        print("\n" + "="*60)
        print(" SUCESSO: O seu CRUD foi gerado com sucesso!")
        print(f" Localização: {os.path.abspath(args.saida)}")
        print("="*60)
        print("\nPróximos passos:")
        print(f" 1. Verifique a pasta '{args.saida}/exemplos'")
        print(" 2. Execute um dos arquivos '_exemplo.py' para testar o funcionamento.")

    except Exception as e:
        print(f"\n[FALHA CRÍTICA] Ocorreu um erro durante a geração:")
        print(f" > {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()