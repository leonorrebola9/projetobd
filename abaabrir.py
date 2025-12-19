import sys
import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess  # ← import necessário
import os
from main import img_path

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

# --- CARREGAR E REDIMENSIONAR IMAGEM ---
screen_width = 1920
screen_height = 1080
bg_image = Image.open(img_path("fundo01.jpg")).resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

# --- CANVAS ---
canvas = ctk.CTkCanvas(app, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# --- TEXTO SOBRE A IMAGEM ---
text_y = screen_height // 2 - 50
canvas.create_text(screen_width // 2, text_y, text="Bem Vindo", font=("Comic Sans MS", 50, "bold"), fill="white")

# --- FUNÇÃO DO BOTÃO ---
def open_login():
    app.destroy()
    login_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login.py")
    subprocess.Popen([sys.executable, login_path])


# --- BOTÃO COM ANIMAÇÃO DE CRESCIMENTO ---
final_width = 200
final_height = 50
final_font_size = 20

entrar_btn = ctk.CTkButton(
    app,
    text="Entrar",
    width=1,
    height=1,
    corner_radius=15,
    fg_color="#1E5EFF",
    hover_color="#1C4DE8",
    font=("Comic Sans MS", 1, "bold"),
    command=open_login  # ← ligação para login.py
)
entrar_btn.place(x=screen_width//2, y=text_y + 80, anchor="n")

# --- FUNÇÃO DE ANIMAÇÃO ---
current_width = 1
current_height = 1
current_font = 1
step = 8

def animate_button():
    global current_width, current_height, current_font
    if current_width < final_width:
        current_width += step
        current_height += int(step/4)
        if current_width > final_width:
            current_width = final_width
        if current_height > final_height:
            current_height = final_height
        current_font += 1
        if current_font > final_font_size:
            current_font = final_font_size

        entrar_btn.configure(width=current_width, height=current_height, font=("Comic Sans MS", current_font, "bold"))
        entrar_btn.place(x=760,y=450, anchor="n")
        app.after(20, animate_button)

# Inicia a animação
app.after(500, animate_button)

app.mainloop()




