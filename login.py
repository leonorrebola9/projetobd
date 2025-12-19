import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import sys
import webbrowser
from tkinter import font as tkFont
from main import get_connection, img_path, doc_path, open_insta, open_nasa, open_twitter, open_facebook, open_linkedin

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Login")

# --- FUNÇÕES DE NAVEGAÇÃO ---
def open_crud(nome_completo, usuario):
    app.destroy()
    crud_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crud.py")
    subprocess.Popen([sys.executable, crud_path, nome_completo, usuario])

def open_signin():
    app.destroy()
    signin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "signin.py")
    subprocess.Popen([sys.executable, signin_path])

# --- FUNÇÃO DE LOGIN ---
def greet():
    usuario = entry.get()
    senha = passw.get()

    if not usuario or not senha:
        canvas.itemconfig(output_text, text="Por favor preencha todos os campos!", fill="red")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, surname FROM users WHERE [user]=? AND passw=?", (usuario, senha))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            nome_completo = f"{user[0]} {user[1]}"
            canvas.itemconfig(output_text, text=f"Olá {nome_completo}, login efetuado!", fill="green")
            app.after(500, lambda: open_crud(nome_completo, usuario))
        else:
            canvas.itemconfig(output_text, text="Usuário ou senha incorretos!", fill="red")

    except Exception as e:
        canvas.itemconfig(output_text, text=f"Erro ao conectar ao banco: {e}", fill="red")

# --- INTERFACE VISUAL ---
screen_width = 2000
screen_height = 1000
bg_image = Image.open(img_path("fundologs.jpg")).resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = ctk.CTkCanvas(app, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# --- TOP BAR ---
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0)

logo = Image.open(img_path("logo.png")).resize((100, 100))
photo = ImageTk.PhotoImage(logo)
logo_label = ctk.CTkLabel(top_bar, image=photo, text="")
logo_label.place(x=30, y=8)

login_title = ctk.CTkLabel(top_bar, text="Login", font=("Aharoni", 50, "bold"), text_color="#E2DFDF")
login_title.place(x=125, y=15)

# --- CAMPOS DE ENTRADA ---
entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=250, height=35)
entry.place(x=650, y=120)

passw = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250, height=35)
passw.place(x=650, y=170)

bold_font = tkFont.Font(family="Arial", size=14, weight="bold")
output_text = canvas.create_text(825, 300, text="", fill="red", font=bold_font, anchor="nw")

greet_btn = ctk.CTkButton(app, text="Entrar", fg_color="#0C1B33", hover_color="#14284D", text_color="white", width=250, height=40, command=greet)
greet_btn.place(x=650, y=270)

# --- SIGN IN LINK ---
font_label = ("Arial", 14, "underline")
signin_text = canvas.create_text(890, 272, text="Ir para o Sign In", fill="#1E5EFF", font=font_label, anchor="nw")

def on_enter(event):
    canvas.itemconfig(signin_text, fill="orange")
    canvas.config(cursor="hand2")

def on_leave(event):
    canvas.itemconfig(signin_text, fill="#1E5EFF")
    canvas.config(cursor="")

canvas.tag_bind(signin_text, "<Enter>", on_enter)
canvas.tag_bind(signin_text, "<Leave>", on_leave)
canvas.tag_bind(signin_text, "<Button-1>", lambda e: open_signin())

# --- DOWN BAR ---
down_bar = ctk.CTkFrame(app, width=2000, height=250, fg_color="#B4AEAE")
down_bar.place(x=0, y=650)

ctk.CTkLabel(down_bar, text="@Adriana Abreu & Leonor Rebola", text_color="black", font=("Aharoni", 12)).place(x=20, y=20)
ctk.CTkLabel(down_bar, text="“Impactos de asteroides moldaram a história da vida na Terra; compreendê-los é compreender nosso passado e proteger nosso futuro.”— Clark R. Chapman", text_color="black", font=("Aharoni", 18, "bold")).place(x=100, y=80)

# --- LOGOS REDES SOCIAIS ---
def add_logo(nome, x, y, callback, size=(35, 35)):
    img = Image.open(img_path(nome)).resize(size)
    photo = ImageTk.PhotoImage(img)
    label = ctk.CTkLabel(down_bar, image=photo, text="")
    label.image = photo
    label.place(x=x, y=y)
    label.bind("<Button-1>", lambda e: callback())
    label.configure(cursor="hand2")

add_logo("nasa.png", 1390, 15, open_nasa)
add_logo("insta.png", 1419, 15, open_insta)
add_logo("twitter.png", 1450, 15, open_twitter, size=(35, 30))
add_logo("facebook.png", 1480, 15, open_facebook)
add_logo("linkedin.png", 1505, 14, open_linkedin, size=(38, 38))

app.mainloop()
