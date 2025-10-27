import platform
import customtkinter as ctk
import tkinter as tk

class ScrollableFrame(ctk.CTkScrollableFrame):
    """CTkScrollableFrame con soporte de rueda y protección contra scroll cuando no procede."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._os_name = platform.system()
    # Vincula el propio frame
        self.bind("<Enter>", self._bind_mousewheel)
        self.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, _event=None):
        # ligamos globalmente para capturar la rueda aunque el widget no tenga foco,
        # pero nuestro handler decidirá si debe actuar según el widget bajo el cursor.
        if self._os_name in ("Windows", "Darwin"):
            # usamos add="+" para no sobrescribir otros bindings
            self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        else:
            self.bind_all("<Button-4>", self._on_mousewheel, add="+")
            self.bind_all("<Button-5>", self._on_mousewheel, add="+")

    def _unbind_mousewheel(self, _event=None):
        # intentar limpiar los bindings que añadimos
        if self._os_name in ("Windows", "Darwin"):
            try:
                self.unbind_all("<MouseWheel>")
            except Exception:
                pass
        else:
            try:
                self.unbind_all("<Button-4>")
                self.unbind_all("<Button-5>")
            except Exception:
                pass

    def _widget_under_pointer(self, event):
        """Devuelve el widget real bajo el puntero (o None)."""
        try:
            return self.winfo_containing(event.x_root, event.y_root)
        except Exception:
            return None

    def _is_scrollable_widget(self, widget):
        """Decidir si el widget sabe hacer scroll por sí mismo.
        heurística: si tiene método yview o es instancia de tk.Text / CTkTextbox.
        """
        if widget is None:
            return False

        # widget puede ser nombre interno; usar isinstance si es widget real
        try:
            # direct check for Text-like widgets
            if isinstance(widget, (tk.Text, )):
                return True
            # customtkinter CTkTextbox suele heredar de tk.Text, pero por seguridad:
            if widget.__class__.__name__ in ("CTkTextbox", "AutoResizeTextbox"):
                return True
            # si implementa yview-> es probablemente scrollable (Listbox, Text, Canvas, etc.)
            if hasattr(widget, "yview"):
                return True
        except Exception:
            pass
        return False

    def _on_mousewheel(self, event):
        """
        Maneja la rueda con protección:
         - Si el widget bajo el puntero es scrollable (ej: Text) dejamos que lo maneje.
         - Si no, hacemos scroll del canvas del CTkScrollableFrame y devolvemos "break".
        """
        # obtener canvas interno (protegido: puede cambiar la implementación interna de CTk)
        canvas = getattr(self, "_parent_canvas", None)
        if canvas is None:
            # intentar obtenerlo por búsqueda (fallback)
            for child in self.winfo_children():
                # CTkScrollableFrame suele tener un Canvas interno; detectarlo por clase
                if isinstance(child, tk.Canvas):
                    canvas = child
                    break
            if canvas is None:
                return

        # si el cursor está sobre un widget que sabe hacer scroll, no interferimos
        widget_under = self._widget_under_pointer(event)
        if self._is_scrollable_widget(widget_under):
            # dejamos que el widget processe el evento; no devolvemos "break"
            return

        # Normalizar delta según plataforma
        if self._os_name == "Windows":
            steps = int(event.delta / 120)
            delta_units = -steps
        elif self._os_name == "Darwin":
            steps = int(event.delta)
            delta_units = -steps
        else:
            # Linux: Button-4 = up, Button-5 = down
            if getattr(event, "num", None) == 4:
                delta_units = -1
            elif getattr(event, "num", None) == 5:
                delta_units = 1
            else:
                return

        # límites y cálculo de visible fraction
        start, end = canvas.yview()
        visible_fraction = end - start
        if visible_fraction >= 1.0:
            return  # no hay nada que desplazar

        if delta_units < 0 and start <= 0.0:
            return
        if delta_units > 0 and end >= 1.0:
            return

        try:
            canvas.yview_scroll(delta_units, "units")
        except Exception:
            new_start = min(max(start + (delta_units * 0.03), 0.0), 1.0 - visible_fraction)
            canvas.yview_moveto(new_start)

        # IMPORTANTE: prevenimos que otros handlers procesen el evento (evita doble scroll)
        return "break"

    def destroy(self):
        self._unbind_mousewheel()
        super().destroy()
