import customtkinter as ctk
from views.notes_view import NotesView
from entities.note import Note

import controllers.notes_controller as con


# Configuración global   
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Lista de notas


def init_view():
    #notes = notes.()
    app = ctk.CTk()
    app.title("Bloc de Notas")
    app.geometry("500x400")

    # Tamaño mínimo permitido
    app.minsize(500, 300)

    # Aquí se renderiza la vista dentro del frame con scroll
    notes_view = NotesView(app)
    notes_view.pack(fill="both", expand=True)    

    app.mainloop()
    