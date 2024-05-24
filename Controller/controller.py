import sqlite3
from Model.model import Estudante

class EstudanteController:
    def __init__(self, db_name="estudantes.db"):
        self.db_name = db_name
        self.conn = None

    def conectar(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)

    def fechar_conexao(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def criar_tabela(self):
        self.conectar()
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudantes (
            nome TEXT PRIMARY KEY,
            nota1 REAL,
            nota2 REAL,
            nota3 REAL,
            nota4 REAL,
            media REAL
        );
        """)
        self.conn.commit()
        self.fechar_conexao()

    def adicionar_estudante(self, nome, nota1, nota2, nota3, nota4):
        self.conectar()
        estudante = Estudante(nome, nota1, nota2, nota3, nota4)
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO estudantes (nome, nota1, nota2, nota3, nota4, media)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (estudante.nome, estudante.nota1, estudante.nota2, estudante.nota3, estudante.nota4, estudante.media))
        self.conn.commit()
        cursor.close()
        self.fechar_conexao()
        return estudante

    def buscar_estudante(self, nome):
        self.conectar()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM estudantes WHERE nome=?", (nome,))
        row = cursor.fetchone()
        self.fechar_conexao()
        if row:
            nome, nota1, nota2, nota3, nota4, media = row
            return Estudante(nome, nota1, nota2, nota3, nota4)

    def atualizar_estudante(self, nome, nota1, nota2, nota3, nota4):
        self.conectar()
        cursor = self.conn.cursor()
        media = (nota1 + nota2 + nota3 + nota4) / 4
        cursor.execute("""
        UPDATE estudantes
        SET nota1=?, nota2=?, nota3=?, nota4=?, media=?
        WHERE nome=?
        """, (nota1, nota2, nota3, nota4, media, nome))
        self.conn.commit()
        self.fechar_conexao()

    def excluir_estudante(self, nome):
        self.conectar()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM estudantes WHERE nome=?", (nome,))
        self.conn.commit()
        self.fechar_conexao()

    def listar_estudantes(self):
        self.conectar()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM estudantes")
        rows = cursor.fetchall()
        self.fechar_conexao()
        return [Estudante(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    

    def editar_estudante(self, nome_original, nome, nota1, nota2, nota3, nota4):
        self.conectar()
        # Se o nome foi alterado, precisamos atualizar o nome separadamente
        if nome != nome_original:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE estudantes SET nome=? WHERE nome=?", (nome, nome_original))
            self.conn.commit()
            cursor.close()
        
        # Atualizar notas e média
        media = (nota1 + nota2 + nota3 + nota4) / 4
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE estudantes
        SET nota1=?, nota2=?, nota3=?, nota4=?, media=?
        WHERE nome=?
        """, (nota1, nota2, nota3, nota4, media, nome))
        self.conn.commit()
        cursor.close()
        
        self.fechar_conexao()

        
