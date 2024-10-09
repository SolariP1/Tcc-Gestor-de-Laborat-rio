import tkinter as tk
import os
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk  
from materiais import conectar_banco  

class VisualizarMateriais:
    def __init__(self, root):
        self.root = root
        self.root.title("Materiais Cadastrados")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0e0e0")

        message_frame = ttk.Frame(self.root, padding="10")
        message_frame.pack()
        message_label = ttk.Label(
            message_frame,
            text="Dê duplo clique no material desejado para excluí-lo.",
            font=("Helvetica", 12, "italic"),
            wraplength=750,
        )
        message_label.pack()

        border_frame = ttk.Frame(self.root, borderwidth=2, relief="solid")
        border_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.criar_tabela_materiais(border_frame)

    def criar_tabela_materiais(self, parent):
        columns = ("ID", "Nome", "Descrição", "Quantidade","Reserva")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Reserva", text="Reserva")
        self.tree.column("ID", width=50)
        self.tree.column("Quantidade", width=50)
        self.tree.column("Reserva", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.carregar_dados()

        self.tree.bind("<Double-1>", self.obter_material_selecionado)

        scrollbar_x = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    def carregar_dados(self):
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, descricao, quantidade, reserva_id FROM materiais")
        rows = cursor.fetchall()
        conexao.close()

        # Limpa a tabela antes de carregar os dados
        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def obter_material_selecionado(self, event):
        item = self.tree.selection()[0]
        material_id = self.tree.item(item, 'values')[0]
        self.editar_material(material_id)

    def editar_material(self, material_id):
        top = tk.Toplevel(self.root)
        top.title("Editar Material")
        top.geometry("600x400")
        top.configure(bg="#e0e0e0")

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM materiais WHERE id=?", (material_id,))
        material = cursor.fetchone()
        conexao.close()

        form_frame = ttk.Frame(top, padding="20")
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Nome").grid(row=0, column=0, sticky=tk.W, pady=5)
        nome_entry = ttk.Entry(form_frame, width=50)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        nome_entry.insert(0, material[1])

        ttk.Label(form_frame, text="Descrição").grid(row=1, column=0, sticky=tk.W, pady=5)


        ttk.Label(form_frame, text="Imagem").grid(row=2, column=0, sticky=tk.W, pady=5)
        img_label = ttk.Label(form_frame)
        img_label.grid(row=2, column=1, padx=5, pady=5)
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

        ttk.Label(form_frame, text="Reserva").grid(row=4, column=0, sticky=tk.W, pady=5)
        reserva_entry = ttk.Entry(form_frame, width=10)
        reserva_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        reserva_entry.insert(0, material[5])

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=1, columnspan=2, pady=10, sticky=tk.E)
        ttk.Button(
            button_frame, text="Excluir", style="Excluir.TButton", command=lambda: self.excluir_material(material[0], top)
        ).pack(side=tk.LEFT, padx=5)

    def exibir_imagem(self, file_path, label):
        img = Image.open(file_path)
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

    def selecionar_imagem_editar(self, label):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.exibir_imagem(file_path, label)

    def salvar_edicao(self, material_id, nome_entry, descricao_entry, img_label, quantidade_entry, top):
        nome = nome_entry.get()
        descricao = descricao_entry.get("1.0", tk.END).strip()
        quantidade = quantidade_entry.get()

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
            (nome, descricao, img_label.image, quantidade, material_id),
        )
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Edição", f"Material {nome} editado com sucesso!")
        top.destroy()
        self.carregar_dados()

    def excluir_material(self, material_id, top):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este material?"):
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM materiais WHERE id=?", (material_id,))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Exclusão", "Material excluído com sucesso!")
            top.destroy()
            self.carregar_dados()