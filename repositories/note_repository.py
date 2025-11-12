from entities.note import Note
from entities.note_manager import NoteManager
 
class NoteRepository:
    def __init__(self, sql_model):
        self.sql_model = sql_model
        self.manager = NoteManager(self._load_from_db())
        self._cache = self.manager.get_all()

    def _load_from_db(self):
        """Carga notas desde la base de datos (modelo SQL)."""
        return [Note(*note_tuple) for note_tuple in self.sql_model.get_all_notes()]

    def get_all_notes(self):
        return self.manager.get_all()

    def add_note(self, note):
        try:
            
            note.id = self.sql_model.insert_note(note)
            self.manager.add(note)
            self._sync_cache()
            print("✅ Nota agregada correctamente {note}")
            return note
        except Exception as e:
            print(f"❌ Error al agregar la nota: {e}")

    def edit_note(self, note):
        if not note.id:
            return print("❌ No se proporcionó un ID válido para la nota")
        try:
            self.sql_model.update_note(note)
            self.manager.update(note)
            self._sync_cache()
            print("✅ Nota actualizada correctamente")
        except Exception as e:
            print(f"Error al actualizar nota: {e}")

    def delete_many_notes(self, notes_id):
        if not notes_id:
            return
        try:
            self.sql_model.delete_notes_batch(notes_id)
            self.manager.remove(notes_id)
            self._sync_cache()
        except Exception as e:
            print(f"Error al eliminar notas: {e}")
    
    def _sync_cache(self):
        self._cache = self.manager.get_all()
