import customtkinter as ctk
import components.ctk_widgets as widget

class EditableButton(ctk.CTkFrame):
    def __init__(self, master, note=None, command=None,update=None,**kwargs):
        super().__init__(master, **kwargs)
        self.update = update
        self.text = note.title
        self.note = note
        self._command = command
        self._cancelled = False
        self.button = widget.button_note(self, self.text, self.on_click)
        self.button.pack(fill="both", expand=True)

        # Detectar doble clic para editar
        self.button.bind("<Double-Button-1>", self.start_edit)

        # Campo de texto oculto inicialmente
        self.entry = ctk.CTkEntry(self)
        self.entry.bind("<Escape>", self.cancel_edit)
        self.entry.bind("<Return>", self.save_text)
        self.entry.bind("<FocusOut>", self.save_text)
        

    def on_click(self):
        print(f"Hiciste clic en: {self.text}")
        if self._command:
            self._command()

    def start_edit(self, event=None):
        self._cancelled = False
        self.entry.delete(0, "end")
        self.entry.insert(0, self.text)
        self.button.pack_forget()
        self.entry.pack(fill="both", expand=True)
        self.entry.focus_set()

    def save_text(self, event=None):
        if self._cancelled:
            self._cancelled = False
            self.return_to_button()
            return

        new_text = self.entry.get().strip()
        if new_text:
            #EDIT CONTROLLER
            self.note.title= new_text
            self.update(self.note)
            self.text = new_text
            self.button.configure(text=self.text)
        self.return_to_button()
        self._cancelled = True
    
    def cancel_edit(self, event=None):
        self._cancelled = True
        self.return_to_button()
        print("Edición cancelada")
    
    def return_to_button(self):
        """Oculta el campo de texto y muestra el botón."""
        self.entry.pack_forget()
        self.button.pack(fill="both", expand=True)   