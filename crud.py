import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
from main import get_connection,img_path,open_insta, open_nasa, open_twitter, open_facebook, open_linkedin
import sys

# Pega o nome do usuário passado pelo login
if len(sys.argv) > 1:
    nome_usuario = sys.argv[1]
else:
    nome_usuario = "Usuário"


# =========================
# CONFIGURAÇÕES
# =========================
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1600x800")
app.title("Asteroides – dbo.dados")

#Imagem de fundo
screen_width = 2000
screen_height = 1000
bg_image = Image.open(img_path("fundologs.jpg")).resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = ctk.CTkCanvas(app, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

pagina_atual = 0
total_paginas = 1

# =========================
# TOP BAR
# =========================
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0)

# LOGO
image = Image.open(img_path("logo.png")).resize((100, 100))
photo = ImageTk.PhotoImage(image)
logo_label = ctk.CTkLabel(top_bar, image=photo, text="")
logo_label.place(x=30, y=8)
logo_label.image = photo

# TÍTULO
login_title = ctk.CTkLabel(
    top_bar,
    text="Visualização de Dados de Asteroides",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF",
    fg_color=None  
)
login_title.place(x=125, y=15)

image = Image.open(img_path("iconeusuario.png")).resize((30, 30))
photo_user = ImageTk.PhotoImage(image)
user_icon = ctk.CTkLabel(top_bar, image=photo_user, text="")
user_icon.place(x=1400, y=30)
user_icon.image = photo_user
user_icon.configure(cursor="hand2")

# Menu suspenso
menu = tk.Menu(app, tearoff=0)
menu.add_command(label=f"Olá, {nome_usuario}", state="disabled")
menu.add_separator()
menu.add_command(label="Abrir User", command=lambda: abrir_user())
menu.add_command(label="Logout", command=lambda: logout())

# Funções
def abrir_user():
    import subprocess, sys
    app.destroy()  # ou apenas abrir sem fechar o CRUD, se quiser
    # Passa o usuário logado como argumento
    subprocess.Popen([sys.executable, "user.py", nome_usuario])


def logout():
    import subprocess, sys
    app.destroy()
    subprocess.Popen([sys.executable, "login.py"])

def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

user_icon.bind("<Button-1>", show_menu)



# =========================
# TREEVIEW + SCROLLBARS
# =========================
columns = (
    "Name_Neo", "h", "albedo", "diameter", "diameter_sigma",
    "pha", "neo", "epoch_cal", "sigma_i", "i", "epoch",
    "e", "sigma_e", "moid_ld", "rms", "a", "sigma_a",
    "q", "sigma_q", "tp_cal", "sigma_tp",
    "Arc", "Opp", "Computer", "Obs", "Mean_Anomaly"
)

frame_table = ctk.CTkFrame(app)
frame_table.pack(pady=(0, 0), fill="x", expand=True)  # ajustado para não sobrepor top_bar

scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    height=18,
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

tree.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

for col in columns:
    tree.heading("Name_Neo", text="Nome")
    tree.heading("h", text="H(mag)")
    tree.heading("albedo", text="albedo")
    tree.heading("diameter", text="diameter(km)")
    tree.heading("diameter_sigma", text="diameter_sigma(km)")
    tree.heading("pha", text="pha")
    tree.heading("neo", text="neo")
    tree.heading("epoch_cal", text="epoch_cal(date)")
    tree.heading("i", text="i(°)")
    tree.heading("sigma_i", text="sigma_i(°)")
    tree.heading("epoch", text="epoch(JD)")
    tree.heading("e", text="e")
    tree.heading("sigma_e", text="sigma_e")
    tree.heading("moid_ld", text="moid_ld(LD)")
    tree.heading("rms", text="rms")
    tree.heading("a", text="a(AU)")
    tree.heading("sigma_a", text="sigma_a(AU)")
    tree.heading("q", text="q(AU)")
    tree.heading("sigma_q", text="sigma_q(AU)")
    tree.heading("tp_cal", text="tp_cal(data)")
    tree.heading("sigma_tp", text="sigma_tp(JD)")
    tree.heading("Arc", text="Arc(years)")
    tree.heading("Opp", text="Opp")
    tree.heading("Computer", text="Computer(text)")
    tree.heading("Obs", text="Obs")
    tree.heading("Mean_Anomaly", text="M(°)")


