import customtkinter as ctk
from components.editable_button import EditableButton
from components.autosave_text import AutoSaveText
from components.clipboard_button import ClipboardButton

class SelectableButtonItem(ctk.CTkFrame):  

    def __init__(self, master, note, title="Titulo", body="Escribir descripción", father=None, **kwargs):
        super().__init__(master, **kwargs)
        self.note = note
        #self.note_id = note_id
        self.title = title
        self.body = body 
        self.textbox = None
        self.father= father
        # Subframe superior
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", pady=0, ipady=0)
        self.top_frame.columnconfigure(1, weight=1)

        # Checkbox
        self.var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(
            self.top_frame,
            text="",              # sin texto
            variable=self.var,
            fg_color="#00A2FF",   # color de selección
            border_color="#808080",
            width=20,             # ancho controlado
            height=20,            # alto controlado
            corner_radius=3
        )
        self.checkbox.grid(row=0, column=0, padx=1, pady=0, sticky="w")

        # Botón principal
        self.button = EditableButton(self.top_frame, note_id=self.note.id, text=self.note.title, command=self.toggle_textbox,reset_cache=self.father.refresh_note_list, repo=self.father.repo)
        self.button.grid(row=0, column=1, padx=1, pady=0, sticky="ew")

        self.clipboard = ClipboardButton(self.top_frame, text=lambda: self.textbox.get() if self.textbox else self.note.body, content=self.father)
        self.clipboard.grid(row=0, column=2, padx=1, pady=0, sticky="e")

    def toggle_textbox(self,event=None):
        if not self.textbox:
            # 🔹 Crear solo al abrir
            self.textbox = AutoSaveText(self, note_id=self.note.id, body=self.note.body, reset_cache=self.father.refresh_note_list,repo=self.father.repo)

        if self.textbox.visible():
            self.textbox.hide()
        else:
            self.textbox.show()
            self.textbox.focus()


