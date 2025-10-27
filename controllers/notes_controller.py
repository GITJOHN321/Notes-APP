import models.note_model as model
from entities.note import Note

def get_list_notes():
    return [Note(*note_tuple) for note_tuple in model.get_all_notes()]

def add_note(title, body):
    if title and body:
        try:
            note = model.add_note(title, body)
            print("✅ Nota agregada correctamente")
            return note
        except Exception as e:
            print(f"❌ Error al agregar la nota: {e}")

def edit_note(id_note, title=None, body=None):
    if not id_note:
        return print("❌ No se proporcionó un ID válido para la nota")

    if title is None and body is None:
        return print("⚠️ No se proporcionaron parámetros para actualizar")

    try:
        model.update_note(id_note, title=title, body=body)
        print("✅ Nota actualizada correctamente")
    except Exception as e:
        print(f"Error al actualizar nota: {e}")
            

def delete_note(id_note):
    if id_note:
        try:
            model.delete_note(int(id_note))
            print("Nota eliminada correctamente")
        except Exception as e:
            print(f"Error al eliminar nota: {e}")