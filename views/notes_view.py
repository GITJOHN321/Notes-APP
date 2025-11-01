import customtkinter as ctk
import components.ctk_widgets as widget
from components.selectable_button import SelectableButtonItem
from components.scrollframe import ScrollableFrame
from components.search_entry import SearchVar
from repositories.note_repository import NoteRepository

class NotesView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Repositorio (puede tardar)
        self.repo = NoteRepository()
        self.note_list = self.repo.get_all()

        # Diferir foco
        self.after(100, self.focus_set)

        # Atajos globales
        self.master.bind("<Control-f>", self.show_search)
        self.master.bind("<Escape>", self.hide_search)

        # Lista de botones/ítems
        self.items = []

        # Frame de controles
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=5)

        # Botones
        self.sync_button = widget.button_control(self.control_frame, text="🗘 Sync")
        self.sync_button.pack(side="left", padx=2)

        self.add_button = widget.button_control(self.control_frame, text="✚ add", command=self.add_item)
        self.add_button.pack(side="left", padx=2)

        self.delete_button = widget.button_control(self.control_frame, text="🗑 del", command=self.delete_selected)
        self.delete_button.pack(side="left", padx=2)

        self.search_button = widget.button_control(self.control_frame, text="🔍︎", command=self.show_search)
        self.search_button.pack(side="left", padx=2)

        # Frame contenedor de ítems
        self.items_frame = ScrollableFrame(self, fg_color="transparent")
        self.items_frame.pack(pady=5, fill="both", expand=True)

        # Diferir render inicial de notas
        self.after(50, lambda: self.render_notes(self.note_list))

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

    def render_notes(self, notes):
        # Limpiar solo si es necesario
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        self.items.clear()
        for note in notes:
            self.add_item(new_note=note)

    def add_item(self, new_note=None, title="Nueva nota", body="Escribe una descripción"):
        if not new_note:
            new_note = self.repo.add(title, body)
            self.refresh_note_list()
        note = SelectableButtonItem(self.items_frame, note=new_note, father=self)
        self.items.append(note)
        note.pack(pady=0, fill="x", padx=5)
        #Forzar el render
        self.update_idletasks()

    def delete_selected(self):
        try:
            to_remove = [i for i in self.items if i.var.get()]
            if not to_remove:
                return
            note_ids = [i.note.id for i in to_remove if i.note.id]
            if note_ids:
                self.repo.delete_many_notes(note_ids)
                self.refresh_note_list()
            for i in to_remove:
                i.destroy()
                self.items.remove(i)
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")

    def filter_notes(self, *args):
        query = self.search_var.get()
        if not query:
            notas_filtradas = self.note_list
        else:
            notas_filtradas = [
                n for n in self.note_list
                if query in n.title.lower() or query in n.body.lower()
            ]
        self.render_notes(notas_filtradas)

    def refresh_note_list(self):
        self.note_list = self.repo.get_all()
        return self.note_list
