import customtkinter as ctk
import components.ctk_widgets as widget
from components.selectable_button import SelectableButtonItem
from components.scrollframe import ScrollableFrame
from components.search_entry import SearchVar
import controllers.notes_controller as con
 
class NotesView(ctk.CTkFrame):
    def __init__(self, master, note_list=None,**kwargs):
        super().__init__(master,**kwargs)
        self.focus_set()
        # Vincular Ctrl + F

        self.master.bind("<Control-f>", self.show_search)
        self.master.bind("<Escape>", self.hide_search)

        # Lista de componentes
        self.items = []
        self.note_list= note_list

        # Frame de controles
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=5) 

        # Frame contenedor de ítems
        self.items_frame = ScrollableFrame(self, fg_color="transparent")
        self.items_frame.pack(pady=5, fill="both", expand=True)

        self.sync_button = widget.button_control(self.control_frame, text="🗘 Sync").pack(side="left", padx=2)
    
        self.add_button = widget.button_control(self.control_frame, text="✚ add", command=self.add_item).pack(side="left", padx=2)
        
        self.delete_button = widget.button_control(self.control_frame, text="🗑 del", command=self.delete_selected).pack(side="left", padx=2)

        self.search_button = widget.button_control(self.control_frame, text="🔍︎", command=self.show_search).pack(side="left", padx=2)      

        #List notes first time
        self.render_notes(self.note_list)

        # --- Campo de búsqueda ---
        self.search_var = SearchVar(self, search=self.filter_notes)

    def show_search(self,event=None):
        if self.search_var.visible():
            self.search_var.hide()
        else:
            self.search_var.show()
    
    def hide_search(self, event=None):
        if self.search_var.visible():
            self.search_var.hide()

    def render_notes(self, notes):
        if notes:
            for widget in self.items_frame.winfo_children():
                widget.destroy()

            for note in notes:
                self.add_item(note_id=note.id, title=note.title, body=note.body)

    def add_item(self, note_id = None, title="Nueva nota", body="Escribe una descripción"):
        #Si no existe el id entonces inserta una nueva nota en BD y devuelve su ID para el componente
        try:
            if not note_id:
                note_id = con.add_note(title, body)
                print(note_id)
        except Exception as e:
            return print(f"❌ Error al agregar la nota: {e}")
        note = SelectableButtonItem(self.items_frame, note_id=note_id, title=title, body=body, father_content=self)
        note.pack(pady=0, fill="x", padx=5)
        self.items.append(note)
    
    def delete_selected(self):
        to_remove = [i for i in self.items if i.var.get()]
        for i in to_remove:
            try:
                if i.note_id:
                    con.delete_note(i.note_id)
                i.destroy()
                self.items.remove(i)
            except Exception as e:
                return print(f"❌ Error al eliminar la nota: {e}")

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
    
