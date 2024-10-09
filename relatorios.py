import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class RelatoriosMateriais:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.create_relatorios_window()

    def create_relatorios_window(self):
        self.parent_window.title("Relatórios de Materiais")
        self.parent_window.geometry("300x200")

        frame = ttk.Frame(self.parent_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        generate_pdf_btn = ttk.Button(frame, text="Gerar Relatório PDF", command=self.generate_pdf)
        generate_pdf_btn.pack(pady=20)

    def generate_pdf(self):
        try:
            conn = sqlite3.connect('materiais.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, descricao, quantidade, reserva_id FROM materiais WHERE is_hidden = 0")
            materials = cursor.fetchall()
            conn.close()

            pdf_file = "relatorio_materiais.pdf"
            doc = SimpleDocTemplate(pdf_file, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            elements.append(Paragraph("Relatório de Materiais", styles['Title']))
            elements.append(Paragraph(" ", styles['Normal'])) 

            data = [["ID", "Nome", "Descrição", "Quantidade", "Reserva"]]
            for material in materials:
                data.append(material)

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(table)
            doc.build(elements)

            messagebox.showinfo("PDF Gerado", f"O relatório foi gerado com sucesso: {pdf_file}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF: {str(e)}")