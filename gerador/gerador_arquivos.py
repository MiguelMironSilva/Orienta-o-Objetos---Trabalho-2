import os
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Any

class GeradorArquivos:
    """
    Classe responsável por orquestrar a criação de pastas e a renderização
    dos templates Jinja2 para gerar o código-fonte final.
    """

    def __init__(self, metadados_tabelas: List[Dict[str, Any]], pasta_saida: str = "saida_gerada/dominio_banco"):
        self.metadados = metadados_tabelas
        self.pasta_saida = pasta_saida
        
        # Configura o Jinja2 para buscar os templates na pasta correta
        # O FileSystemLoader aponta para onde os arquivos .jinja2 estão salvos
        caminho_templates = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(caminho_templates))

    def _criar_estrutura_pastas(self):
        """
        Garante que a estrutura de diretórios exigida exista antes de salvar os arquivos.
        """
        pastas_necessarias = [
            os.path.join(self.pasta_saida, "entidades"),
            os.path.join(self.pasta_saida, "dados"),
            os.path.join(self.pasta_saida, "exemplos")
        ]
        
        for pasta in pastas_necessarias:
            # exist_ok=True impede que o Python lance um erro se a pasta já existir
            os.makedirs(pasta, exist_ok=True)
            
            # Opcional: cria um arquivo __init__.py vazio para tornar as pastas módulos importáveis
            with open(os.path.join(pasta, "__init__.py"), "a", encoding="utf-8") as f:
                pass
                
        print(f"Estrutura de pastas verificada/criada em: {self.pasta_saida}")

    def _salvar_arquivo(self, caminho_arquivo: str, conteudo: str):
        """
        Escreve o código gerado em um arquivo físico.
        """
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

    def gerar_tudo(self):
        """
        Executa o processo de geração para todas as tabelas lidas do banco.
        """
        print("Iniciando a geração de arquivos...")
        self._criar_estrutura_pastas()

        # Carrega os moldes previamente criados
        template_entidade = self.env.get_template('template_entidade.py.jinja2')
        template_dao = self.env.get_template('template_dao.py.jinja2')
        template_exemplo = self.env.get_template('template_exemplo.py.jinja2')

        for tabela in self.metadados:
            nome_tabela = tabela['nome_tabela'].lower()
            nome_classe = tabela['nome_classe']
            
            print(f"  -> Processando tabela: '{nome_tabela}' (Classe: {nome_classe})...")

            # 1. Gera e salva a Entidade
            codigo_entidade = template_entidade.render(tabela)
            caminho_entidade = os.path.join(self.pasta_saida, "entidades", f"{nome_tabela}.py")
            self._salvar_arquivo(caminho_entidade, codigo_entidade)

            # 2. Gera e salva o DAO
            codigo_dao = template_dao.render(tabela)
            caminho_dao = os.path.join(self.pasta_saida, "dados", f"{nome_tabela}_dao.py")
            self._salvar_arquivo(caminho_dao, codigo_dao)

            # 3. Gera e salva o Script de Exemplo
            codigo_exemplo = template_exemplo.render(tabela)
            caminho_exemplo = os.path.join(self.pasta_saida, "exemplos", f"{nome_tabela}_exemplo.py")
            self._salvar_arquivo(caminho_exemplo, codigo_exemplo)

        print("\nGeração concluída com sucesso! Verifique a pasta de saída.")