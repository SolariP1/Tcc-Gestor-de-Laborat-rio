from tkinter import *
import customtkinter as ctk
from conecta import conectar_ao_banco
from auth_login import Login
from frames import Principal  

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1920x1080")  
        self.db, _ = conectar_ao_banco()
        self._frame = None
        self.switch_frame(Login)

    def switch_frame(self, frame_class):
        if self._frame is not None:
            self._frame.destroy()

        self._frame = frame_class(self)
        self._frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = MainApp()
    app.update_idletasks()  
    app.state("zoomed")  
    app.mainloop()
