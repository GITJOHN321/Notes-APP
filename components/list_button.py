import customtkinter as ctk
from components.selectable_button import SelectableButtonItem
from controllers.note_controller import NoteController

class NotesButtonManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Controlador
        self.con = NoteController()
        # Lista de botones/ítems
        self.items = []
        self.master=master
        
    def render_notes(self, notes, batch_size=20):
        if not self.items:
            for widget in self.master.winfo_children():
                widget.destroy()

        self.items.clear()

        # Convertir lista a iterador para cargar por partes
        notes_iter = iter(notes)
        self._render_batch(notes_iter, batch_size)

    def _render_batch(self, notes_iter, batch_size):
        for _ in range(batch_size):
            try:
                note = next(notes_iter)
            except StopIteration:
                return  # Ya se renderizaron todas

            self.add_item(new_note=note)

        # Esperar 10 ms y continuar con el siguiente lote
        self.after(30, lambda: self._render_batch(notes_iter, batch_size))

    def add_item(self, new_note=None, title="Nueva nota", body="Escribe una descripción"):
        if not new_note:
            new_note = self.con.add_note(title,body)
        note = SelectableButtonItem(self.master, note=new_note, update=self.con.update, toast_father=self.master.master)
        self.items.append(note)
        note.pack(pady=0, fill="x", padx=5)
        #Forzar el render
        self.update_idletasks()

    def delete_selected(self):
        to_remove = [i for i in self.items if i.var.get()]
        if not to_remove:
            return
        note_ids = [i.note.id for i in to_remove if i.note.id]
        if note_ids:
            self.con.remove_notes(note_ids)
        for i in to_remove:
            i.destroy()
            self.items.remove(i)


    def filter_notes(self, query,*args):
        # Si no hay texto, mostrar todas

        notes = self.refresh_note_list()

        if not query:
            filtered_ids = {n.id for n in notes}
        else:
            filtered_notes = [
                n for n in notes
                if query in n.title.lower() or query in n.body.lower()
            ]
            filtered_ids = {n.id for n in filtered_notes}

        self.render_filter(filtered_ids)
        
    def render_filter(self, filtered_ids=None):
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

    def refresh_note_list(self):
        return self.con.get_notes()