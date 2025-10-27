import controllers.notes_controller as controller
from models.note_model import create_table
from views.app_view import init_view

if __name__ == "__main__":
    create_table()
    print("=== CRUD de Notas en Consola ===")
    init_view()
