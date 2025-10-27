import platform
import customtkinter as ctk

class ScrollableFrame(ctk.CTkScrollableFrame):
    """CTkScrollableFrame con soporte de rueda y protección contra scroll cuando no procede."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # cachear el nombre del sistema para no llamarlo en cada evento
        self._os_name = platform.system()
        # bind al entrar/salir del widget para no registrar handlers globales permanentemente
        self.bind("<Enter>", self._bind_mousewheel)
        self.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, _event=None):
        if self._os_name in ("Windows", "Darwin"):
            self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        else:  # Linux
            self.bind_all("<Button-4>", self._on_mousewheel, add="+")
            self.bind_all("<Button-5>", self._on_mousewheel, add="+")

    def _unbind_mousewheel(self, _event=None):
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

    def _on_mousewheel(self, event):
        """
        Maneja la rueda con protección:
         - no hace nada si el contenido cabe en el viewport
         - impide desplazar más allá de los límites
        """
        canvas = getattr(self, "_parent_canvas", None)
        if canvas is None:
            return  # seguridad si la implementación interna cambia

        # yview devuelve (start_frac, end_frac) entre 0.0 y 1.0
        start, end = canvas.yview()
        visible_fraction = end - start

        # Si todo el contenido cabe (visible_fraction >= 1.0) no debe scrollarse
        if visible_fraction >= 1.0:
            return

        # Normalizar el valor de "pasos" según plataforma
        if self._os_name == "Windows":
            # event.delta suele ser múltiplo de 120 por tick
            steps = int(event.delta / 120)
            # queremos que positivo sea scroll arriba -> invertimos signo para que coincida
            delta_units = -steps
        elif self._os_name == "Darwin":  # macOS
            # macOS puede dar delta pequeño o grande según touchpad
            steps = int(event.delta)
            delta_units = -steps
        else:  # Linux: event.num == 4 (up) o 5 (down)
            if getattr(event, "num", None) == 4:
                delta_units = -1
            elif getattr(event, "num", None) == 5:
                delta_units = 1
            else:
                return

        # Antes de aplicar, comprobar límites para evitar "subir" más de la cuenta
        # Si delta_units < 0 => subimos (mover vista hacia arriba), solo si start > 0
        # Si delta_units > 0 => bajamos, solo si end < 1
        if delta_units < 0 and start <= 0.0:
            return
        if delta_units > 0 and end >= 1.0:
            return

        # Finalmente desplazar (unidades). Ajusta el factor si quieres más/menos sensibilidad.
        try:
            canvas.yview_scroll(delta_units, "units")
        except Exception:
            # fallback seguro: usar moveto con fracción cuidando límites
            new_start = min(max(start + (delta_units * 0.03), 0.0), 1.0 - visible_fraction)
            canvas.yview_moveto(new_start)

    def destroy(self):
        # limpiar bindings globales si quedaron
        self._unbind_mousewheel()
        super().destroy()
