from entities.note import Note
import controllers.notes_controller as con

class NoteRepository:
    def __init__(self):
        self._notes_cache = []

    def refresh(self):
        data = con.get_all_notes()
        self._notes_cache = [Note(*n) for n in data]

    def get_all(self):
        if not self._notes_cache:
            self.refresh()
        return self._notes_cache
    
    def add (self, title, body):
        note_id= con.add_note(title, body)
        new_note = Note(note_id, title, body)
        self._notes_cache.append(new_note)
        return new_note

    def delete(self, note):
        if note in self._notes_cache: 
            con.delete_note(note.id)     # elimina de memoria
            self._notes_cache.remove(note)
        return True

    def update(self, note_id, new_body=None, new_title=None):
        con.edit_note(note_id, body=new_body, title=new_title)

        for note in self._notes_cache:
            if note.id == note_id:
                if new_body is not None:
                    note.body = new_body
                if new_title is not None:
                    note.title = new_title
                break

    def delete_many_notes(self, note_ids):
        if not note_ids:
            return
        con.delete_list_note(note_ids)
        self._notes_cache = [n for n in self._notes_cache if n.id not in note_ids]