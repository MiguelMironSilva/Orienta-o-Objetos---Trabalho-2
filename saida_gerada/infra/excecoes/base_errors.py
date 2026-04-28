# framework_universidade/infra/excecoes/base_errors.py

class FrameworkError(Exception):
    """
    Exceção base para todo o framework 'infra'.
    Todas as outras exceções customizadas devem herdar desta classe.
    
    Vantagem: Permite que um desenvolvedor lá na aplicação faça um 
    'except FrameworkError' para capturar qualquer falha originada 
    dentro do nosso mini-framework.
    """
    pass


class RegistroNaoEncontradoError(FrameworkError):
    """
    Lançada pela camada de Dados (DAO) ou de Negócios (Gerenciadores) 
    quando uma busca por chave primária ou filtro não retorna resultados.
    """
    def __init__(self, mensagem: str = "O registro solicitado não foi encontrado no sistema."):
        self.mensagem = mensagem
        # Repassa a mensagem para a classe Exception original do Python
        super().__init__(self.mensagem)


class ErroDeValidacao(FrameworkError):
    """
    Lançada EXCLUSIVAMENTE pela camada de Negócios (Gerenciadores) 
    quando um objeto (ex: Aluno) tenta ser salvo, mas quebra alguma 
    regra de negócio (ex: Nome muito curto, Data no futuro, etc).
    """
    def __init__(self, mensagem: str = "Os dados fornecidos violam uma regra de negócio."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)