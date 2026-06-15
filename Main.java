import java.util.ArrayList;
import java.util.List;

// Interface Iterator
interface Iterator<T> {
    boolean hasNext();
    T next();
}

// Interface Aggregate (coleção iterável)
interface IterableCollection<T> {
    Iterator<T> createIterator();
}

// Elemento concreto
class Aluno {
    private String nome;
    private double nota;

    public Aluno(String nome, double nota) {
        this.nome = nome;
        this.nota = nota;
    }

    public String getNome() { return nome; }
    public double getNota() { return nota; }

    @Override
    public String toString() {
        return nome + " - Nota: " + nota;
    }
}

// Coleção concreta
class Turma implements IterableCollection<Aluno> {
    private List<Aluno> alunos = new ArrayList<>();

    public void adicionarAluno(Aluno aluno) {
        alunos.add(aluno);
    }

    public int getTamanho() {
        return alunos.size();
    }

    public Aluno getAluno(int index) {
        return alunos.get(index);
    }

    @Override
    public Iterator<Aluno> createIterator() {
        return new TurmaIterator(this);
    }
}

// Iterador concreto
class TurmaIterator implements Iterator<Aluno> {
    private Turma turma;
    private int posicaoAtual = 0;

    public TurmaIterator(Turma turma) {
        this.turma = turma;
    }

    @Override
    public boolean hasNext() {
        return posicaoAtual < turma.getTamanho();
    }

    @Override
    public Aluno next() {
        Aluno aluno = turma.getAluno(posicaoAtual);
        posicaoAtual++;
        return aluno;
    }
}

// Classe principal (cliente)
public class Main {
    public static void main(String[] args) {
        Turma turma = new Turma();
        turma.adicionarAluno(new Aluno("Marcos", 9.5));
        turma.adicionarAluno(new Aluno("Ana", 8.0));
        turma.adicionarAluno(new Aluno("Pedro", 7.2));

        Iterator<Aluno> iterator = turma.createIterator();

        System.out.println("Lista de alunos da turma:");
        while (iterator.hasNext()) {
            Aluno aluno = iterator.next();
            System.out.println(aluno);
        }
    }
}
