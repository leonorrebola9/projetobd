import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import tkinter as tk
from main import get_connection, img_path
import sys
import subprocess
import os



# =========================
# USUÁRIO LOGADO
# =========================
if len(sys.argv) >= 3:
    nome_completo = sys.argv[1]
    usuario = sys.argv[2]
else:
    nome_completo = "Usuário"
    usuario = ""

# =========================
# CONFIGURAÇÕES GERAIS
# =========================
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1600x800")
app.title("Asteroides – vw_App_Completa")

# =========================
# BACKGROUND
# =========================
bg_image = Image.open(img_path("fundologs.jpg")).resize((2000, 1000))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = ctk.CTkCanvas(app, width=2000, height=1000, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

pagina_atual = 0
total_paginas = 1

# =========================
# TOP BAR
# =========================
top_bar = ctk.CTkFrame(app, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0, relwidth=1)

logo = ImageTk.PhotoImage(Image.open(img_path("logo.png")).resize((100, 100)))
ctk.CTkLabel(top_bar, image=logo, text="").place(x=30, y=8)

ctk.CTkLabel(
    top_bar,
    text="Visualização de Asteroides",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF"
).place(x=125, y=15)

# =========================
# ÍCONE DE USUÁRIO NA TOP BAR
# =========================
user_icon_image = ImageTk.PhotoImage(Image.open(img_path("iconeusuario.png")).resize((50, 50)))

def open_configurations():
    app.destroy()
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user.py")
    subprocess.Popen([sys.executable, conf_path, usuario])

def logout():
    app.destroy()  # fecha a aplicação

# Criar menu suspenso usando tk.Menu
menu_usuario = tk.Menu(app, tearoff=0)
menu_usuario.add_command(label=nome_completo, state="disabled")  # só exibe o nome
menu_usuario.add_separator()
menu_usuario.add_command(label="Configurações", command=open_configurations)
menu_usuario.add_command(label="Logout", command=logout)

# Botão com ícone que dispara o menu
def mostrar_menu_usuario(event):
    try:
        menu_usuario.tk_popup(event.x_root, event.y_root)
    finally:
        menu_usuario.grab_release()

btn_user = ctk.CTkButton(
    top_bar,
    image=user_icon_image,
    text="",
    width=50,
    height=50,
    fg_color="#0C1B33",
    hover_color="#162B4C",
    corner_radius=25
)
btn_user.place(x=1450, y=15)  # ajuste a posição conforme necessário
btn_user.bind("<Button-1>", mostrar_menu_usuario)

# =========================
# TREEVIEW
# =========================
columns = (
    "Asteroid_ID",  # OCULTO
    "Nome", "Diametro", "Incerteza_Diametro", "Magnitude", "Albedo",
    "PHA", "NEO", "epoch_cal",
    "Distancia_Minima_Terra", "RMS", "Excentricidade", "Eixo_Semimaior",
    "Perielio", "Inclinacao", "Anomalia_Media", "tp_cal", "Epoch",
    "Status_Alerta", "Prioridade_Alerta", "Escala_Torino",
    "Data_Aproximacao", "Descricao_Risco",
    "Total_Sessoes", "Total_Imagens", "Maior_Arco_Dias",
    "Lista_Equipamentos", "Lista_Softwares",
    "Equipa_Astronomos", "Centros_Observacao"
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

# =========================
# HEADINGS (SEM ID)
# =========================
headings = {
    "Nome": "Nome",
    "Diametro": "Diâmetro (km)",
    "Incerteza_Diametro": "Diâmetro Inc. (km)",
    "Magnitude": "H",
    "Albedo": "Albedo",
    "PHA": "PHA",
    "NEO": "NEO",
    "epoch_cal": "Epoch",
    "Distancia_Minima_Terra": "MOID (LD)",
    "RMS": "RMS",
    "Excentricidade": "e",
    "Eixo_Semimaior": "a (AU)",
    "Perielio": "q (AU)",
    "Inclinacao": "i (°)",
    "Anomalia_Media": "M (°)",
    "tp_cal": "tp",
    "Epoch": "Época",
    "Status_Alerta": "Status",
    "Prioridade_Alerta": "Prioridade",
    "Escala_Torino": "Torino",
    "Data_Aproximacao": "Aproximação",
    "Descricao_Risco": "Descrição",
    "Total_Sessoes": "Sessões",
    "Total_Imagens": "Imagens",
    "Maior_Arco_Dias": "Arco Máx.",
    "Lista_Equipamentos": "Equipamentos",
    "Lista_Softwares": "Softwares",
    "Equipa_Astronomos": "Astrónomos",
    "Centros_Observacao": "Centros"
}

for col, text in headings.items():
    tree.heading(col, text=text)

# =========================
# ESTILO
# =========================
style = ttk.Style()
style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Aharoni", 11, "bold"))

tree.tag_configure('par', background='#FFFFFF')
tree.tag_configure('impar', background='#E6F0FF')

# =========================
# PESQUISA + PAGINAÇÃO
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
# FUNÇÕES
# =========================
def atualizar_lista():
    global pagina_atual, total_paginas

    termo = entry_search.get()
    limit = int(combo_limit.get())
    offset = pagina_atual * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM vw_App_Completa
        WHERE Nome LIKE ?
    """, (f"%{termo}%",))
    total = cursor.fetchone()[0]
    total_paginas = max(1, (total + limit - 1) // limit)

    cursor.execute("""
        SELECT *
        FROM vw_App_Completa
        WHERE Nome LIKE ?
        ORDER BY Nome
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """, (f"%{termo}%", offset, limit))

    rows = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())

    for i, row in enumerate(rows):
        valores = [
            "" if v is None else f"{v:.3f}" if isinstance(v, float) else str(v)
            for v in row
        ]
        tree.insert("", "end", values=valores, tags=('par' if i % 2 == 0 else 'impar'))

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
    if not item:
        return None
    return tree.item(item)["values"][0]

def apagar_asteroide():
    asteroid_id = get_asteroid_id_selecionado()

    if asteroid_id is None:
        messagebox.showwarning("Aviso", "Selecione um asteroide.")
        return

    if not messagebox.askyesno(
        "Confirmar eliminação",
        "Esta ação irá apagar TODA a informação do asteroide.\n\nDeseja continuar?"
    ):
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

    if asteroid_id is None:
        messagebox.showwarning("Aviso", "Selecione um asteroide para alterar.")
        return

    # Caminho absoluto para o script alterar.py
    alterar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alterar.py")
    
    # Abrir o script de alteração passando o ID do asteroide
    subprocess.Popen([sys.executable, alterar_path, str(asteroid_id)])


ctk.CTkButton(frame_pag, text="Anterior", command=pagina_anterior).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_pag, text="Próxima", command=proxima_pagina).grid(row=0, column=2, padx=10)

entry_search.bind("<KeyRelease>", lambda e: atualizar_lista())
combo_limit.bind("<<ComboboxSelected>>", lambda e: atualizar_lista())

# =========================
# BOTÃO ELIMINAR
# =========================
frame_actions = ctk.CTkFrame(app, fg_color="transparent")
frame_actions.place(x=100, y=650)

ctk.CTkButton(
    frame_actions,
    text="Criar",
    width=140,
    fg_color="#27AE60",
    hover_color="#1E8449",
    command=lambda: open_criar()
).grid(row=0, column=0, padx=10)

ctk.CTkButton(
    frame_actions,
    text="Alterar",
    width=140,
    fg_color="#F1C40F",
    hover_color="#D4AC0D",
    command=alterar_asteroide
).grid(row=0, column=2, padx=10)


ctk.CTkButton(
    frame_actions,
    text="Eliminar",
    width=140,
    fg_color="#C0392B",
    hover_color="#922B21",
    command=apagar_asteroide
).grid(row=0, column=1, padx=10)

def open_criar():
    app.destroy()
    criar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "criar.py")
    subprocess.Popen([sys.executable, criar_path])


# =========================
# INICIAR
# =========================
atualizar_lista()
app.mainloop()
