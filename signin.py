import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import sys
import webbrowser

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- CAMINHO BASE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- JANELA PRINCIPAL ---
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

# --- TOP BAR ---
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0)

# --- LOGO ---
img_path = os.path.join(BASE_DIR, r"Imagens_app\logo.png")
image = Image.open(img_path).resize((100, 100))
photo = ImageTk.PhotoImage(image)

logo_label = ctk.CTkLabel(top_bar, image=photo, text="")
logo_label.place(x=30, y=8)
logo_label.image = photo  # manter referência


# --- TÍTULO ---
login_title = ctk.CTkLabel(
    top_bar,
    text="Sign In",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF"
)
login_title.place(x=150, y=15)  # deslocado para dar espaço à logo

# --- CAMPOS DE ENTRADA ---
name = ctk.CTkEntry(app, placeholder_text="Nome", width=400, height=35)
name.place(x=400, y=120)

surname = ctk.CTkEntry(app, placeholder_text="Sobrenome", width=250, height=35)
surname.place(x=800, y=120)

usuario_entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=400, height=35)
usuario_entry.place(x=400, y=200)

passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250, height=35)
passw.place(x=800, y=200)

# --- OUTPUT LABEL ---
output_label = ctk.CTkLabel(app, text="", text_color="Red")
output_label.place(x=650, y=235)

# --- FUNÇÃO BOTÃO “ENTRAR” ---
def greet():
    nome = name.get()
    sobrenome = surname.get()
    usuario = usuario_entry.get()
    senha = passw.get()

    if not nome or not sobrenome or not usuario or not senha:
        output_label.configure(text="Preencha todos os campos!", text_color="red")
        return

    output_label.configure(text="Conta criada com sucesso!", text_color="green")

greet_btn = ctk.CTkButton(
    app,
    text="Entrar",
    fg_color="#0C1B33",
    hover_color="#14284D",
    text_color="white",
    width=250,
    height=40,
    command=greet
)
greet_btn.place(x=650, y=270)

# --- FUNÇÃO PARA ABRIR login.py ---
def open_signin():
    login_path = os.path.join(BASE_DIR, "login.py")
    if not os.path.isfile(login_path):
        output_label.configure(text="Erro: login.py não encontrado.", text_color="red")
        return
    try:
        app.destroy()
        subprocess.Popen([sys.executable, login_path], cwd=BASE_DIR)
    except Exception as e:
        output_label.configure(text=f"Erro ao abrir login: {e}", text_color="red")

# --- LABEL “LOGIN” COM HOVER E CLIQUE ---
font_label = ctk.CTkFont(family="Arial", size=14, underline=True)
signin_label = ctk.CTkLabel(app, text="Login", text_color="#4278CE", font=font_label)
signin_label.place(x=710, y=310)

def on_enter(event):
    signin_label.configure(text_color="orange", cursor="hand2")

def on_leave(event):
    signin_label.configure(text_color="#4278CE", cursor="")

signin_label.bind("<Enter>", on_enter)
signin_label.bind("<Leave>", on_leave)
signin_label.bind("<Button-1>", lambda e: open_signin())




#---------------------------------------------
# --- FUNÇÕES ABRIR REDES SOCIAIS -------------
#---------------------------------------------

def open_nasa():
    webbrowser.open("https://www.nasa.gov/")

def open_insta():
    webbrowser.open("https://www.instagram.com/nasa/")

def open_twitter():
    webbrowser.open("https://x.com/NASA")

def open_facebook():
    webbrowser.open("https://www.facebook.com/NASA/")

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/company/nasa/?originalSubdomain=pt")





#---------------------------------------------
# --- DOWN BAR -----------------------------
#---------------------------------------------


down_bar = ctk.CTkFrame(app, width=2000, height=250, fg_color="#B4AEAE")
down_bar.place(x=0, y=650)

mencao = ctk.CTkLabel(
    app,
    text="@Adriana Abreu & Leonor Rebola",
    text_color="black",
    font=("Aharoni", 10),
    fg_color="#B4AEAE"
)
mencao.place(x=10, y=670)


# --- IMAGENS LOGOS ---

# Nasa
img_pathnasa = os.path.join(BASE_DIR, r"Imagens_app\nasa.png")
nasa = Image.open(img_pathnasa).resize((30, 30))
photonasa = ImageTk.PhotoImage(nasa)
nasa_label = ctk.CTkLabel(down_bar, image=photonasa, text="")
nasa_label.place(x=1390, y=15)
nasa_label.image = photonasa
nasa_label.bind("<Button-1>", lambda e: open_nasa())
nasa_label.configure(cursor="hand2")  # cursor de clique

# Instagram
img_pathinsta = os.path.join(BASE_DIR, r"Imagens_app\insta.png")
insta = Image.open(img_pathinsta).resize((45, 35))
photoinsta = ImageTk.PhotoImage(insta)
insta_label = ctk.CTkLabel(down_bar, image=photoinsta, text="")
insta_label.place(x=1415, y=15)
insta_label.image = photoinsta
insta_label.bind("<Button-1>", lambda e: open_insta())
insta_label.configure(cursor="hand2")

# Twitter
img_pathtwitter = os.path.join(BASE_DIR, r"Imagens_app\twitter.png")
twitter = Image.open(img_pathtwitter).resize((35, 30))
phototwitter = ImageTk.PhotoImage(twitter)
twitter_label = ctk.CTkLabel(down_bar, image=phototwitter, text="")
twitter_label.place(x=1450, y=15)
twitter_label.image = phototwitter
twitter_label.bind("<Button-1>", lambda e: open_twitter())
twitter_label.configure(cursor="hand2")

# Facebook
img_pathfacebook = os.path.join(BASE_DIR, r"Imagens_app\facebook.png")
facebook = Image.open(img_pathfacebook).resize((35, 35))
photofacebook = ImageTk.PhotoImage(facebook)
facebook_label = ctk.CTkLabel(down_bar, image=photofacebook, text="")
facebook_label.place(x=1480, y=15)
facebook_label.image = photofacebook
facebook_label.bind("<Button-1>", lambda e: open_facebook())
facebook_label.configure(cursor="hand2")

# LinkedIn
img_pathlinkedin = os.path.join(BASE_DIR, r"Imagens_app\linkedin.png")
linkedin = Image.open(img_pathlinkedin).resize((38, 38))
photolinkedin = ImageTk.PhotoImage(linkedin)
linkedin_label = ctk.CTkLabel(down_bar, image=photolinkedin, text="")
linkedin_label.place(x=1505, y=14)
linkedin_label.image = photolinkedin
linkedin_label.bind("<Button-1>", lambda e: open_linkedin())
linkedin_label.configure(cursor="hand2")


app.mainloop()



