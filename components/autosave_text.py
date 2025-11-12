import customtkinter as ctk
from components.autoresize_textbox import AutoResizeTextbox

class AutoSaveText(ctk.CTkFrame):
    def __init__(self, master, note=None,update=None,**kwargs):
        super().__init__(master, **kwargs)

        self.note = note
        self.update = update
        self._after_id = None
        self._last_saved = None
        # --- Línea inferior decorativa (opcional) ---
        self.bottom_border = ctk.CTkFrame(self, height=2, fg_color="royalblue", corner_radius=0)
        self.bottom_border.pack(fill="x")

        # --- Textbox ---
        self.textbox = AutoResizeTextbox(self)
        self.textbox.pack(fill="x", expand=True, pady=(0, 2))
        self.textbox.load_content(self.note.body)        

        # --- Eventos ---
        self.textbox.bind("<KeyRelease>", self.on_edit)

    def on_edit(self, event=None):
        """Programa el guardado automático con debounce."""
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(1000, self.edit_text)

    def edit_text(self):
        """Guarda el contenido si cambió."""
        contenido = self.textbox.get("1.0", "end-1c").strip()
        if contenido == self._last_saved:
            return
        self.note.body=contenido
        self.update(self.note)
        self._last_saved = contenido
        self._after_id = None
        print("Texto guardado automáticamente:\n", contenido)
        print("-----------")

    def get(self):
        """Devuelve el contenido actual."""
        return self.textbox.get("1.0", "end-1c")

    def focus(self):
        self.textbox.focus_set()

    def show(self):
        self.pack(fill="x", padx=5, pady=(5, 0))

    def hide(self):
        self.pack_forget()

    def visible(self):
        """Devuelve si el frame está actualmente visible en pantalla."""
        return self.winfo_ismapped()