# =========================
# ESTILO MODERNO TREEVIEW
# =========================
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#F4F4F4",
                foreground="black",
                rowheight=30,
                fieldbackground="#F4F4F4",
                font=("Segoe UI", 11))

style.configure("Treeview.Heading",
                background="#0C1B33",
                foreground="#E2DFDF",
                font=("Aharoni", 12, "bold"))

style.map("Treeview",
          background=[("selected", "#347083")],
          foreground=[("selected", "white")])

tree.tag_configure('linha_par', background='#FFFFFF')
tree.tag_configure('linha_impar', background='#E6F0FF')

# =========================
# BARRA DE PESQUISA (ABAIXO DA TABELA)
# =========================
frame_search = ctk.CTkFrame(app, fg_color="white", width=400, height=50, corner_radius=10)
frame_search.place(x=1050, y=650)

# Label dentro do frame
ctk.CTkLabel(frame_search, text="Pesquisar:",text_color='black').grid(row=0, column=0, padx=10, pady=10)

# Entry com fundo branco para combinar
entry_search = ctk.CTkEntry(frame_search, width=200, fg_color="grey90", border_width=1, corner_radius=5,text_color="black")
entry_search.grid(row=0, column=1, padx=10, pady=10)


ctk.CTkLabel(frame_search, text="Mostrar:",text_color='black').grid(row=0, column=2, padx=10)
combo_limit = ttk.Combobox(frame_search, values=[10, 50, 100, 500], width=10)
combo_limit.current(0)
combo_limit.grid(row=0, column=3, padx=10)

# =========================
# PAGINAÇÃO (RODAPÉ)
# =========================
frame_pag = ctk.CTkFrame(app)
frame_pag = ctk.CTkFrame(app,fg_color='white', width=1600, height=40) 
frame_pag.place(x=500, y=720)


label_pagina = ctk.CTkLabel(frame_pag, text="Página 1/1", text_color='black')
label_pagina.grid(row=0, column=1, padx=20)

def proxima_pagina():
    global pagina_atual
    if pagina_atual < total_paginas - 1:
        pagina_atual += 1
        atualizar_lista()

def pagina_anterior():
    global pagina_atual
    if pagina_atual > 0:
        pagina_atual -= 1
        atualizar_lista()

ctk.CTkButton(frame_pag, text="Anterior", command=pagina_anterior).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_pag, text="Próxima", command=proxima_pagina).grid(row=0, column=2, padx=10)

