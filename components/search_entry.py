import customtkinter as ctk

class SearchVar(ctk.CTkFrame):
    def __init__(self, master, search=None):
        super().__init__(master)
        self.search = search
        self.search_delay = None

        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(5, 0), pady=5)

        # Botón cerrar
        self.close_button = ctk.CTkButton(self, text="\uf00d", font=("Font Awesome 5 Pro Solid", 14), width=30, command=self.hide)
        self.close_button.grid(row=0, column=1, padx=5, pady=5)

        self.grid_columnconfigure(0, weight=1)

        # Diferir focus y trace para acelerar render inicial
        self.after(100, self.search_entry.focus_set)
        self.after(150, lambda: self.search_var.trace("w", self.on_search_change))

    def on_search_change(self, *args):
        if self.search_delay is not None:
            self.after_cancel(self.search_delay)
        self.search_delay = self.after(300, self.search)

    def get(self):
        return self.search_var.get().lower().strip()

    def show(self):
        self.pack(side="left", padx=2, expand=True)
        self.after(100, self.search_entry.focus_set)

    def hide(self):
        if self.search_var.get():
            self.search_var.set("")
        self.pack_forget()

    def visible(self):
        return bool(self.winfo_ismapped())

        
    
    