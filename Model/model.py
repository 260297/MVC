class Estudante:
    def __init__(self, nome, nota1, nota2, nota3, nota4):
        self.nome = nome
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.nota4 = nota4
        self.media = (nota1 + nota2 + nota3 + nota4) / 4
