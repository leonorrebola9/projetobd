import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import tkinter as tk
import sys, subprocess, os
from main import get_connection, img_path
from graficos import gerar_grafico_prioridade, gerar_grafico_neo_pha, gerar_grafico_risco_colisao


#definir variaveis para o user

if len(sys.argv) >= 3:
    nome_completo = sys.argv[1]
    usuario = sys.argv[2]
else:
    nome_completo = "Usuário"
    usuario = ""


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


#Tamanho da janela
app = ctk.CTk()
app.geometry("1600x800")
app.title("Asteroides – Tabela Completa")

#Imagem de fundo
screen_width = 2000
screen_height = 1000
bg_image = Image.open(img_path("fundologs.jpg")).resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = ctk.CTkCanvas(app, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# ---------------------------------------------
# --- TOP BAR -----------------------------
#---------------------------------------------
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0)


#LOGO
image = Image.open(img_path("logo.png")).resize((100, 100))
photo = ImageTk.PhotoImage(image)

logo_label = ctk.CTkLabel(top_bar, image=photo, text="")
logo_label.place(x=30, y=8)
logo_label.image = photo

ctk.CTkLabel(
    top_bar,
    text="Visualização de Asteroides",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF"
).place(x=125, y=15)

#--------------------------------------------------------------------------------------
#menu de utilizador 

user_icon = CTkImage(
    light_image=Image.open(img_path("iconeusuario.png")),
    dark_image=Image.open(img_path("iconeusuario.png")),
    size=(50, 50)
)

# Funções do menu de utilizador
def open_configurations():
    app.destroy()
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user.py")
    subprocess.Popen([sys.executable, conf_path, usuario])

def logout():
    app.destroy()

# Menu
menu_usuario = tk.Menu(app, tearoff=0)
menu_usuario.add_command(label=nome_completo, state="disabled")
menu_usuario.add_separator()
menu_usuario.add_command(label="Configurações", command=open_configurations)
menu_usuario.add_command(label="Logout", command=logout)

def mostrar_menu_usuario(event):
    try:
        menu_usuario.tk_popup(event.x_root, event.y_root)
    finally:
        menu_usuario.grab_release()

btn_user = ctk.CTkButton(
    top_bar,
    image=user_icon,
    text="",
    width=50,
    height=50,
    fg_color="#0C1B33",
    hover_color="#162B4C",
    corner_radius=25
)
btn_user.place(x=1350, y=15)
btn_user.bind("<Button-1>", mostrar_menu_usuario)


#--------------------------------------------------------------------------------------
#menu de gráficos
grafico_icon = CTkImage(
    light_image=Image.open(img_path("menu.png")),
    size=(50,50)
)

# menu 
menu_graficos = tk.Menu(app, tearoff=0)
menu_graficos.add_command(label="Gráfico por Prioridade", command=gerar_grafico_prioridade)
menu_graficos.add_command(label="Gráfico NEO/PHA", command=gerar_grafico_neo_pha)
menu_graficos.add_command(label="Asteroides com maior risco", command=lambda: gerar_grafico_risco_colisao(10))

# Função menu
def mostrar_menu_graficos(event):
    try:
        menu_graficos.tk_popup(event.x_root, event.y_root)
    finally:
        menu_graficos.grab_release()

# Botão do ícone de gráficos na topbar
btn_graficos = ctk.CTkButton(
    top_bar,
    image=grafico_icon,
    text="",
    width=50,
    height=50,
    fg_color="#0C1B33",
    hover_color="#162B4C",
    corner_radius=25
)
btn_graficos.place(x=1450, y=15)  # posição ajustável
btn_graficos.bind("<Button-1>", mostrar_menu_graficos)
#--------------------------------------------------------------------------------------

pagina_atual = 0
total_paginas = 1


# =========================
# TREEVIEW
# =========================
columns = (
    "Asteroid_ID", "full_name", "diameter", "diameter_sigma", "H", "albedo",
    "pha", "neo", "epoch_cal", "moid_ld", "rms", "e", "a", "q", "i", "M",
    "tp_cal", "Epoch", "status", "Priority", "Torino", "dap", "description",
    "Observation_ID", "num_obs", "arc", "namee", "Computer", "name", "namec"
)

frame_table = ctk.CTkFrame(app)
frame_table.pack(pady=(90, 0), fill="x")

scroll_y = ttk.Scrollbar(frame_table, orient="vertical")
scroll_x = ttk.Scrollbar(frame_table, orient="horizontal")

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    height=19,
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
tree.column("Asteroid_ID", width=0, stretch=False)

headings = {
    "full_name": "Nome", "diameter": "Diâmetro (km)", "diameter_sigma": "Diâmetro Inc. (km)",
    "H": "H", "albedo": "Albedo", "pha": "PHA", "neo": "NEO", "epoch_cal": "Epoch",
    "moid_ld": "MOID (LD)", "rms": "RMS", "e": "e", "a": "a (AU)", "q": "q (AU)",
    "i": "i (°)", "M": "M (°)", "tp_cal": "tp", "Epoch": "Época", "status": "Status",
    "Priority": "Prioridade", "Torino": "Torino", "dap": "Aproximação",
    "description": "Descrição", "Observation_ID": "Sessões", "num_obs": "Imagens",
    "arc": "Arco Máx.", "namee": "Equipamentos", "Computer": "Softwares",
    "name": "Astrónomos", "namec": "Centros"
}
for col in tree["columns"]:
    tree.heading(col, text=headings.get(col, col))

