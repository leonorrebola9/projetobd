import customtkinter as ctk
from PIL import Image
import subprocess
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

# ================================
# RETÂNGULO AZUL NO TOPO
# ================================
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#1E5EFF")
top_bar.place(x=0, y=0)

# --- LOGIN TITLE ---
login = ctk.CTkLabel(top_bar, text="Sign In", font=("Comic Sans MS", 50, "bold"), text_color="white")
login.place(x=30, y=10)

# --- USER ENTRY ---
entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=250)
entry.place(x=30, y=150)

# --- PASSWORD ENTRY ---
passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250)
passw.place(x=30, y=200)

# --- OUTPUT LABEL ---
output_label = ctk.CTkLabel(app, text="", text_color="purple")
output_label.place(x=30, y=250)


def greet():
    nome = entry.get()
    if nome.strip() == "":
        output_label.configure(text="Por favor escreva um nome!")
    else:
        output_label.configure(text=f"Olá {nome}, somos mesmo bué fixes 😎")


# --- FUNÇÃO PARA ABRIR SIGNIN E FECHAR LOGIN ---
def open_signin():
    subprocess.Popen(["python", "signin.py"])
    app.destroy()       # ← Fecha a janela atual
    sys.exit()          # ← Garante que o processo fecha


# --- ICON IMAGE ---
icon_image = Image.open("menu.png")
icon_image = icon_image.resize((30, 30))
icon_img = ctk.CTkImage(light_image=icon_image, dark_image=icon_image)

menu_frame = None


def toggle_menu():
    global menu_frame

    if menu_frame is not None:
        menu_frame.destroy()
        menu_frame = None
        return

    menu_frame = ctk.CTkFrame(app, width=150, height=140, corner_radius=10)
    menu_frame.place(x=250, y=100)

    ctk.CTkButton(menu_frame, text="Sign In",
                  font=("Candara", 12, "bold"),
                  width=120,
                  command=open_signin).pack(pady=5)

    ctk.CTkButton(menu_frame, text="Opção 2", width=120).pack(pady=5)
    ctk.CTkButton(menu_frame, text="Entrar", width=120, command=greet).pack(pady=5)


# --- BUTTON WITH ICON ---
menu_button = ctk.CTkButton(app, text="", image=icon_img, command=toggle_menu, width=40, height=40)
menu_button.place(x=330, y=20)

# --- LOGIN BUTTON ---
greet_btn = ctk.CTkButton(app, text="Entrar", command=greet, width=250)
greet_btn.place(x=30, y=300)

app.mainloop()
