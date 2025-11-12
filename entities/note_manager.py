class NoteManager:

    def __init__(self, notes=None):
        # Lista local (puede ser cargada desde caché o base de datos)
        self._notes = notes or []

    def get_all(self):
        return list(self._notes)  # retorno inmutable

    def add(self, note):
        self._notes.append(note)

    def update(self, updated_note):
        for i, note in enumerate(self._notes):
            if note.id == updated_note.id:
                self._notes[i] = updated_note
                return True
        return False


    def remove(self, notes_id):
        self._notes = [n for n in self._notes if n.id not in notes_id]


