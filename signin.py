import customtkinter as ctk
from PIL import Image
import subprocess
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

# --- TOP BAR ---
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#1E5EFF")
top_bar.place(x=0, y=0)

# --- LOGIN TITLE ---
login = ctk.CTkLabel(top_bar, text="Sign In", font=("Comic Sans MS", 50, "bold"), text_color="#E2DFDF")
login.place(x=30, y=10)

# --- USER ENTRY ---
entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=250)
entry.place(x=650, y=150)

# --- PASSWORD ENTRY ---
passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250)
passw.place(x=650, y=200)

# --- OUTPUT LABEL (CTkFont com sublinhado) ---
font = ctk.CTkFont(family="Arial", size=14, underline=True)
output_label = ctk.CTkLabel(app, text="Ir para o Login", text_color="#1E5EFF", font=font)
output_label.place(x=725, y=230)

# --- Funções ---
def greet():
    nome = entry.get()
    if nome.strip() == "":
        output_label.configure(text="Por favor preencha os campos!")
    else:
        output_label.configure(text=f"Olá {nome}, somos mesmo bué fixes 😎")

def open_login():
    subprocess.Popen(["python", "login.py"])
    app.destroy()
    sys.exit()

# --- Hover e cursor de mão ---
def on_enter(event):
    output_label.configure(text_color="orange", cursor="hand2")  # cursor "mãozinha"

def on_leave(event):
    output_label.configure(text_color="#1E5EFF", cursor="")

output_label.bind("<Enter>", on_enter)
output_label.bind("<Leave>", on_leave)
output_label.bind("<Button-1>", lambda e: open_login())  # clique abre login

# --- ICON IMAGE ---
icon_image = Image.open("menu.png").resize((30, 30))
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

    ctk.CTkButton(menu_frame, text="Sign In", font=("Candara", 12, "bold"),
                  width=120, command=open_login).pack(pady=5)
    ctk.CTkButton(menu_frame, text="Opção 2", width=120).pack(pady=5)
    ctk.CTkButton(menu_frame, text="Entrar", width=120, command=greet).pack(pady=5)

# --- LOGIN BUTTON ---
greet_btn = ctk.CTkButton(app, text="Entrar", command=greet, width=250)
greet_btn.place(x=650, y=300)

down_bar = ctk.CTkFrame(app, width=1920, height=200, fg_color="#B4AEAE")
down_bar.place(x=0, y=650)

app.mainloop()

