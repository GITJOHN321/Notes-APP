import customtkinter as ctk

class ToastMessage(ctk.CTkFrame):
    def __init__(self, master, text="", duration=2000, **kwargs):
        super().__init__(master, fg_color="#333333", corner_radius=8, **kwargs)

        self.text = text
        self.duration = duration

        # Crear el texto dentro del frame
        self.label = ctk.CTkLabel(
            self,
            text=text,
            text_color="white",
            font=("Arial", 12)
        )
        self.label.pack(padx=15, pady=8)

        # Colocar el toast de forma flotante
        self.place(relx=0.5, rely=0.9, anchor="center")

        # Programar la desaparición
        self.after(self.duration, self.destroy)

    def destroy(self):
        super().destroy()
