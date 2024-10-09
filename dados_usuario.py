
import customtkinter as ctk
from conecta import conectar_ao_banco

class DadosUsuario(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.db, _ = conectar_ao_banco()
        
        self.titulo = ctk.CTkLabel(self, text="Dados da Conta", font=ctk.CTkFont(size=20, weight="bold"))
        self.titulo.pack(pady=20)

        self.carregar_dados()

        self.botaoFechar = ctk.CTkButton(self, text="Fechar", command=self.master.destroy)
        self.botaoFechar.pack(pady=10)

    def carregar_dados(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT usu_nome, usu_email, usu_cpf, usu_cidade FROM usuario WHERE usu_usuario = %s", (self.usuario,))
        dados = cursor.fetchone()

        if dados:
            nome, email, cpf, cidade = dados
            ctk.CTkLabel(self, text=f"Nome: {nome}").pack(pady=5)
            ctk.CTkLabel(self, text=f"E-mail: {email}").pack(pady=5)
            ctk.CTkLabel(self, text=f"CPF: {cpf}").pack(pady=5)
            ctk.CTkLabel(self, text=f"Cidade: {cidade}").pack(pady=5)
        else:
            ctk.CTkLabel(self, text="Usuário não encontrado.").pack(pady=5)
