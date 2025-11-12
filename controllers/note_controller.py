from repositories.note_repository import NoteRepository
import models.note_model as model
from entities.note import Note

class NoteController:
    def __init__(self, repository=None):
        self.repo = NoteRepository(model)

    def get_notes(self):
        return self.repo.get_all_notes()

    def add_note(self, title, body):
        note = Note(title=title, body=body)
        return self.repo.add_note(note)

    def remove_notes(self,notes_id):
        self.repo.delete_many_notes(notes_id)

    def update(self,note):
        self.repo.edit_note(note)
