class Note:
    def __init__(self, id=None, title="", body=""):
        self.id = id
        self.title = title
        self.body = body
    
    #This use for print on console
    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"