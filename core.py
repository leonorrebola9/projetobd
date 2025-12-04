import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

bg_image = ctk.CTkImage(
    light_image=Image.open("fundo01.jpg"),
    dark_image=Image.open("fundo01.jpg"),
    size=(1580, 800)
)

bg_label = ctk.CTkLabel(app, image=bg_image, text="")
bg_label.place(x=0, y=0)
# --- LOGIN TITLE ---
# --- LOGIN TITLE (AGORA TRANSPARENTE) ---
login = ctk.CTkLabel(
    app, 
    text="Bem Vindo", 
    font=("Comic Sans MS", 50, "bold"),
    bg_color="transparent",  # Corrigido: usa fg_color
    text_color="white"       # Adicionado: Garante que o texto se destaca na cor branca
)
# Usamos place com coordenadas relativas para posicionar em cima da imagem
login.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

"""
# --- USER ENTRY ---
entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=250)
entry.place(x=30, y=120)

# --- PASSWORD ENTRY ---
passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250)
passw.place(x=30, y=170)

# --- OUTPUT LABEL ---
output_label = ctk.CTkLabel(app, text="", text_color="purple")
output_label.place(x=30, y=220)

def greet():
    nome = entry.get()
    if nome.strip() == "":
        output_label.configure(text="Por favor escreva um nome!")
    else:
        output_label.configure(text=f"Olá {nome}, somos mesmo bué fixes 😎")

# --- ICON IMAGE ---
icon_image = Image.open("menu.png")
icon_image = icon_image.resize((30, 30))
icon_img = ctk.CTkImage(light_image=icon_image, dark_image=icon_image)

# Variável global para o menu
menu_frame = None

def toggle_menu():
    global menu_frame

    # Fecha se já estiver aberto
    if menu_frame is not None:
        menu_frame.destroy()
        menu_frame = None
        return

    # Abre menu
    menu_frame = ctk.CTkFrame(app, width=150, height=140, corner_radius=10)
    menu_frame.place(x=250, y=60)

    ctk.CTkButton(menu_frame, text="Sign In",font=("Candara",12, "bold"), width=120).pack(pady=5)
    ctk.CTkButton(menu_frame, text="Opção 2", width=120).pack(pady=5)
    ctk.CTkButton(menu_frame, text="Entrar", width=120, command=greet).pack(pady=5)

# --- BUTTON WITH ICON ---
menu_button = ctk.CTkButton(app, text="", image=icon_img, command=toggle_menu, width=40, height=40)
menu_button.place(x=330, y=10)

# --- LOGIN BUTTON ---
greet_btn = ctk.CTkButton(app, text="Entrar", command=greet, width=250)
greet_btn.place(x=30, y=270)

"""
app.mainloop()
