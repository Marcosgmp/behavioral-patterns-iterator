# Padrão Iterator - Trabalho de Engenharia de Software

## 1. Introdução

O **Iterator** é um padrão de projeto **comportamental** (behavioral pattern), catalogado pelo GoF (Gang of Four). Seu objetivo é fornecer uma forma de acessar sequencialmente os elementos de uma coleção (lista, árvore, conjunto etc.) sem expor sua estrutura interna de implementação.

## 2. Problema que resolve

Coleções de dados (listas, arrays, mapas, árvores) possuem estruturas internas diferentes. Se o código cliente precisar percorrer essas estruturas diretamente, ele fica fortemente acoplado aos detalhes de implementação de cada coleção — qualquer mudança na estrutura interna quebraria o código cliente.

O Iterator resolve isso ao:

- Extrair a lógica de travessia (percurso) para um objeto separado, o **iterador**.
- Permitir percorrer a coleção sem conhecer sua representação interna (array, lista encadeada, árvore etc.).
- Permitir múltiplas formas de percurso (ordem direta, reversa, por filtro) sem alterar a coleção.
- Permitir percorrer a mesma coleção simultaneamente por diferentes iteradores, cada um mantendo seu próprio estado.

## 3. Estrutura do padrão

| Elemento | Papel |
|---|---|
| **Iterator** (interface) | Define os métodos que todo iterador concreto deve implementar, normalmente `hasNext()` e `next()`. |
| **ConcreteIterator** | Implementa a interface Iterator e mantém o controle da posição atual do percurso na coleção. |
| **Aggregate / IterableCollection** (interface) | Define o método `createIterator()`, que retorna um novo iterador para a coleção. |
| **ConcreteAggregate** | Implementa a interface Aggregate, armazenando os elementos e fornecendo acesso a eles através do iterador. |

## 4. Exemplos de código

Este repositório contém dois exemplos equivalentes do padrão Iterator, em linguagens diferentes:

- `java/Main.java` — Turma de alunos
- `python/biblioteca.py` — Biblioteca de livros

### 4.1 Exemplo em Java (`java/Main.java`)

Implementa o padrão de forma **clássica/explícita**, com interfaces próprias:

- `Iterator<T>` — interface com `hasNext()` e `next()`
- `IterableCollection<T>` — interface com `createIterator()`
- `Turma` — coleção concreta (ConcreteAggregate)
- `TurmaIterator` — iterador concreto (ConcreteIterator)
- `Aluno` — elemento armazenado na coleção

**Como funciona:**

1. A classe `Turma` armazena uma lista de objetos `Aluno`.
2. Ao chamar `turma.createIterator()`, é criado um novo `TurmaIterator`, que guarda referência à turma e a posição atual (`posicaoAtual = 0`).
3. `hasNext()` verifica se ainda há elementos a percorrer.
4. `next()` retorna o elemento atual e avança a posição.
5. O cliente (`Main`) usa um `while` controlado por `hasNext()`/`next()`, sem acessar diretamente a lista interna.

**Saída esperada:**
```
Lista de alunos da turma:
Marcos - Nota: 9.5
Ana - Nota: 8.0
Pedro - Nota: 7.2
```

### 4.2 Exemplo em Python (`python/biblioteca.py`)

Implementa o padrão usando o **protocolo de iteração nativo do Python**, baseado em métodos especiais (dunder methods):

- `__iter__(self)` → retorna o objeto iterador (equivalente a `createIterator()`)
- `__next__(self)` → retorna o próximo elemento ou lança `StopIteration` (equivalente a `next()`/`hasNext()` combinados)

Classes:

- `Livro` — elemento da coleção
- `Biblioteca` — coleção concreta, implementa `__iter__`
- `BibliotecaIterator` — iterador concreto, implementa `__iter__` e `__next__`
- `BibliotecaComGenerator` — implementação alternativa usando `yield` (generator)

**Como funciona:**

1. A classe `Biblioteca` armazena uma lista de objetos `Livro`.
2. Ao usar `for livro in biblioteca`, o Python chama automaticamente `biblioteca.__iter__()`, que retorna um `BibliotecaIterator`.
3. A cada iteração do `for`, o Python chama `__next__()` no iterador.
4. Quando não há mais elementos, `__next__()` lança `StopIteration`, e o `for` encerra automaticamente.
5. A classe `BibliotecaComGenerator` mostra a forma idiomática alternativa: com `yield`, o Python cria o iterador automaticamente, sem precisar de uma classe `Iterator` separada.

