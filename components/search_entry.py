import customtkinter as ctk

class SearchVar(ctk.CTkFrame):
    def __init__(self, master, search=None):
        super().__init__(master)

        self.search=search

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var)
        self.search_entry.pack(side="left",fill="x", padx=(5,0), pady=5)
        self.search_delay = None  # para almacenar el temporizador activo
        self.search_var.trace("w", self.on_search_change)  # Detecta cambios en tiempo real   

        # Botón Cerrar
        self.close_button = ctk.CTkButton(self, text="✖", width=30, command= self.hide)
        self.close_button.pack(side="left", padx=5, pady=5)

        # Enfocar el campo
        self.search_entry.focus()

        #visible variable
        self._visible = False

    def on_search_change(self, *args):
        # Si ya hay un temporizador corriendo, lo cancela
        if self.search_delay is not None:
            self.after_cancel(self.search_delay)

        # Inicia un nuevo temporizador (1000 ms = 1 segundo)
        self.search_delay = self.after(300, self.search)

    def get(self):
        print(self.search_var.get().lower().strip())
        return self.search_var.get().lower().strip()   

    def show(self):
        self.pack(side="left", padx=2, expand=True)
        self._visible = True
        self.search_entry.focus()

    def hide(self):
        content = self.search_var.get().lower().strip()
        if content:
            self.search_var.set("")
        self.pack_forget()
        self._visible = False

    def visible(self):
        return self._visible
        
    
    