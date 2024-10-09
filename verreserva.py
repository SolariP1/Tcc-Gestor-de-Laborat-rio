import tkinter as tk
from tkinter import ttk
import sqlite3

# Variável global para controlar a instância da janela de reservas
ver_reservas_window = None

class VerReservasWindow(tk.Toplevel):
    def __init__(self, parent, usuario_atual):
        super().__init__(parent)
        self.title("Visualizar Reservas")
        self.geometry("800x600")
        self.usuario_atual = usuario_atual

        # Fechar a janela de maneira customizada
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Configurar o estilo da Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", 
                        fieldbackground="white", foreground="black")
        style.configure("Treeview.Heading", background="lightgray", 
                        foreground="black", relief="raised")

        # Criar um frame para conter a Treeview e a scrollbar
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Criar a Treeview
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Usuário", "Laboratório", "Horário Inicial", "Horário Final", "Data"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.heading("Laboratório", text="Laboratório")
        self.tree.heading("Horário Inicial", text="Horário Inicial")
        self.tree.heading("Horário Final", text="Horário Final")
        self.tree.heading("Data", text="Data")

        # Configurar as colunas
        self.tree.column("ID", width=50)
        self.tree.column("Usuário", width=150)
        self.tree.column("Laboratório", width=100)
        self.tree.column("Horário Inicial", width=100)
        self.tree.column("Horário Final", width=100)
        self.tree.column("Data", width=100)

        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Posicionar a Treeview e a scrollbar
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botão para alternar entre todas as reservas e reservas do usuário
        self.toggle_button = ttk.Button(self, text="Mostrar Todas as Reservas", command=self.toggle_view)
        self.toggle_button.pack(pady=10)

        # Variável para controlar o modo de visualização
        self.show_all = False

        # Carregar os dados inicialmente
        self.load_reservas()

    def load_reservas(self):
        # Abrir conexão com o banco de dados
        conn = sqlite3.connect('reservas3.db')
        cursor = conn.cursor()

        # Limpar a Treeview antes de carregar novos dados
        self.tree.delete(*self.tree.get_children())  

        # Consulta SQL baseada no modo de visualização atual
        if self.show_all:
            cursor.execute('SELECT * FROM reservas')
            print("Carregando todas as reservas")
        else:
            cursor.execute('SELECT * FROM reservas WHERE usuario = ?', (self.usuario_atual,))
            print(f"Carregando reservas para o usuário: {self.usuario_atual}")

        rows = cursor.fetchall()
        print(f"Número de reservas encontradas: {len(rows)}")

        # Inserir os dados na Treeview
        for row in rows:
            self.tree.insert("", tk.END, values=row)
            print(f"Inserindo linha: {row}")

        # Fechar a conexão com o banco de dados
        conn.close()

    def toggle_view(self):
        # Alterna o modo de visualização entre "todas as reservas" e "minhas reservas"
        self.show_all = not self.show_all
        if self.show_all:
            self.toggle_button.config(text="Esconder Todas as Reservas")
        else:
            self.toggle_button.config(text="Mostrar Todas as Reservas")
        
        # Carregar as reservas novamente com base no modo atual
        self.load_reservas()

    def on_close(self):
        global ver_reservas_window
        ver_reservas_window = None
        self.destroy()

def open_ver_reservas_window(parent, usuario_atual):
    global ver_reservas_window
    if ver_reservas_window is None:
        ver_reservas_window = VerReservasWindow(parent, usuario_atual)
    else:
        ver_reservas_window.lift()  # Traz a janela existente para a frente