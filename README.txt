Docente: Eduardo Kessler Piveta
Discente: Miguel Miron Silva

Este guia explica como configurar e utilizar o Gerador de CRUDs, uma ferramenta desenvolvida para automatizar a criação de camadas de software a partir de metadados de bancos de dados SQLite. O projeto foi construído para ser uma extensão direta do Framework de Gestão Universitária (Trabalho 1), respeitando sua arquitetura em camadas e princípios de Análise e Projeto de Software.

Pré-requisitos

Python 3.10 ou superior.

SQLite3 (biblioteca padrão).

Jinja2 (motor de templates para geração de código).

Estrutura do Projeto
O gerador está organizado para separar a lógica de inspeção do banco da lógica de escrita de arquivos:

gerador/: Núcleo da ferramenta.

extrator_metadados.py: Responsável por ler o sqlite_master e os PRAGMA do banco para identificar tabelas e tipos.

gerador_arquivos.py: Orquestra a criação das pastas e a renderização dos templates.

templates/: Contém os moldes (.jinja2) para as Entidades, DAOs e Scripts de Exemplo.

main_gerador.py: Ponto de entrada via linha de comando para disparar o processo.

requirements.txt: Lista de dependências necessárias.

saida_gerada/: Diretório onde o código automatizado (Entidades, DAOs e Exemplos) será depositado.

Como Executar

Preparação do Ambiente:
Instale as dependências necessárias através do terminal:
Bash
pip install -r requirements.txt

Geração do Código:
Execute o script principal passando o caminho do banco de dados desejado:
Bash
python main_gerador.py bancos_teste/universidade.db
universidade.db pode ser substituído por qualquer outro db desejado.

Execução dos Exemplos:
O sistema criará automaticamente scripts de teste na pasta 
saida_gerada/dominio_banco/exemplos/. Estes arquivos utilizam dados 
aleatórios para validar o funcionamento do CRUD gerado.
Bash
python saida_gerada/dominio_banco/exemplos/clientes_exemplo.py
Esse comando testa a persistência da tabela Clientes

Funcionamento das Camadas

Extração: O sistema utiliza introspecção de metadados para mapear tipos 
SQL (como INTEGER e REAL) para tipos nativos do Python (int e float), 
aplicando inferência de tipos onde disponível.

Renderização: Através do Jinja2, o gerador injeta os metadados nos templates,
 criando classes que herdam automaticamente as bases genéricas da pasta 
infra/ do Trabalho 1.

Exemplos Dinâmicos: Conforme solicitado, os arquivos de exemplo geram dados
 aleatórios (Strings, Floats, Ints) para testar as operações de inserção, 
alteração e listagem sem intervenção manual.

Observações Acadêmicas
Este trabalho demonstra a aplicação prática de Metaprogramação e Geração 
Automática de Código. Ao utilizar o framework do Trabalho 1 como base, o 
gerador garante que o código produzido seja modular e compatível com a 
arquitetura de Injeção de Dependência já estabelecida. A ferramenta foi 
projetada para tratar as principais exceções de execução, garantindo 
robustez no processamento de diferentes esquemas de banco de dados.