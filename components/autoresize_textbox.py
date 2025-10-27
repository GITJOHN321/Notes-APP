import customtkinter as ctk

class AutoResizeTextbox(ctk.CTkTextbox):
    def __init__(self, master=None, min_height=100, max_height=500, line_height=20, **kwargs):
        kwargs.setdefault("undo", True)
        kwargs.setdefault("autoseparators", True)
        kwargs.setdefault("maxundo", -1)
        super().__init__(master, **kwargs)

        # Guardamos los parámetros
        self.min_height = min_height
        self.max_height = max_height
        self.line_height = line_height

        # Enlazamos el evento para que escuche cuando se edite
        self.bind("<<Modified>>", self._resize_to_content)

        # Redimensionamos inicialmente según el texto existente
        self.after(100, self._resize_to_content)

         # --- Atajos de teclado ---
        self.bind("<Control-z>", self.undo_action)
        self.bind("<Control-y>", self.redo_action)
        self.bind("<Control-Shift-z>", self.redo_action)  # Ctrl+Shift+Z = rehacer (opcional)

    def _resize_to_content(self, event=None):
        # Obtiene todo el texto
        text = self.get("1.0", "end-1c")

        # Cuenta cuántas líneas hay
        num_lines = text.count("\n") + 1

        # Calcula altura sugerida
        new_height = num_lines * self.line_height

        # Aplica límites mínimo y máximo
        final_height = max(self.min_height, min(new_height, self.max_height))

        # Configura el nuevo alto
        self.configure(height=final_height)

        # Resetea el flag de modificación para que vuelva a detectar cambios
        self.edit_modified(False)

    # --- Métodos undo/redo ---
    def undo_action(self, event=None):
        try:
            self.edit_undo()
        except Exception as e:
            print("Undo error:", e)
        return "break"

    def redo_action(self, event=None):
        try:
            self.edit_redo()
        except Exception as e:
            print("Redo error:", e)
        return "break"
    
    def load_content(self, text):
        self.delete("1.0", "end")
        self.insert("1.0", text)
        # Asegurar que el Text haya procesado la inserción
        self.update_idletasks()
        # Resetear la pila de undo para que el contenido actual sea el estado base
        try:
            self.edit_reset()
        except Exception as e:
            print("edit_reset error:", e)