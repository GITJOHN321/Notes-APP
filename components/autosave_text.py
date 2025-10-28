import customtkinter as ctk
import controllers.notes_controller as con
from components.autoresize_textbox import AutoResizeTextbox

class AutoSaveText(ctk.CTkFrame):
    def __init__(self, master, note_id=None, body="escribe un texto", **kwargs):
        super().__init__(master, **kwargs)

        self.note_id = note_id
        self._contenido = body
        self.bottom_border = ctk.CTkFrame(self, height=2, fg_color="royalblue", corner_radius=0)
        self.bottom_border.pack(fill="x") # Make it fill the width
        self.textbox = AutoResizeTextbox(self)
        self.textbox.load_content(body)
        self.textbox.pack(fill="x", expand=True)

        #visible variable
        self._visible = False        

        # Variable para controlar el guardado
        self._after_id = None  # identificador del temporizador

        # Detectar cualquier cambio de teclado dentro del textbox
        self.textbox.bind("<Control-z>", lambda e: self.textbox.edit_undo())
        self.textbox.bind("<Control-y>", lambda e: self.textbox.edit_redo())
        self.textbox.bind("<KeyRelease>", self.on_edit)

    def on_edit(self, event=None):
        """Se ejecuta cada vez que el usuario edita el contenido."""
        # Cancelar cualquier guardado anterior programado
        if self._after_id is not None:
            self.after_cancel(self._after_id)

        # Programar guardado después de 1 segundo sin teclear
        self._after_id = self.after(1000, self.guardar_texto)

    def guardar_texto(self):
        #EDIT CONTROLLER
        
        contenido = self.textbox.get("1.0", "end-1c")
        con.edit_note(self.note_id,body=contenido)
        self._contenido = contenido
        print("Texto guardado automáticamente:")
        print(contenido)
        print("-----------")

        self._after_id = None  # reinicia el temporizador
    
    def get(self):
        print(self._contenido)
        return self._contenido
    
    def focus(self):
        self.textbox.focus_set()

    def show(self):
        self.pack(fill="x", padx=5, pady=(5, 0))
        self._visible = True

    def hide(self):
        self.pack_forget()
        self._visible = False

    def visible(self):
        return self._visible