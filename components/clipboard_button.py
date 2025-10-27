import customtkinter as ctk
from components.toast import ToastMessage

class ClipboardButton(ctk.CTkFrame):
    def __init__(self,master, text=None, icon_on="!✔", icon_off="🗐", content=None):
        super().__init__(master)

        self.text = text
        self.icon_on = icon_on
        self.icon_off = icon_off
        self.content = content
        self.var = ctk.BooleanVar(value=False)
        # Botón que copia el valor
        self.copy_button = ctk.CTkButton(
            self,
            text=self.icon_off,
            width=30,
            command=self.copy_to_clipboard,
            fg_color="#525459",
            #hover_color="#222325",
            text_color="white",
            corner_radius=10,
            font=("Arial", 14, "bold"),
            border_spacing=1
        )
        self.copy_button.pack(fill="both", expand=True,pady=5)

    def copy_to_clipboard(self):
        copy = self.text()
        self.clipboard_clear()
        self.clipboard_append(copy)
        ToastMessage(self.content, text="Copiado al portapapeles ✅")
        self.update()  # asegura que se actualice el portapapeles (importante en Linux)

 

