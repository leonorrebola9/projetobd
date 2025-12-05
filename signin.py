import customtkinter as ctk
from PIL import Image
import subprocess

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- JANELA PRINCIPAL ---
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

# --- TOP BAR ---
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#1E5EFF")
top_bar.place(x=0, y=0)

login_title = ctk.CTkLabel(
    top_bar,
    text="Sign In",
    font=("Comic Sans MS", 50, "bold"),
    text_color="#E2DFDF",
    fg_color=None  # transparente
)
login_title.place(x=30, y=10)


name = entry = ctk.CTkEntry(app, placeholder_text="Nome", width=400, height=35)
name.place(x=400, y=120)


surname = entry = ctk.CTkEntry(app, placeholder_text="Sobrenome", width=250, height=35)
surname.place(x=800, y=120)

# --- CAMPOS DE ENTRADA ---
entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=400, height=35)
entry.place(x=400, y=200)

passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250, height=35)
passw.place(x=800, y=200)

# --- OUTPUT LABEL ---
output_label = ctk.CTkLabel(app, text="", text_color="Red", fg_color=None)
output_label.place(x=650, y=235)

def greet():
    nome = entry.get()
    if nome.strip() == "":
        output_label.configure(text="Por favor preencha os campos!")
    else:
        output_label.configure(text=f"Olá {nome}, somos mesmo bué fixes 😎")

# --- FUNÇÕES DE NAVEGAÇÃO ---
def open_signin():
    app.destroy()
    subprocess.Popen(["python", "login.py"])

def open_principal():
    app.destroy()
    subprocess.Popen(["python", "abaabrir.py"])

# --- LABEL “Ir para o Sign In” com hover e clique ---
font_label = ctk.CTkFont(family="Arial", size=14, underline=True)
signin_label = ctk.CTkLabel(app, text="Login", text_color="#1E5EFF", font=font_label, fg_color=None)
signin_label.place(x=710, y=310)

def on_enter(event):
    signin_label.configure(text_color="orange", cursor="hand2")

def on_leave(event):
    signin_label.configure(text_color="#1E5EFF", cursor="")

signin_label.bind("<Enter>", on_enter)
signin_label.bind("<Leave>", on_leave)
signin_label.bind("<Button-1>", lambda e: open_signin())

# --- LOGIN BUTTON ---
greet_btn = ctk.CTkButton(app, text="Entrar", command=greet, width=250, height=40)
greet_btn.place(x=650, y=270)

# --- DOWN BAR ---
down_bar = ctk.CTkFrame(app, width=2000, height=250, fg_color="#B4AEAE")
down_bar.place(x=0, y=650)

# --- MENÇÃO SOBRE O DOWN BAR ---
mencao = ctk.CTkLabel(
    app,
    text="@Adriana Abreu & Leonor Rebola",
    text_color="black",
    font=("Comic Sans MS", 10),
    fg_color="#B4AEAE"  # transparente
)
# Coloca dentro do down_bar
mencao.place(x=10, y=670)

# --- MENU COM ÍCONE (opcional) ---
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
    menu_frame.place(x=250, y=60)
    ctk.CTkButton(menu_frame, text="Página Principal", width=120).pack(pady=5)
    ctk.CTkButton(menu_frame, text="Sign In", width=120, command=open_signin).pack(pady=5)


# --- BOTÃO DE MENU (opcional) ---
# menu_button = ctk.CTkButton(app, text="", image=icon_img, command=toggle_menu, width=40, height=40)
# menu_button.place(x=1450, y=10)

app.mainloop()
