import customtkinter as ctk
from components.toast import ToastMessage
import components.ctk_widgets as widget

class ClipboardButton(ctk.CTkFrame):
    def __init__(self,master, text=None, icon_on="!✔", icon_off="\uf0c5", content=None):
        super().__init__(master)

        self.text = text
        self.icon_on = icon_on
        self.icon_off = icon_off
        self.content = content
        self.var = ctk.BooleanVar(value=False)
        # Botón que copia el valor
        self.copy_button = widget.button_clipboard(self,text=self.icon_off, command=self.copy_to_clipboard)
        self.copy_button.pack(fill="both", expand=True,pady=5)

    def copy_to_clipboard(self):
        copy = self.text()
        self.clipboard_clear()
        self.clipboard_append(copy)
        ToastMessage(self.content, text="Copiado al portapapeles \uf058")
        self.update()  # asegura que se actualice el portapapeles (importante en Linux)

 