import tkinter as Tkinter
import calendar
import time
from tkinter import messagebox
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter as tk  
import sqlite3

selected_day = ''

def criarbanco():
    conn = sqlite3.connect('reservas3.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            laboratorio TEXT,
            horario_inicial TEXT,
            horario_final TEXT,
            data_reserva TEXT
        )
    ''')
    conn.commit()
    conn.close()

criarbanco()

def print_database_contents():
    # Conectar ao banco de dados
    conn = sqlite3.connect('reservas3.db')
    cursor = conn.cursor()
    
    # Executar uma consulta para selecionar todos os registros
    cursor.execute('SELECT * FROM reservas')
    rows = cursor.fetchall()
    
    # Imprimir os registros
    print("ID | Usuário | Laboratório | Horário Inicial | Horário Final | Data da Reserva")
    print("---------------------------------------------------------------------------")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
    
    # Fechar a conexão
    conn.close()

# Chamar a função para imprimir os dados
print_database_contents()

class CalendarApp:
    def __init__(self, root, usuario_atual):
        self.root = root
        self.usuario_atual = usuario_atual  # Armazene o usuário atual
        self.root.title("Calendar")
        self.root.minsize(200, 200)
        self.root.maxsize(500, 500)

        self.segoe = tkFont.Font(family='Segoe UI')
        self.curtime = time.localtime()
        self.yearInt = self.curtime[0]
        self.monthInt = self.curtime[1]
        self.dateInt = self.curtime[2]

        # Adicionando self.year e self.month como StringVar de tkinter
        self.year = tk.StringVar(value=str(self.yearInt))
        self.month = tk.StringVar(value=str(self.monthInt))

        self.HLayout = ttk.PanedWindow(self.root, orient=Tkinter.HORIZONTAL)
        self.ctx = Tkinter.Text(self.root, padx=10, pady=10, bg="#f3e9ae", relief=Tkinter.FLAT, height=9, width=20)

        self.create_widgets()
        self.update_calendar()

        print(f"Usuário atual na CalendarApp: {self.usuario_atual}")

        self.consultar_nome_usuario()

    def consultar_nome_usuario(self):
        from conecta import conectar_ao_banco
        conn, cursor = conectar_ao_banco()

        if conn is None or cursor is None:
            print("Não foi possível conectar ao banco de dados.")
            return None
        
        try:
            cursor.execute('SELECT usu_nome FROM usuario WHERE usu_usuario = %s', (self.usuario_atual,))
            result = cursor.fetchone()

            if result:
                usuario_nome = result[0]
                return usuario_nome
            else:
                print("Usuário não encontrado")
                return None
        
        finally:
            conn.close()

    def create_widgets(self):
        prev = ttk.Button(self.HLayout, text="<<", command=self.prevb)
        nex = ttk.Button(self.HLayout, text=">>", command=self.nextb)
        goto = ttk.Button(self.root, text="Goto", command=self.gotod)
        mark = ttk.Button(self.root, text="Marcar", command=self.open_mark_window)

        menubar = Tkinter.Menu(self.root, relief=Tkinter.FLAT)
        filemenu = Tkinter.Menu(menubar, tearoff=0, relief=Tkinter.FLAT)
        helpmenu = Tkinter.Menu(menubar, tearoff=0, relief=Tkinter.FLAT)

        filemenu.add_command(label="Goto", command=self.gotod)
        filemenu.add_command(label="Ver Reservas", command=self.open_ver_reservas_window)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)
        helpmenu.add_command(label="About", command=self.about_show)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

        prev.pack(side=Tkinter.LEFT)
        nex.pack(side=Tkinter.RIGHT)
        self.ctx.pack()
        self.HLayout.pack()
        goto.pack()
        mark.pack(pady=10)

    def update_calendar(self, selected_date=None):
        calstr = calendar.month(self.yearInt, self.monthInt)
        self.ctx.configure(state=Tkinter.NORMAL)
        self.ctx.delete('0.0', Tkinter.END)
        self.ctx.insert(Tkinter.INSERT, calstr)

        # Obter os dias reservados no mês atual
        dias_reservados = self.get_reserved_days(self.yearInt, self.monthInt)

        for i in range(2, 9):
            line_start = f'{i}.0'
            line_end = f'{i}.end'
            self.ctx.tag_add("others", line_start, line_end)
            line_text = self.ctx.get(line_start, line_end)
            if len(line_text) == 20:
                self.ctx.tag_add("sun", f'{i}.end-2c', line_end)

            for day in range(1, 32):
                day_str = f"{day:2}"
                index = self.ctx.search(day_str, line_start)
                if index:
                    self.ctx.tag_add(f"day_{day}", index, f"{index}+2c")
                    self.ctx.tag_bind(f"day_{day}", "<Button-1>", lambda e, d=day: self.select_day(d))

                    # Destacar os dias que têm reservas
                    if day in dias_reservados:
                        self.ctx.tag_add(f"reserved_{day}", index, f"{index}+2c")
                        self.ctx.tag_config(f"reserved_{day}", background="red", foreground="white")

        self.ctx.tag_config("sun", foreground="#fb4622")
        self.ctx.tag_config("others", foreground="#427eb5")
        self.ctx.tag_add("head", '1.0', '1.end')

        if selected_date:
            index = self.ctx.search(f"{selected_date:2}", '2.0')
            if index:
                self.ctx.tag_add("selected", index, f"{index}+2c")
                self.ctx.tag_config("selected", background="blue", foreground="white")
        else:
            if self.curtime[0] == self.yearInt and self.curtime[1] == self.monthInt:
                index = self.ctx.search(str(self.curtime[2]), '2.0')
                self.ctx.tag_add("cur", index, f"{index}+2c")
                self.ctx.tag_config("cur", background="blue", foreground="white")

        self.ctx.tag_config("head", font=self.segoe, foreground="#0d8241", justify=Tkinter.CENTER)
        self.ctx.configure(state=Tkinter.DISABLED)

    def get_reserved_days(self, year, month):
        # Consultar o banco de dados para obter os dias reservados
        conn = sqlite3.connect('reservas3.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT strftime('%d', data_reserva) FROM reservas
            WHERE strftime('%Y', data_reserva) = ? AND strftime('%m', data_reserva) = ?
        ''', (str(year), f"{month:02d}"))

        rows = cursor.fetchall()
        conn.close()

        # Extrair os dias como inteiros e retornar
        return [int(row[0]) for row in rows]

    def select_day(self, day):
        global selected_day
        self.ctx.tag_remove("selected", "1.0", Tkinter.END)
        selected_day = f"{self.yearInt}-{self.monthInt:02d}-{day:02d}"
        print(selected_day)
        self.update_calendar(selected_date=day)

    def open_mark_window(self):
        def validate_selection():
            start_time = combo_start.get()
            end_time = combo_end.get()
            lab = combo_labs.get()
            usuario = self.consultar_nome_usuario()

            print(selected_day)

            if start_time and end_time:
                start_hour, start_minute = map(int, start_time.split(":"))
                end_hour, end_minute = map(int, end_time.split(":"))
                if end_hour < start_hour or (end_hour == start_hour and end_minute <= start_minute):
                    messagebox.showerror("Erro", "O horário final não pode ser menor ou igual ao horário inicial.")
                else:
                    conn = sqlite3.connect('reservas3.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                        SELECT horario_inicial, horario_final FROM reservas 
                        WHERE laboratorio = ? AND data_reserva = ?
                    ''', (lab, selected_day))

                    horarios_ocupados = cursor.fetchall()
                    conflito = False
                    for h_inicial, h_final in horarios_ocupados:
                        h_inicial_hora, h_inicial_min = map(int, h_inicial.split(":"))
                        h_final_hora, h_final_min = map(int, h_final.split(":"))

                        if not (end_hour < h_inicial_hora or (end_hour == h_inicial_hora and end_minute <= h_inicial_min) or
                                (start_hour > h_final_hora or (start_hour == h_final_hora and start_minute >= h_final_min))):
                            conflito = True
                            break

                    if conflito:
                        messagebox.showerror("Erro", "Horário já reservado!")
                    else:
                        cursor.execute('''
                            INSERT INTO reservas (usuario, laboratorio, horario_inicial, horario_final, data_reserva)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (usuario, lab, start_time, end_time, selected_day))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Sucesso", "Reserva efetuada com sucesso!")
                        mark_window.destroy()
            else:
                messagebox.showerror("Erro", "Selecione horários válidos.")

        mark_window = Tkinter.Toplevel(self.root)
        mark_window.title("Marcar Horário")
        mark_window.geometry("300x200")

        frame = ttk.Frame(mark_window, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")

        label_start = ttk.Label(frame, text="Horário Inicial:")
        label_start.grid(row=0, column=0, sticky="w")

        combo_start = ttk.Combobox(frame, values=[f"{hour:02d}:00" for hour in range(7, 23)])
        combo_start.grid(row=0, column=1, sticky="ew")

        label_end = ttk.Label(frame, text="Horário Final:")
        label_end.grid(row=1, column=0, sticky="w")

        combo_end = ttk.Combobox(frame, values=[f"{hour:02d}:00" for hour in range(7, 23)])
        combo_end.grid(row=1, column=1, sticky="ew")

        label_lab = ttk.Label(frame, text="Laboratório:")
        label_lab.grid(row=2, column=0, sticky="w")

        combo_labs = ttk.Combobox(frame, values=["Automação 01", "Automação 02", "Quimica 01", "Informática 01", "Informática 02", "Informática 03", "Informática 04"])
        combo_labs.grid(row=2, column=1, sticky="ew")

        button_mark = ttk.Button(frame, text="Marcar", command=validate_selection)
        button_mark.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        frame.columnconfigure(1, weight=1)
        mark_window.transient(self.root)
        mark_window.grab_set()
        self.root.wait_window(mark_window)

    def prevb(self):
        self.monthInt -= 1
        if self.monthInt == 0:
            self.monthInt = 12
            self.yearInt -= 1
        self.update_calendar()

    def nextb(self):
        self.monthInt += 1
        if self.monthInt == 13:
            self.monthInt = 1
            self.yearInt += 1
        self.update_calendar()

    def gotod(self):
        goto_window = Tkinter.Toplevel(self.root)
        goto_window.title("Goto Date")

        frame = ttk.Frame(goto_window, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")

        label_year = ttk.Label(frame, text="Year:")
        label_year.grid(row=0, column=0, sticky="w")

        entry_year = ttk.Entry(frame, textvariable=self.year)
        entry_year.grid(row=0, column=1, sticky="ew")

        label_month = ttk.Label(frame, text="Month:")
        label_month.grid(row=1, column=0, sticky="w")

        entry_month = ttk.Entry(frame, textvariable=self.month)
        entry_month.grid(row=1, column=1, sticky="ew")

        button_go = ttk.Button(frame, text="Go", command=lambda: self.goto_date(entry_year.get(), entry_month.get(), goto_window))
        button_go.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        frame.columnconfigure(1, weight=1)
        goto_window.transient(self.root)
        goto_window.grab_set()
        self.root.wait_window(goto_window)

    def goto_date(self, year, month, window):
        try:
            year_int = int(year)
            month_int = int(month)
            if 1 <= month_int <= 12:
                self.yearInt = year_int
                self.monthInt = month_int
                self.update_calendar()
                window.destroy()
            else:
                messagebox.showerror("Erro", "Mês inválido. Deve ser entre 1 e 12.")
        except ValueError:
            messagebox.showerror("Erro", "Ano e mês devem ser números inteiros válidos.")

    def about_show(self):
        messagebox.showinfo("Sobre", "Aplicativo de Reservas v1.0\nDesenvolvido por OpenAI")

    def open_ver_reservas_window(self):
        VerReservasWindow(self.root)

class VerReservasWindow(Tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Visualizar Reservas")
        self.geometry("600x400")

        # Criar a Treeview para exibir as reservas
        self.tree = ttk.Treeview(self, columns=("ID", "Usuário", "Laboratório", "Horário Inicial", "Horário Final", "Data"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.heading("Laboratório", text="Laboratório")
        self.tree.heading("Horário Inicial", text="Horário Inicial")
        self.tree.heading("Horário Final", text="Horário Final")
        self.tree.heading("Data", text="Data")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botão para excluir a reserva selecionada
        self.btn_delete = ttk.Button(self, text="Excluir Reserva", command=self.delete_reserva)
        self.btn_delete.pack(pady=10)

        self.load_reservas()

    def load_reservas(self):
        # Limpar a treeview antes de carregar os dados
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Carregar as reservas do banco de dados
        conn = sqlite3.connect('reservas3.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM reservas')
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def delete_reserva(self):
        # Obter o item selecionado
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma reserva para excluir.")
            return

        # Obter o ID da reserva selecionada
        reserva_id = self.tree.item(selected_item, 'values')[0]

        # Confirmar a exclusão
        confirm = messagebox.askyesno("Confirmar", "Você tem certeza que deseja excluir esta reserva?")
        
        if confirm:
            # Conectar ao banco de dados e excluir a reserva
            conn = sqlite3.connect('reservas3.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM reservas WHERE id = ?', (reserva_id,))
            conn.commit()
            conn.close()

            # Remover o item da Treeview
            self.tree.delete(selected_item)

            messagebox.showinfo("Sucesso", "Reserva excluída com sucesso!")