# =========================
# FUNÇÃO DE ATUALIZAÇÃO
# =========================
def atualizar_lista():
    global total_paginas, pagina_atual

    termo = entry_search.get()
    limit = int(combo_limit.get())
    offset = pagina_atual * limit

    conn = get_connection()
    cursor = conn.cursor()

    # Conta total de registros
    cursor.execute("""
        SELECT COUNT(*)
        FROM dbo.dados
        WHERE Name_Neo LIKE ?
    """, (f"%{termo}%",))

    total_registros = cursor.fetchone()[0]
    total_paginas = max(1, (total_registros + limit - 1) // limit)

    if pagina_atual >= total_paginas:
        pagina_atual = total_paginas - 1

    # Busca dados
    cursor.execute("""
        SELECT
            Name_Neo, h, albedo, diameter, diameter_sigma,
            pha, neo, epoch_cal, sigma_i, i, epoch,
            e, sigma_e, moid_ld, rms, a, sigma_a,
            q, sigma_q, tp_cal, sigma_tp,
            Arc, Opp, Computer, Obs, Mean_Anomaly_MPCORB
        FROM dbo.dados
        WHERE Name_Neo LIKE ?
        ORDER BY Name_Neo
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """, (f"%{termo}%", offset, limit))

    rows = cursor.fetchall()
    conn.close()

    # Limpa tabela
    tree.delete(*tree.get_children())

    for i, row in enumerate(rows):
        # Formata cada campo
        formatted_row = []
        for value in row:
            if value is None:
                formatted_row.append("")          # substitui None por vazio
            elif isinstance(value, float):
                formatted_row.append(f"{value:.3f}")  # 3 casas decimais para floats
            else:
                formatted_row.append(str(value))  # converte tudo para string limpa

        tag = 'linha_par' if i % 2 == 0 else 'linha_impar'
        tree.insert("", "end", values=formatted_row, tags=(tag,))

    label_pagina.configure(text=f"Página {pagina_atual + 1}/{total_paginas}")


# =========================
# START
# =========================
entry_search.bind("<KeyRelease>", lambda e: atualizar_lista())
combo_limit.bind("<<ComboboxSelected>>", lambda e: atualizar_lista())

atualizar_lista()

down_bar = ctk.CTkFrame(app, width=2000, height=50, fg_color="#B4AEAE")
down_bar.place(x=0, y=750)

mencao = ctk.CTkLabel(
    down_bar,
    text="@Adriana Abreu & Leonor Rebola",
    text_color="black",
    font=("Aharoni", 12),
    fg_color="transparent"
)
mencao.place(x=20, y=20)

# --- IMAGENS LOGOS ---

# Nasa
nasa = Image.open(img_path("nasa.png")).resize((35, 35))
photonasa = ImageTk.PhotoImage(nasa)
nasa_label = ctk.CTkLabel(down_bar, image=photonasa, text="")
nasa_label.place(x=1390, y=15)
nasa_label.image = photonasa
nasa_label.bind("<Button-1>", lambda e: open_nasa())
nasa_label.configure(cursor="hand2")  # cursor de clique

# Instagram
insta = Image.open(img_path("insta.png")).resize((35, 35))
photoinsta = ImageTk.PhotoImage(insta)
insta_label = ctk.CTkLabel(down_bar, image=photoinsta, text="")
insta_label.place(x=1419, y=15)
insta_label.image = photoinsta
insta_label.bind("<Button-1>", lambda e: open_insta())
insta_label.configure(cursor="hand2")

# Twitter
twitter = Image.open(img_path("twitter.png")).resize((35, 30))
phototwitter = ImageTk.PhotoImage(twitter)
twitter_label = ctk.CTkLabel(down_bar, image=phototwitter, text="")
twitter_label.place(x=1450, y=15)
twitter_label.image = phototwitter
twitter_label.bind("<Button-1>", lambda e: open_twitter())
twitter_label.configure(cursor="hand2")

# Facebook
facebook = Image.open(img_path("facebook.png")).resize((35, 35))
photofacebook = ImageTk.PhotoImage(facebook)
facebook_label = ctk.CTkLabel(down_bar, image=photofacebook, text="")
facebook_label.place(x=1480, y=15)
facebook_label.image = photofacebook
facebook_label.bind("<Button-1>", lambda e: open_facebook())
facebook_label.configure(cursor="hand2")

# LinkedIn
linkedin = Image.open(img_path("linkedin.png")).resize((38, 38))
photolinkedin = ImageTk.PhotoImage(linkedin)
linkedin_label = ctk.CTkLabel(down_bar, image=photolinkedin, text="")
linkedin_label.place(x=1505, y=14)
linkedin_label.image = photolinkedin
linkedin_label.bind("<Button-1>", lambda e: open_linkedin())
linkedin_label.configure(cursor="hand2")
app.mainloop()
