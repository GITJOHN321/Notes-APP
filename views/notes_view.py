import customtkinter as ctk
import components.ctk_widgets as widget
from components.scrollframe import ScrollableFrame
from components.search_entry import SearchVar

from components.list_button import NotesButtonManager

class NotesView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)       
        
        # Diferir foco
        self.after(100, self.focus_set)

        # Atajos globales
        self.master.bind("<Control-f>", self.show_search)
        self.master.bind("<Escape>", self.hide_search)

        # Frame de controles
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=5)

        # Frame contenedor de ítems
        self.items_frame = ScrollableFrame(self, fg_color="transparent")
        self.items_frame.pack(pady=5, fill="both", expand=True)

        self.manager = NotesButtonManager(self.items_frame)

        # Botones
        self.sync_button = widget.button_control(self.control_frame, text="\uf2f1 Sync")
        self.sync_button.pack(side="left", padx=2)

        self.add_button = widget.button_control(self.control_frame, text="\uf067 Add", command=self.manager.add_item)
        self.add_button.pack(side="left", padx=2)

        self.delete_button = widget.button_control(self.control_frame, text="\uf1f8 Del", command=self.manager.delete_selected)
        self.delete_button.pack(side="left", padx=2)

        self.search_button = widget.button_control(self.control_frame, text="\uf002", command=self.show_search)
        self.search_button.pack(side="left", padx=2)


        # Diferir render inicial de notas
        self.after(50, lambda: self.manager.render_notes(self.manager.refresh_note_list()))
        
        # Campo de búsqueda
        self.search_var = SearchVar(self, search=self.filter_notes)

    def show_search(self, event=None):
        if self.search_var.visible():
            self.search_var.hide()
        else:
            self.search_var.show()

    def hide_search(self, event=None):
        if self.search_var.visible():
            self.search_var.hide()

    def filter_notes(self, *args):
        """Filtra las notas y oculta las que no coinciden con la búsqueda."""
        query = self.search_var.get().strip().lower()
        self.manager.filter_notes(query)
