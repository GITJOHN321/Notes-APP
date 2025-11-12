import customtkinter as ctk
import components.ctk_widgets as widget
from components.selectable_button import SelectableButtonItem
from components.scrollframe import ScrollableFrame
from components.search_entry import SearchVar

from controllers.note_controller import NoteController

class NotesView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Controlador
        self.con = NoteController()
        
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

        # Frame contenedor de ítems
        self.items_frame = ScrollableFrame(self, fg_color="transparent")
        self.items_frame.pack(pady=5, fill="both", expand=True)

        # Botones
        self.sync_button = widget.button_control(self.control_frame, text="\uf2f1 Sync")
        self.sync_button.pack(side="left", padx=2)

        self.add_button = widget.button_control(self.control_frame, text="\uf067 Add", command=self.add_item)
        self.add_button.pack(side="left", padx=2)

        self.delete_button = widget.button_control(self.control_frame, text="\uf1f8 Del", command=self.delete_selected)
        self.delete_button.pack(side="left", padx=2)

        self.search_button = widget.button_control(self.control_frame, text="\uf002", command=self.show_search)
        self.search_button.pack(side="left", padx=2)

        

        # Diferir render inicial de notas
        self.after(50, lambda: self.render_notes(self.refresh_note_list()))
        
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

    def render_notes(self, notes, batch_size=20):
        """Renderiza las notas en lotes para evitar bloquear la interfaz."""
        # Limpiar solo si es necesario
        if not self.items:
            for widget in self.items_frame.winfo_children():
                widget.destroy()

        self.items.clear()

        # Convertir lista a iterador para cargar por partes
        notes_iter = iter(notes)
        self._render_batch(notes_iter, batch_size)

    def _render_batch(self, notes_iter, batch_size):
        """Carga los botones en pequeños lotes para mantener la UI fluida."""
        for _ in range(batch_size):
            try:
                note = next(notes_iter)
            except StopIteration:
                return  # Ya se renderizaron todas

            self.add_item(new_note=note)

        # Esperar 10 ms y continuar con el siguiente lote
        self.after(10, lambda: self._render_batch(notes_iter, batch_size))

    def add_item(self, new_note=None, title="Nueva nota", body="Escribe una descripción"):
        if not new_note:
            new_note = self.con.add_note(title,body)
        note = SelectableButtonItem(self.items_frame, note=new_note, update=self.con.update, toast_father=self)
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
                self.con.remove_notes(note_ids)
            for i in to_remove:
                i.destroy()
                self.items.remove(i)
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")

    def filter_notes(self, *args):
        """Filtra las notas y oculta las que no coinciden con la búsqueda."""
        query = self.search_var.get().strip().lower()

        # Si no hay texto, mostrar todas
        if not query:
            filtered_ids = {n.id for n in self.refresh_note_list()}
        else:
            filtered_notes = [
                n for n in self.refresh_note_list()
                if query in n.title.lower() or query in n.body.lower()
            ]
            filtered_ids = {n.id for n in filtered_notes}

        self.render_filter(filtered_ids)


    def refresh_note_list(self):
        return self.con.get_notes()
        
    def render_filter(self, filtered_ids=None):
        """
        Muestra u oculta los botones según el filtro actual.
        Si filtered_ids es None o vacío, muestra todos.
        """
        for btn in self.items:
            note_id = btn.note.id
            if not filtered_ids or note_id in filtered_ids:
                # Mostrar si no está visible
                if not btn.winfo_ismapped():
                    btn.pack(pady=0, fill="x", padx=5)
            else:
                # Ocultar si no cumple filtro
                if btn.winfo_ismapped():
                    btn.pack_forget()

        self.update_idletasks()
