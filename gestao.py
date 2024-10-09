import customtkinter as ctk
import sqlite3
from PIL import Image, ImageTk
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def conectar_banco():
    return sqlite3.connect('materiais.db')

def criar_tabela_materiais():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        imagem TEXT,
        quantidade INTEGER,
        em_uso INTEGER DEFAULT 0  -- Adicionando a coluna em_uso
    )
    ''')
    conexao.commit()
    conexao.close()

def atualizar_status_uso(material_id, em_uso):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("UPDATE materiais SET em_uso = ? WHERE id = ?", (em_uso, material_id))
    conexao.commit()
    conexao.close()

class MaterialUsageManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Uso de Materiais")
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self.main_frame, text="Gerenciador de Uso de Materiais", font=("Helvetica", 20))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.materials_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.materials_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        self.refresh_button = ctk.CTkButton(self.main_frame, text="Atualizar Lista", command=self.load_materials)
        self.refresh_button.grid(row=2, column=0, padx=20, pady=(0, 20))

        self.load_materials()

    def load_materials(self):
        for widget in self.materials_frame.winfo_children():
            widget.destroy()

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, descricao, imagem, quantidade, em_uso FROM materiais")
        materials = cursor.fetchall()
        conexao.close()

        for material in materials:
            self.create_material_card(material)

    def create_material_card(self, material):
        material_id, nome, descricao, imagem, quantidade, em_uso = material
        em_uso = bool(em_uso)  # Convert to boolean

        card = ctk.CTkFrame(self.materials_frame)
        card.pack(padx=10, pady=10, fill="x")

        # Image
        if imagem and os.path.exists(imagem):
            img = Image.open(imagem)
            img.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(card, image=photo, text="")
            img_label.image = photo
            img_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        else:
            img_label = ctk.CTkLabel(card, text="Sem\nimagem", width=100, height=100)
            img_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        # Material info
        name_label = ctk.CTkLabel(card, text=nome, font=("Helvetica", 16, "bold"))
        name_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))

        desc_label = ctk.CTkLabel(card, text=descricao[:50] + "..." if len(descricao) > 50 else descricao)
        desc_label.grid(row=1, column=1, sticky="w", padx=10)

        quantity_label = ctk.CTkLabel(card, text=f"Quantidade: {quantidade}")
        quantity_label.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))

        # Usage status
        usage_var = ctk.StringVar(value="Em uso" if em_uso else "Disponível")
        usage_switch = ctk.CTkSwitch(card, text="Status", variable=usage_var, 
                                     onvalue="Em uso", offvalue="Disponível",
                                     command=lambda: self.toggle_usage(material_id, usage_var))
        usage_switch.grid(row=1, column=2, padx=10, pady=10)
        usage_switch.select() if em_uso else usage_switch.deselect()

    def toggle_usage(self, material_id, usage_var):
        em_uso = usage_var.get() == "Em uso"
        atualizar_status_uso(material_id, em_uso)

if __name__ == "__main__":
    criar_tabela_materiais()  # Chama a função para criar a tabela
    app = MaterialUsageManager()
    app.mainloop()
