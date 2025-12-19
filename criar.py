import customtkinter as ctk
from tkinter import messagebox
from main import get_connection, img_path, open_insta, open_nasa, open_twitter, open_facebook, open_linkedin
from PIL import Image, ImageTk
import sys
import subprocess

# =========================
# CONFIGURAÇÕES E ESTADO
# =========================
if len(sys.argv) >= 3:
    nome_completo = sys.argv[1]
    usuario = sys.argv[2]
else:
    nome_completo = "Usuário"
    usuario = ""

ctk.set_appearance_mode("Dark")
app = ctk.CTk()
app.geometry("1600x800")
app.title("Asteroides – vw_App_Completa")

# =========================
# BACKGROUND (SUBSTITUINDO CANVAS POR LABEL)
# =========================
# Usar CTkLabel para o fundo permite transparência real nos widgets sobrepostos
bg_img = Image.open(img_path("fundologs.jpg")).resize((1600, 800))
bg_photo = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(1600, 800))

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
    text="Criar Asteroide",
    font=("Aharoni", 40, "bold"),
    text_color="#E2DFDF",
    fg_color="transparent"
).place(x=125, y=15)

def voltar():
    app.destroy()  # fecha a janela atual
    subprocess.Popen([sys.executable, "crud.py"])  # abre o crud.py no mesmo interpretador Python

voltar_btn = ctk.CTkButton(
    top_bar,
    text="← Voltar",
    width=100,
    height=40,
    fg_color="#34495E",
    hover_color="#2C3E50",
    font=("Arial", 14, "bold"),
    command=voltar
)
voltar_btn.place(x=1400, y=20)

# =========================
# FUNÇÃO DE CRIAÇÃO (COM TRANSPARÊNCIA REAL)
# =========================
fields = {}

def criar_label_entry(texto, x_pos, y_pos):
    # O container DEVE ter fg_color="transparent"
    container = ctk.CTkFrame(app, fg_color="transparent")
    container.place(x=x_pos, y=y_pos)

    # Agora a label será 100% transparente sobre a imagem
    label = ctk.CTkLabel(
        container, 
        text=texto, 
        font=("Arial", 12, "bold"), 
        text_color="white",
        fg_color="transparent",
        width=150,
        anchor="w"
    )
    label.pack(side="left", padx=(0, 10))

    entry = ctk.CTkEntry(
        container, 
        width=180, 
        height=28, 
        fg_color="#1E1E1E", 
        text_color="white", 
        border_color="#444444"
    )
    entry.pack(side="left")
    
    return entry

# Posicionamento
spacing_y = 42  
y_inicial = 130 
col1_x = 200
col2_x = 750

y = y_inicial

# Listagem de campos organizada
itens = [
    ("Nome", "Diametro_Inc", "Diâmetro Inc. (km)"),
    ("Diametro", "Magnitude", "Magnitude (H)"),
    ("Albedo", "PHA", "PHA (Y/N)"),
    ("NEO", "Epoch", "Epoch"),
    ("e", "a", "a (AU)"),
    ("q", "i", "i (°)"),
    ("M", "tp", "tp"),
    ("MOID", "RMS", "RMS"),
    ("Descricao", "Sessoes", "Sessões"),
    ("Imagens", "Arco_Max", "Arco Máx."),
    ("Equipamentos", "Softwares", "Softwares"),
    ("Astronomos", "Centros", "Centros")
]

for label1, key2, label2 in itens:
    fields[label1 if ' ' not in label1 else label1.split()[0]] = criar_label_entry(label1, col1_x, y)
    fields[key2] = criar_label_entry(label2, col2_x, y)
    y += spacing_y

# =========================
# BOTÃO GUARDAR
# =========================
def criar_asteroide():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Asteroid (full_name) VALUES (?)", (fields['Nome'].get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Salvo!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

guardar_btn = ctk.CTkButton(app, text="Guardar Asteroide", command=criar_asteroide, 
                             fg_color="#27AE60", hover_color="#1E8449", width=250, height=45, font=("Arial", 16, "bold"))
guardar_btn.place(x=550, y=y + 20)

# =========================
# DOWN BAR
# =========================
down_bar = ctk.CTkFrame(app, height=60, fg_color="#B4AEAE", corner_radius=0)
down_bar.place(x=0, y=740, relwidth=1)

ctk.CTkLabel(down_bar, text="@Adriana Abreu & Leonor Rebola", text_color="black", 
              font=("Aharoni", 14, "bold"), fg_color="transparent").place(x=20, y=15)

def add_social_icon(img_name, x, cmd):
    img = Image.open(img_path(img_name)).resize((30, 30))
    ph = ctk.CTkImage(img, size=(30, 30))
    lbl = ctk.CTkLabel(down_bar, image=ph, text="", fg_color="transparent")
    lbl.place(x=x, y=15)
    lbl.bind("<Button-1>", lambda e: cmd())
    lbl.configure(cursor="hand2")

add_social_icon("nasa.png", 1350, open_nasa)
add_social_icon("insta.png", 1400, open_insta)
add_social_icon("twitter.png", 1450, open_twitter)
add_social_icon("facebook.png", 1500, open_facebook)
add_social_icon("linkedin.png", 1550, open_linkedin)

app.mainloop()