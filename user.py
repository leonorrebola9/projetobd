import customtkinter as ctk
from tkinter import messagebox
from main import get_connection, img_path, open_insta, open_nasa, open_twitter, open_facebook, open_linkedin
from PIL import Image
import sys
import subprocess
import os

# =========================
# RECEBER UTILIZADOR
# =========================
if len(sys.argv) > 1:
    nome_usuario = sys.argv[1]
else:
    messagebox.showerror("Erro", "Usuário não informado")
    sys.exit()

# =========================
# CONFIGURAÇÕES
# =========================
ctk.set_appearance_mode("Dark")
app = ctk.CTk()
app.geometry("1600x800")
app.title("Asteroides – Editar Usuário")

# =========================
# BACKGROUND
# =========================
bg_img = Image.open(img_path("fundologs.jpg")).resize((1600, 800))
bg_photo = ctk.CTkImage(bg_img, size=(1600, 800))

bg_label = ctk.CTkLabel(app, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# =========================
# TOP BAR
# =========================
top_bar = ctk.CTkFrame(app, height=80, fg_color="#0C1B33", corner_radius=0)
top_bar.place(x=0, y=0, relwidth=1)

logo_img = Image.open(img_path("logo.png")).resize((60, 60))
logo = ctk.CTkImage(logo_img, size=(60, 60))
ctk.CTkLabel(top_bar, image=logo, text="").place(x=30, y=10)

ctk.CTkLabel(
    top_bar,
    text="Editar Usuário",
    font=("Aharoni", 40, "bold"),
    text_color="#E2DFDF",
    fg_color="transparent"
).place(x=125, y=15)

def voltar():
    app.destroy()
    voltar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crud.py")
    subprocess.Popen([sys.executable, voltar_path])

ctk.CTkButton(
    top_bar,
    text="← Voltar",
    width=100,
    height=40,
    fg_color="#34495E",
    hover_color="#2C3E50",
    font=("Arial", 14, "bold"),
    command=voltar
).place(x=1400, y=20)

# =========================
# CAMPOS
# =========================
fields = {}

def campo(label, key, x, y, show=None):
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.place(x=x, y=y)

    ctk.CTkLabel(
        frame,
        text=label,
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color="transparent",
        width=120,
        anchor="w"
    ).pack(side="left", padx=(0, 10))

    entry = ctk.CTkEntry(
        frame,
        width=300,
        height=28,
        fg_color="#1E1E1E",
        text_color="white",
        border_color="#444444",
        show=show
    )
    entry.pack(side="left")
    fields[key] = entry

x = 550
y = 220
gap = 50

campo("Nome", "name", x, y)
campo("Sobrenome", "surname", x, y + gap)
campo("Usuário", "user", x, y + gap*2)
campo("Senha", "passw", x, y + gap*3, show="*")

# =========================
# CARREGAR DADOS
# =========================
def carregar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, surname, [user], passw FROM users WHERE [user]=?", (nome_usuario,))
    d = cur.fetchone()
    conn.close()

    if not d:
        messagebox.showerror("Erro", "Usuário não encontrado")
        app.destroy()
        return

    fields["name"].insert(0, d[0])
    fields["surname"].insert(0, d[1])
    fields["user"].insert(0, d[2])
    fields["passw"].insert(0, d[3])

# =========================
# ATUALIZAR
# =========================
def atualizar():
    n, s, u, p = (fields[k].get() for k in fields)

    if not all([n, s, u, p]):
        messagebox.showwarning("Aviso", "Preencha todos os campos")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET name=?, surname=?, [user]=?, passw=?
        WHERE [user]=?
    """, (n, s, u, p, nome_usuario))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Dados atualizados")
    app.destroy()

ctk.CTkButton(
    app,
    text="Guardar Alterações",
    command=atualizar,
    fg_color="#27AE60",
    hover_color="#1E8449",
    width=280,
    height=45,
    font=("Arial", 16, "bold")
).place(x=660, y=y + gap*4 + 20)

# =========================
# DOWN BAR
# =========================
down = ctk.CTkFrame(app, height=60, fg_color="#B4AEAE", corner_radius=0)
down.place(x=0, y=740, relwidth=1)

ctk.CTkLabel(
    down,
    text="@Adriana Abreu & Leonor Rebola",
    text_color="black",
    font=("Aharoni", 14, "bold"),
    fg_color="transparent"
).place(x=20, y=15)

def social(img, x, cmd):
    im = Image.open(img_path(img)).resize((30, 30))
    ph = ctk.CTkImage(im, size=(30, 30))
    lbl = ctk.CTkLabel(down, image=ph, text="", fg_color="transparent")
    lbl.place(x=x, y=15)
    lbl.bind("<Button-1>", lambda e: cmd())

social("nasa.png", 1350, open_nasa)
social("insta.png", 1400, open_insta)
social("twitter.png", 1450, open_twitter)
social("facebook.png", 1500, open_facebook)
social("linkedin.png", 1550, open_linkedin)

carregar()
app.mainloop()