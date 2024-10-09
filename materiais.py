import tkinter as tk
from tkinter import ttk, filedialog, Text, messagebox
from PIL import ImageTk, Image
import sqlite3
import os

def criar_tabela():
    conexao = sqlite3.connect('materiais.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materiais (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            descricao TEXT,
            imagem TEXT,
            quantidade INTEGER,
            reserva_id INTEGER,
            is_hidden INTEGER DEFAULT 0
        )
    ''')
    conexao.commit()
    conexao.close()

criar_tabela()

def conectar_banco():
    return sqlite3.connect('materiais.db')

class CadastroMateriais:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Materiais")
        self.root.geometry("800x550") 

        self.img_path = ""
        self.reserva_id = None
        main_frame = ttk.Frame(root)
        main_frame.pack(expand=True)

        # Borda
        border_frame = ttk.Frame(main_frame, borderwidth=2, relief="solid")
        border_frame.pack(padx=10, pady=10)

        # Header
        header_frame = ttk.Frame(border_frame)
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Cadastro de Materiais").pack(
            side=tk.LEFT, padx=10, pady=10
        )
        ttk.Button(header_frame, text="Voltar", command=self.voltar).pack(
            side=tk.RIGHT, padx=10, pady=10
        )

        # Formulário
        self.criar_formulario(border_frame)

    def criar_formulario(self, parent):
        form_frame = ttk.Frame(parent, padding="20 10 20 10")
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Nome").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Descrição").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.descricao_entry = Text(form_frame, width=50, height=5, wrap=tk.WORD)
        self.descricao_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Imagem").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.img_label = ttk.Label(form_frame)
        self.img_label.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(form_frame, text="Selecionar Imagem", command=self.selecionar_imagem).grid(
            row=2, column=2, padx=5, pady=5
        )

        ttk.Label(form_frame, text="Quantidade").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.quantidade_entry = ttk.Entry(form_frame, width=10)
        self.quantidade_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # New button for associating with a reservation
        ttk.Button(form_frame, text="Associar à Reserva", command=self.associar_reserva).grid(
            row=4, column=1, pady=5, sticky=tk.W
        )
        self.reserva_label = ttk.Label(form_frame, text="Nenhuma reserva selecionada")
        self.reserva_label.grid(row=4, column=1, padx=(150, 0), pady=5, sticky=tk.W)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=1, columnspan=2, pady=10, sticky=tk.E)
        ttk.Button(button_frame, text="Cadastrar", command=self.cadastrar).pack(side=tk.LEFT, padx=5)

    def associar_reserva(self):
        # This method will open a new window to select a reservation
        self.abrir_janela_selecao_reserva()

    def abrir_janela_selecao_reserva(self):
        top = tk.Toplevel(self.root)
        top.title("Selecionar Reserva")
        top.geometry("600x400")

        # Create a treeview to display reservations
        columns = ("ID", "Usuário", "Laboratório", "Data")
        tree = ttk.Treeview(top, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Fetch reservations from the database
        conexao = sqlite3.connect('reservas3.db')  # Make sure this is the correct database file
        cursor = conexao.cursor()
        cursor.execute("SELECT id, usuario, laboratorio, data_reserva FROM reservas")
        reservas = cursor.fetchall()
        conexao.close()

        # Populate the treeview
        for reserva in reservas:
            tree.insert("", tk.END, values=reserva)

        # Bind double-click event
        tree.bind("<Double-1>", lambda event: self.selecionar_reserva(event, top))

    def selecionar_reserva(self, event, window):
        selected_item = event.widget.selection()[0]
        reserva = event.widget.item(selected_item, 'values')
        self.reserva_id = reserva[0]
        self.reserva_label.config(text=f"Reserva selecionada: ID {self.reserva_id}")
        window.destroy()

    def voltar(self):
        self.root.destroy() 

    def selecionar_imagem(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.exibir_imagem(file_path, self.img_label)
            self.img_path = file_path

    def exibir_imagem(self, file_path, label):
        img = Image.open(file_path)
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

    def cadastrar(self):
        nome = self.nome_entry.get().strip()
        descricao = self.descricao_entry.get("1.0", tk.END).strip()
        quantidade = self.quantidade_entry.get().strip()

        if not nome or not descricao or not quantidade:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            quantidade = int(quantidade)
            if quantidade < 0:
                raise ValueError("A quantidade não pode ser negativa.")
        except ValueError as e:
            messagebox.showerror("Erro", f"Quantidade inválida: {str(e)}")
            return

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO materiais (nome, descricao, imagem, quantidade, reserva_id) VALUES (?, ?, ?, ?, ?)",
                (nome, descricao, self.img_path, quantidade, self.reserva_id)
            )
            conexao.commit()
            messagebox.showinfo("Cadastro", f"Material '{nome}' cadastrado com sucesso!")
            self.limpar_formulario()
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro ao cadastrar o material: {str(e)}")
        finally:
            if conexao:
                conexao.close()

    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
        self.descricao_entry.delete("1.0", tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.img_label.config(image="")
        self.img_path = ""

    def visualizar(self):
        top = tk.Toplevel(self.root)
        top.title("Materiais Cadastrados")
        top.geometry("800x600")

        message_frame = ttk.Frame(top, padding="10")
        message_frame.pack()
        message_label = ttk.Label(
            message_frame,
            text="Dê duplo clique no material desejado para editá-lo ou ocultá-lo.",
            font=("Helvetica", 12, "italic"),
            wraplength=750,
        )
        message_label.pack()

        border_frame = ttk.Frame(top, borderwidth=2, relief="solid")
        border_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = self.criar_tabela_materiais(border_frame)

    
    def criar_tabela_materiais(self, parent):
        columns = ("ID", "Nome", "Descrição", "Quantidade")
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Quantidade", text="Quantidade")
        tree.column("ID", width=50)
        tree.column("Quantidade", width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, descricao, quantidade FROM materiais WHERE is_hidden = 0")
        rows = cursor.fetchall()
        conexao.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.bind("<Double-1>", self.obter_material_selecionado)

        scrollbar_x = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y = tk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)


    def obter_material_selecionado(self, event):
        try:
            selected_item = event.widget.selection()[0]
            selected_id = event.widget.item(selected_item, 'values')[0]
            self.editar_material(selected_id)
        except IndexError:
            pass
        
    def editar_material(self, material_id):
        top = tk.Toplevel(self.root)
        top.title("Editar Material")
        top.geometry("600x400")

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM materiais WHERE id=?", (material_id,))
        material = cursor.fetchone()
        conexao.close()

        if material:
            self.criar_formulario_edicao(top, material)

    def criar_formulario_edicao(self, parent, material):
        form_frame = ttk.Frame(parent, padding="20 10 20 10")
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Nome").grid(row=0, column=0, sticky=tk.W, pady=5)
        nome_entry = ttk.Entry(form_frame, width=50)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        nome_entry.insert(0, material[1])

        ttk.Label(form_frame, text="Descrição").grid(row=1, column=0, sticky=tk.W, pady=5)
        descricao_entry = Text(form_frame, width=50, height=5, wrap=tk.WORD)
        descricao_entry.grid(row=1, column=1, padx=5, pady=5)
        descricao_entry.insert("1.0", material[2])

        ttk.Label(form_frame, text="Imagem").grid(row=2, column=0, sticky=tk.W, pady=5)
        img_label = ttk.Label(form_frame)
        img_label.grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        img_path = material[3] if material[3] and os.path.exists(material[3]) else ""
        if img_path:
            self.exibir_imagem(img_path, img_label)
        ttk.Button(
            form_frame, text="Selecionar Imagem", command=lambda: self.selecionar_imagem_editar(img_label)
        ).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(form_frame, text="Quantidade").grid(row=3, column=0, sticky=tk.W, pady=5)
        quantidade_entry = ttk.Entry(form_frame, width=10)
        quantidade_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        quantidade_entry.insert(0, material[4])

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=1, columnspan=2, pady=10, sticky=tk.E)
        ttk.Button(
            button_frame, text="Salvar", command=lambda: self.salvar_edicao(material[0], nome_entry, descricao_entry, img_path, quantidade_entry, parent)
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Excluir", style="Excluir.TButton", command=lambda: self.excluir_material(material[0], parent)
        ).pack(side=tk.LEFT, padx=5)

    def selecionar_imagem_editar(self, img_label):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.exibir_imagem(file_path, img_label)
            self.img_path = file_path

    def salvar_edicao(self, material_id, nome_entry, descricao_entry, img_path, quantidade_entry, parent):
        nome = nome_entry.get()
        descricao = descricao_entry.get("1.0", tk.END).strip()
        quantidade = quantidade_entry.get()
        imagem = self.img_path

        if not nome or not descricao or not quantidade:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
            return

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE materiais SET nome=?, descricao=?, imagem=?, quantidade=? WHERE id=?",
            (nome, descricao, imagem, quantidade, material_id),
        )
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Editar", f"Material {nome} editado com sucesso!")
        parent.destroy()

    def excluir_material(self, material_id, parent):
        if messagebox.askyesno("Confirmação", "Deseja realmente ocultar este material?"):
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("UPDATE materiais SET is_hidden = 1 WHERE id=?", (material_id,))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Ocultar", "Material ocultado com sucesso!")
            parent.destroy()
            self.atualizar_visualizacao()

    def atualizar_visualizacao(self):
        # This method should be called after hiding a material to refresh the view
        if hasattr(self, 'tree'):
            self.tree.delete(*self.tree.get_children())
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, descricao, quantidade FROM materiais WHERE is_hidden = 0")
            rows = cursor.fetchall()
            conexao.close()
            for row in rows:
                self.tree.insert("", tk.END, values=row)