**Saída esperada:**
```
Livros da biblioteca (ConcreteIterator manual):
Clean Code - Robert C. Martin
Design Patterns - GoF
Refactoring - Martin Fowler

Livros da biblioteca (usando generator/yield):
The Pragmatic Programmer - Hunt & Thomas
Effective Java - Joshua Bloch
```

## 5. Diferenças entre as implementações Java e Python

| Aspecto | Java | Python |
|---|---|---|
| **Interfaces explícitas** | Necessárias (`Iterator<T>`, `IterableCollection<T>`) — o padrão é implementado "do zero" pelo programador. | Não são necessárias. O próprio Python já define um "protocolo de iteração" (`__iter__`/`__next__`) reconhecido pela linguagem. |
| **Criação do iterador** | Método explícito `createIterator()` na coleção. | Método especial `__iter__()`, chamado automaticamente pelo `for`. |
| **Verificação de fim da coleção** | Método separado `hasNext()` retorna `boolean`. | Não existe `hasNext()`; o fim é sinalizado lançando a exceção `StopIteration` dentro de `__next__()`. |
| **Uso pelo cliente** | Laço `while` manual combinando `hasNext()` e `next()`. | Laço `for ... in ...` direto — a linguagem gerencia a chamada de `__next__()` e o tratamento de `StopIteration`. |
| **Iterador como objeto separado** | Sempre uma classe própria (`TurmaIterator`). | Pode ser uma classe própria (`BibliotecaIterator`) **ou** uma função geradora com `yield` (`BibliotecaComGenerator`), que o interpretador transforma automaticamente em um iterador. |
| **Verbosidade** | Mais verboso: exige declarar duas interfaces e duas classes concretas. | Mais conciso: o protocolo já é parte da linguagem, e o `yield` reduz ainda mais o código necessário. |
| **Onde mais aparece** | `java.util.Iterator`, usado por todas as coleções (`List`, `Set`, `Map`) e pelo `for-each`. | Qualquer objeto iterável (`list`, `dict`, `set`, arquivos, generators) segue o mesmo protocolo `__iter__`/`__next__`. |

### Conclusão da comparação

A **ideia central do padrão é a mesma** nas duas linguagens: separar a lógica de percurso da estrutura de dados, permitindo percorrer uma coleção sem conhecer sua implementação interna. A diferença está em **quanto da estrutura do padrão já vem embutida na linguagem**:

- Em **Java**, o programador precisa modelar explicitamente as interfaces `Iterator` e `Aggregate` (ou implementar `java.util.Iterator` e `Iterable` para integrar com o `for-each`).
- Em **Python**, esse "contrato" já existe na linguagem através dos métodos especiais `__iter__`/`__next__`, tornando a implementação mais curta e permitindo até substituir a classe iteradora por uma simples função `yield`.

## 6. Vantagens do padrão

- **Encapsulamento**: a estrutura interna da coleção fica escondida do cliente.
- **Responsabilidade única**: a lógica de percurso fica isolada em uma classe (ou função) própria.
- **Suporte a múltiplos percursos**: é possível criar diferentes tipos de iteradores (reverso, filtrado) sem alterar a coleção original.
- **Iteração simultânea independente**: cada iterador mantém seu próprio estado, permitindo múltiplos percursos paralelos sobre a mesma coleção.
- **Interface uniforme**: qualquer coleção que siga o protocolo (interface em Java, dunder methods em Python) pode ser percorrida da mesma forma.

## 7. Aplicações reais

- **Java**: `java.util.Iterator`, usado por `List`, `Set`, `Map` e pelo `for-each`.
- **Python**: protocolo `__iter__`/`__next__`, usado por `list`, `dict`, `set`, arquivos e generators.
- **C#**: interfaces `IEnumerable`/`IEnumerator`, com suporte ao `foreach`.

## 8. Conclusão

O Iterator é fundamental para promover baixo acoplamento entre coleções e o código que as utiliza. Comparando as implementações em Java e Python, fica claro que o padrão pode ser tanto **explícito** (Java, exigindo interfaces e classes próprias) quanto **embutido na linguagem** (Python, via protocolo de iteração), mas em ambos os casos a ideia fundamental — separar "o que é percorrido" de "como é percorrido" — permanece a mesma.
