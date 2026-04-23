# framework_universidade/infra/entidades/registro.py

from abc import ABC, abstractmethod

class Registro(ABC):
    """
    Interface/Classe Base Abstrata para todas as entidades do sistema.
    Garante que qualquer classe que herde de Registro (como Aluno ou Curso) 
    implemente obrigatoriamente o método para retornar seu rótulo de exibição.
    """

    @abstractmethod
    def get_rotulo(self) -> str:
        """
        Retorna uma representação em texto amigável do registro.
        
        No Java legado, as listas e menus precisavam desse método para 
        saber o que escrever na tela (ex: o nome do Aluno ou o título do Livro).
        """
        pass