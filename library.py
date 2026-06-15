class Livro:
    """Elemento concreto: representa um item da coleção."""

    def __init__(self, titulo: str, autor: str):
        self.titulo = titulo
        self.autor = autor

    def __repr__(self):
        return f"{self.titulo} - {self.autor}"


class Biblioteca:
    """
    Coleção concreta (Aggregate).

    Implementa __iter__, que retorna um iterador (BibliotecaIterator).
    Isso é o equivalente ao método createIterator() do Java.
    """

    def __init__(self):
        self._livros = []

    def adicionar_livro(self, livro: Livro):
        self._livros.append(livro)

    def __iter__(self):
        return BibliotecaIterator(self._livros)


class BibliotecaIterator:
    """
    Iterador concreto (ConcreteIterator).

    Implementa __next__ e __iter__ para seguir o protocolo de
    iteração do Python (também chamado de "iterator protocol").
    """

    def __init__(self, livros: list):
        self._livros = livros
        self._posicao_atual = 0

    def __iter__(self):
        # Um iterador deve retornar a si mesmo quando __iter__ é chamado
        return self

    def __next__(self):
        if self._posicao_atual >= len(self._livros):
            raise StopIteration  # sinaliza o fim da iteração

        livro = self._livros[self._posicao_atual]
        self._posicao_atual += 1
        return livro

class BibliotecaComGenerator:
    def __init__(self):
        self._livros = []

    def adicionar_livro(self, livro: Livro):
        self._livros.append(livro)

    def __iter__(self):
        for livro in self._livros:
            yield livro


# Código cliente
if __name__ == "__main__":
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro(Livro("Clean Code", "Robert C. Martin"))
    biblioteca.adicionar_livro(Livro("Design Patterns", "GoF"))
    biblioteca.adicionar_livro(Livro("Refactoring", "Martin Fowler"))

    print("Livros da biblioteca (ConcreteIterator manual):")
    for livro in biblioteca:
        print(livro)

    print("\nLivros da biblioteca (usando generator/yield):")
    biblioteca2 = BibliotecaComGenerator()
    biblioteca2.adicionar_livro(Livro("The Pragmatic Programmer", "Hunt & Thomas"))
    biblioteca2.adicionar_livro(Livro("Effective Java", "Joshua Bloch"))

    for livro in biblioteca2:
        print(livro)
