import tkinter as tk
from tkinter import ttk, messagebox
from Controller.controller import EstudanteController

class EstudanteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Estudantes")
        self.controller = EstudanteController()
        self.controller.criar_tabela()

        # Interface
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Nome:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.frame, text="Nota 1:").grid(row=1, column=0)
        self.entry_nota1 = tk.Entry(self.frame)
        self.entry_nota1.grid(row=1, column=1)

        tk.Label(self.frame, text="Nota 2:").grid(row=2, column=0)
        self.entry_nota2 = tk.Entry(self.frame)
        self.entry_nota2.grid(row=2, column=1)

        tk.Label(self.frame, text="Nota 3:").grid(row=3, column=0)
        self.entry_nota3 = tk.Entry(self.frame)
        self.entry_nota3.grid(row=3, column=1)

        tk.Label(self.frame, text="Nota 4:").grid(row=4, column=0)
        self.entry_nota4 = tk.Entry(self.frame)
        self.entry_nota4.grid(row=4, column=1)

        self.button_adicionar = tk.Button(self.frame, text="Adicionar Estudante", command=self.adicionar_estudante)
        self.button_adicionar.grid(row=5, columnspan=2)

        self.tree = ttk.Treeview(root, columns=("nome", "nota1", "nota2", "nota3", "nota4", "media"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("nota1", text="Nota 1")
        self.tree.heading("nota2", text="Nota 2")
        self.tree.heading("nota3", text="Nota 3")
        self.tree.heading("nota4", text="Nota 4")
        self.tree.heading("media", text="Média")
        self.tree.pack(padx=10, pady=10)

        self.button_listar = tk.Button(root, text="Listar Estudantes", command=self.listar_estudantes)
        self.button_listar.pack(pady=10)

        self.button_delete = tk.Button(root, text="Deletar Estudante", command=self.deletar_estudante)
        self.button_delete.pack(pady=10)

        self.tree.bind("<Double-1>", self.editar_estudante)


    
    def adicionar_estudante(self):
        def ler_nota(nota_str):
            try:
                nota = float(nota_str)
                if 0 <= nota <= 10:
                    return nota
                else:
                    raise ValueError("Nota fora do intervalo válido")
            except ValueError:
                
                return None
        nome = self.entry_nome.get()
        nota1_str = self.entry_nota1.get()
        nota2_str = self.entry_nota2.get()
        nota3_str = self.entry_nota3.get()
        nota4_str = self.entry_nota4.get()

        if not nome or not nota1_str or not nota2_str or not nota3_str or not nota4_str:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        nota1 = ler_nota(nota1_str)
        nota2 = ler_nota(nota2_str)
        nota3 = ler_nota(nota3_str)
        nota4 = ler_nota(nota4_str)

        if nota1 is None or nota2 is None or nota3 is None or nota4 is None:
            messagebox.showerror("Erro", "As notas devem ser números válidos entre 0 e 10.")
            return

        estudante = self.controller.adicionar_estudante(nome, nota1, nota2, nota3, nota4)
        messagebox.showinfo("Sucesso", f"Estudante {estudante.nome} adicionado com sucesso!")

        self.entry_nome.delete(0, tk.END)
        self.entry_nota1.delete(0, tk.END)
        self.entry_nota2.delete(0, tk.END)
        self.entry_nota3.delete(0, tk.END)
        self.entry_nota4.delete(0, tk.END)

        # Definindo o foco de volta para o campo de nome
        self.entry_nome.focus()

        self.listar_estudantes()

    def listar_estudantes(self):
        self.tree.delete(*self.tree.get_children())
        estudantes = self.controller.listar_estudantes()
        for estudante in estudantes:
            self.tree.insert("", tk.END, values=(estudante.nome, estudante.nota1, estudante.nota2, estudante.nota3, estudante.nota4, estudante.media))

    def deletar_estudante(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum estudante selecionado.")
            return

        nome = self.tree.item(selected_item, 'values')[0]
        self.controller.excluir_estudante(nome)
        self.listar_estudantes()
        messagebox.showinfo("Sucesso", f"Estudante {nome} deletado com sucesso!")

    def editar_estudante(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        nome = self.tree.item(selected_item, 'values')[0]
        estudante = self.controller.buscar_estudante(nome)

        if estudante:
            self.abrir_janela_edicao(estudante)


    def abrir_janela_edicao(self, estudante):
        self.edicao_window = tk.Toplevel(self.root)
        self.edicao_window.title("Editar Estudante")

        tk.Label(self.edicao_window, text="Nome:").grid(row=0, column=0)
        self.edicao_nome = tk.Entry(self.edicao_window)
        self.edicao_nome.grid(row=0, column=1)
        self.edicao_nome.insert(0, estudante.nome)

        tk.Label(self.edicao_window, text="Nota 1:").grid(row=1, column=0)
        self.edicao_nota1 = tk.Entry(self.edicao_window)
        self.edicao_nota1.grid(row=1, column=1)
        self.edicao_nota1.insert(0, estudante.nota1)

        tk.Label(self.edicao_window, text="Nota 2:").grid(row=2, column=0)
        self.edicao_nota2 = tk.Entry(self.edicao_window)
        self.edicao_nota2.grid(row=2, column=1)
        self.edicao_nota2.insert(0, estudante.nota2)

        tk.Label(self.edicao_window, text="Nota 3:").grid(row=3, column=0)
        self.edicao_nota3 = tk.Entry(self.edicao_window)
        self.edicao_nota3.grid(row=3, column=1)
        self.edicao_nota3.insert(0, estudante.nota3)

        tk.Label(self.edicao_window, text="Nota 4:").grid(row=4, column=0)
        self.edicao_nota4 = tk.Entry(self.edicao_window)
        self.edicao_nota4.grid(row=4, column=1)
        self.edicao_nota4.insert(0, estudante.nota4)

        self.button_salvar_edicao = tk.Button(self.edicao_window, text="Salvar", command=lambda: self.salvar_edicao(estudante.nome))
        self.button_salvar_edicao.grid(row=5, columnspan=2)

    def salvar_edicao(self, nome_original):
        nome = self.edicao_nome.get()
        nota1 = self.edicao_nota1.get()
        nota2 = self.edicao_nota2.get()
        nota3 = self.edicao_nota3.get()
        nota4 = self.edicao_nota4.get()

        if not nome or not nota1 or not nota2 or not nota3 or not nota4:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            nota1 = float(nota1)
            nota2 = float(nota2)
            nota3 = float(nota3)
            nota4 = float(nota4)
        except ValueError:
            messagebox.showerror("Erro", "As notas devem ser números válidos.")
            return

        self.controller.conectar()  # Abrir conexão com o banco de dados

        # Atualizar notas, media e nome (se alterado) no banco de dados
        self.controller.editar_estudante(nome_original, nome, nota1, nota2, nota3, nota4)
                
        messagebox.showinfo("Sucesso", f"Estudante {nome_original} atualizado com sucesso!")

        self.edicao_window.destroy()
        self.listar_estudantes()


    

if __name__ == "__main__":
    root = tk.Tk()
    app = EstudanteGUI(root)
    root.mainloop()
