import customtkinter as ctk


def button_note(container, text, command=None):
    button = ctk.CTkButton(
        container,
        text=text,
        command=command,
        fg_color="royalblue",
        text_color="white",
        corner_radius=10,
        font=("Arial", 14, "bold"),
        border_spacing=1
    )
    return button

def button_control(container, text=None, command=None):
    button = ctk.CTkButton(
        container,
        text=text,
        command=command,
        fg_color="#525459",
        hover_color="#222325",
        text_color="white",
        corner_radius=10,
        font=("Arial", 14, "bold"),
        border_spacing=1
    )
    return button


def frame_note(container):
    frame = ctk.CTkFrame(container)
    frame.pack(fill="x", pady=5)
    return frame

def textbox_note(container, body):
    textbox = ctk.CTkTextbox(
        container,
        height=100
    )
    textbox.pack(fill="x", padx=0, pady=(5,0))
    textbox.insert("0.0", body)
    return textbox
