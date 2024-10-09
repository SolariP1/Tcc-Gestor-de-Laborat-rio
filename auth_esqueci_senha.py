import customtkinter as ctk
from conecta import conectar_ao_banco
from auth_login import Login
from utilidades import contar_espacos, contar_letras
import mysql.connector
import random
import string
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO)

class EsqueciSenha(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.fontePadrao = ctk.CTkFont(size=12)
        self.verification_code = None
        self.email = None
        self.create_widgets()

    def create_widgets(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=20, fill='both', expand=True)

        self.frame_labels = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_labels.pack(side="left", fill="both", expand=True)

        self.frame_botoes = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_botoes.pack(side="right", fill="both", expand=True)

        self.titulo = ctk.CTkLabel(self.frame_labels, text="Redefinir Senha", font=ctk.CTkFont(size=30, weight="bold"), fg_color="transparent")
        self.titulo.pack(pady=(180, 20), anchor="w", padx=(80, 0))

        self.emailLabel = ctk.CTkLabel(self.frame_labels, text="E-mail")
        self.emailLabel.pack(pady=(0, 5), padx=(0, 10))
        self.emailEntry = ctk.CTkEntry(self.frame_labels, width=250, border_width=1)
        self.emailEntry.pack(pady=(0, 10), padx=(0, 10))

        self.codeLabel = ctk.CTkLabel(self.frame_labels, text="Código de Verificação")
        self.codeLabel.pack(pady=(0, 5), padx=(0, 10))
        self.codeEntry = ctk.CTkEntry(self.frame_labels, width=250, border_width=1)
        self.codeEntry.pack(pady=(0, 10), padx=(0, 10))

        self.novaSenhaLabel = ctk.CTkLabel(self.frame_labels, text="Nova Senha", font=self.fontePadrao, fg_color="transparent", anchor="w")
        self.novaSenhaLabel.pack(pady=(0, 5), padx=(0, 10))
        self.novaSenha = ctk.CTkEntry(self.frame_labels, width=250, show="*", border_width=1)
        self.novaSenha.pack(pady=(0, 10), padx=(0, 10))

        self.confirmarSenhaLabel = ctk.CTkLabel(self.frame_labels, text="Confirmar Nova Senha", font=self.fontePadrao, fg_color="transparent", anchor="w")
        self.confirmarSenhaLabel.pack(pady=(0, 5), padx=(0, 10))
        self.confirmarSenha = ctk.CTkEntry(self.frame_labels, width=250, show="*", border_width=1)
        self.confirmarSenha.pack(pady=(0, 10), padx=(0, 10))

        self.botaoEnviarCodigo = ctk.CTkButton(self.frame_botoes, text="Enviar Código", command=self.enviar_codigo)
        self.botaoEnviarCodigo.pack(pady=(270, 5), padx=(10, 0))

        self.botaoVerificar = ctk.CTkButton(self.frame_botoes, text="Verificar", command=self.verificar_codigo)
        self.botaoVerificar.pack(pady=(0, 5), padx=(10, 0))

        self.botaoRedefinir = ctk.CTkButton(self.frame_botoes, text="Redefinir", command=self.redefinir_senha)
        self.botaoRedefinir.pack(pady=(0, 5), padx=(10, 0))

        self.botaoVoltar = ctk.CTkButton(self.frame_botoes, text="Voltar", command=self.retorno)
        self.botaoVoltar.pack(pady=(0, 10), padx=(10, 0))

        self.mensagem = ctk.CTkLabel(self.frame_botoes, text="", font=self.fontePadrao, fg_color="transparent")
        self.mensagem.pack(pady=(10, 0))

    def enviar_codigo(self):
        self.email = self.emailEntry.get()
        
        if not self.email:
            self.mensagem.configure(text="Por favor, insira um e-mail.")
            return

        try:
            cursor = self.master.db.cursor()
            cursor.execute("SELECT usu_email FROM usuario WHERE usu_email = %s", (self.email,))
            resultado = cursor.fetchone()

            if resultado:
                self.verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if self.enviar_email(self.email, self.verification_code):  # Usando smtplib
                    self.mensagem.configure(text="Código de verificação enviado para o e-mail.")
                else:
                    self.mensagem.configure(text="Erro ao enviar e-mail. Por favor, tente novamente.")
            else:
                self.mensagem.configure(text="E-mail não encontrado no banco de dados.")
        except mysql.connector.Error as err:
            self.mensagem.configure(text=f"Erro ao verificar o e-mail: {err}")
            logging.error(f"Erro no banco de dados: {err}")
        finally:
            cursor.close()

    def enviar_email(self, destinatario, codigo):
        remetente = 'tccsesisenai@gmail.com'  
        senha = 'qaajwknbyyolgctk' 

        # Criação da mensagem
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = 'Código de Verificação para Redefinição de Senha'

        # Corpo HTML do e-mail
        corpo_email = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Código de Verificação</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                    color: #333;
                }}
                .container {{
                    background-color: #fff;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #fff;
                    background-color: #4CAF50;
                }}
                .codigo {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #fff;
                    background-color: #4CAF50;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    display: inline-block;
                }}
                p {{
                    margin: 15px 0;
                }}
                footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Código de Verificação</h1>
                <p>Olá,</p>
                <p>Você solicitou a redefinição de sua senha. Para prosseguir, utilize o seguinte código de verificação:</p>
                <div class="codigo">{codigo}</div>
                <p>Se você não solicitou essa redefinição, por favor, inão responda esse e-mail.</p>
                <footer>
                    <p>Obrigado!</p>
                </footer>
            </div>
        </body>
        </html>
        """

        mensagem.attach(MIMEText(corpo_email, 'html'))  # Alterado para 'html'

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.starttls()  # Conexão segura
                servidor.login(remetente, senha)  # Login no servidor
                servidor.send_message(mensagem)  # Envio da mensagem
            logging.info(f"E-mail enviado com sucesso para {destinatario}")
            return True
        except Exception as e:
            logging.error(f"Erro ao enviar e-mail: {e}")
            return False

    def verificar_codigo(self):
        codigo_inserido = self.codeEntry.get()
        if codigo_inserido == self.verification_code:
            self.mensagem.configure(text="Código verificado. Você pode redefinir sua senha agora.")
        else:
            self.mensagem.configure(text="Código incorreto.")

    def redefinir_senha(self):
        if not self.verification_code or self.codeEntry.get() != self.verification_code:
            self.mensagem.configure(text="Por favor, verifique o código primeiro.")
            return

        nova_senha = self.novaSenha.get()
        confirmar_senha = self.confirmarSenha.get()

        if nova_senha != confirmar_senha:
            self.mensagem.configure(text="As senhas não coincidem.")
            return

        espaco = contar_espacos(nova_senha)
        quantidade = contar_letras(nova_senha)

        if espaco > 0 or quantidade < 8:
            self.mensagem.configure(text="A senha deve ter pelo menos 8 caracteres e não deve conter espaços.")
            return

        cursor = self.master.db.cursor()
        try:
            cursor.execute("UPDATE usuario SET usu_senha = %s WHERE usu_email = %s", (nova_senha, self.email))
            self.master.db.commit()
            self.mensagem.configure(text="Senha redefinida com sucesso.")
            self.master.switch_frame(Login)
        except mysql.connector.Error as err:
            self.mensagem.configure(text=f"Erro ao redefinir senha: {err}")

    def retorno(self):
        self.master.switch_frame(Login)