# =========================
# ESTILO
# =========================
style = ttk.Style()
style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Aharoni", 11, "bold"))
tree.tag_configure('par', background='#FFFFFF')
tree.tag_configure('impar', background='#E6F0FF')

# =========================
# FUNÇÕES DE PAGINAÇÃO E PESQUISA
# =========================
frame_search = ctk.CTkFrame(app, fg_color="white", corner_radius=10)
frame_search.place(x=1000, y=650)
ctk.CTkLabel(frame_search, text="Pesquisar Nome:", text_color="black").grid(row=0, column=0, padx=10)
entry_search = ctk.CTkEntry(frame_search, width=200)
entry_search.grid(row=0, column=1, padx=10)
ctk.CTkLabel(frame_search, text="Mostrar:", text_color="black").grid(row=0, column=2)
combo_limit = ttk.Combobox(frame_search, values=[10, 50, 100, 500], width=8)
combo_limit.current(0)
combo_limit.grid(row=0, column=3, padx=10)

frame_pag = ctk.CTkFrame(app, fg_color="white")
frame_pag.place(x=600, y=720)
label_pagina = ctk.CTkLabel(frame_pag, text="Página 1/1", text_color="black")
label_pagina.grid(row=0, column=1, padx=20)

# =========================
# FUNÇÕES CRUD
# =========================
def formatar_valores(row):
    return ["" if v is None else f"{v:.3f}" if isinstance(v, float) else str(v) for v in row]

def atualizar_lista():
    global pagina_atual, total_paginas
    termo = entry_search.get()
    limit = int(combo_limit.get())
    offset = pagina_atual * limit

    conn = get_connection()
    cursor = conn.cursor()

    # Substituir 'Nome' por 'full_name'
    cursor.execute("SELECT COUNT(*) FROM vw_App_Completa WHERE full_name LIKE ?", (f"%{termo}%",))
    total = cursor.fetchone()[0]
    total_paginas = max(1, (total + limit - 1) // limit)

    cursor.execute("""
        SELECT * FROM vw_App_Completa
        WHERE full_name LIKE ?
        ORDER BY full_name
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """, (f"%{termo}%", offset, limit))

    rows = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tree.insert("", "end", values=formatar_valores(row), tags=('par' if i % 2 == 0 else 'impar'))

    label_pagina.configure(text=f"Página {pagina_atual + 1}/{total_paginas}")


def pagina_anterior():
    global pagina_atual
    if pagina_atual > 0:
        pagina_atual -= 1
        atualizar_lista()

def proxima_pagina():
    global pagina_atual
    if pagina_atual < total_paginas - 1:
        pagina_atual += 1
        atualizar_lista()

def get_asteroid_id_selecionado():
    item = tree.focus()
    return tree.item(item)["values"][0] if item else None

def apagar_asteroide():
    asteroid_id = get_asteroid_id_selecionado()
    if asteroid_id is None: return messagebox.showwarning("Aviso", "Selecione um asteroide.")
    if not messagebox.askyesno("Confirmar eliminação",
                               "Esta ação irá apagar TODA a informação do asteroide.\n\nDeseja continuar?"):
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC SP_ApagarAsteroid ?", asteroid_id)
    conn.commit()
    conn.close()
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Asteroide eliminado com sucesso.")

def alterar_asteroide():
    asteroid_id = get_asteroid_id_selecionado()
    if asteroid_id is None: return messagebox.showwarning("Aviso", "Selecione um asteroide para alterar.")
    alterar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alterar.py")
    subprocess.Popen([sys.executable, alterar_path, str(asteroid_id)])

def open_criar():
    app.destroy()
    criar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "criar.py")
    subprocess.Popen([sys.executable, criar_path])

# =========================
# BOTOES PAGINAÇÃO
# =========================
ctk.CTkButton(frame_pag, text="Anterior", command=pagina_anterior).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_pag, text="Próxima", command=proxima_pagina).grid(row=0, column=2, padx=10)
entry_search.bind("<KeyRelease>", lambda e: atualizar_lista())
combo_limit.bind("<<ComboboxSelected>>", lambda e: atualizar_lista())

# =========================
# BOTOES CRUD
# =========================
frame_actions = ctk.CTkFrame(app, fg_color="transparent")
frame_actions.place(x=100, y=650)
ctk.CTkButton(frame_actions, text="Criar", width=140, fg_color="#27AE60",
               hover_color="#1E8449", command=open_criar).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_actions, text="Eliminar", width=140, fg_color="#C0392B",
               hover_color="#922B21", command=apagar_asteroide).grid(row=0, column=1, padx=10)
ctk.CTkButton(frame_actions, text="Alterar", width=140, fg_color="#F1C40F",
               hover_color="#D4AC0D", command=alterar_asteroide).grid(row=0, column=2, padx=10)

# =========================
# INICIAR
# =========================
atualizar_lista()
app.mainloop()
