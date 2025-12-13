import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import sys
import webbrowser
from tkinter import font as tkFont
#from main import conectar_sql


# --- CAMINHO BASE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- JANELA PRINCIPAL ---
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

screen_width = 2000
screen_height = 1000
bg_image = Image.open(r"C:\Users\adria\Documents\GitHub\projetobd\Imagens_app\fundologs.jpg").resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

# --- CANVAS ---
canvas = ctk.CTkCanvas(app, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# --- TOP BAR ---
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0)

login_title = ctk.CTkLabel(
    top_bar,
    text="Login",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF",
    fg_color=None  # transparente
)
login_title.place(x=125, y=15)

# --- LOGO ---
img_path = os.path.join(BASE_DIR, r"Imagens_app\logo.png")
image = Image.open(img_path).resize((100, 100))
photo = ImageTk.PhotoImage(image)

logo_label = ctk.CTkLabel(top_bar, image=photo, text="")
logo_label.place(x=30, y=8)
logo_label.image = photo  # manter referência

# --- CAMPOS DE ENTRADA ---
entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=250, height=35)
entry.place(x=650, y=120)

passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250, height=35)
passw.place(x=650, y=170)

# --- OUTPUT LABEL ---
# Supondo que você tenha um canvas chamado "canvas"

# Criar fonte negrito
bold_font = tkFont.Font(family="Arial", size=14, weight="bold")

# Criar o texto no canvas
output_text = canvas.create_text(
    825, 300,
    text="", 
    fill="red",
    font=bold_font,
    anchor="nw"
)

# Função greet atualizada
def greet():
    nome = entry.get()
    if nome.strip() == "":
        canvas.itemconfig(output_text, text="Por favor preencha os campos!", fill="red")
    else:
        canvas.itemconfig(output_text, text=f"Olá {nome}, somos mesmo bué fixes 😎", fill="green")



# --- FUNÇÕES DE NAVEGAÇÃO ---
def open_signin():
    app.destroy()
    subprocess.Popen(["python", "signin.py"])

def open_principal():
    app.destroy()
    subprocess.Popen(["python", "abaabrir.py"])

# --- LABEL “Ir para o Sign In” com hover e clique ---
font_label = ("Arial", 14, "underline")

signin_text = canvas.create_text(
    890, 272,
    text="Ir para o Sign In",
    fill="#1E5EFF",
    font=font_label,
    anchor="nw"
)

# Hover e clique
def on_enter(event):
    canvas.itemconfig(signin_text, fill="orange")
    canvas.config(cursor="hand2")

def on_leave(event):
    canvas.itemconfig(signin_text, fill="#1E5EFF")
    canvas.config(cursor="")

def on_click(event):
    open_signin()

canvas.tag_bind(signin_text, "<Enter>", on_enter)
canvas.tag_bind(signin_text, "<Leave>", on_leave)
canvas.tag_bind(signin_text, "<Button-1>", on_click)


# --- LOGIN BUTTON ---
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
nasa = Image.open(img_pathnasa).resize((35, 35))
photonasa = ImageTk.PhotoImage(nasa)
nasa_label = ctk.CTkLabel(down_bar, image=photonasa, text="")
nasa_label.place(x=1390, y=15)
nasa_label.image = photonasa
nasa_label.bind("<Button-1>", lambda e: open_nasa())
nasa_label.configure(cursor="hand2")  # cursor de clique

# Instagram
img_pathinsta = os.path.join(BASE_DIR, r"Imagens_app\insta.png")
insta = Image.open(img_pathinsta).resize((35, 35))
photoinsta = ImageTk.PhotoImage(insta)
insta_label = ctk.CTkLabel(down_bar, image=photoinsta, text="")
insta_label.place(x=1419, y=15)
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





