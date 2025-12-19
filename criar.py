import customtkinter as ctk
from tkinter import messagebox
from main import get_connection, img_path, open_insta, open_nasa, open_twitter, open_facebook, open_linkedin
from PIL import Image, ImageTk
import sys

# =========================
# CONFIGURAÇÕES E ESTADO
# =========================
if len(sys.argv) >= 3:
    nome_completo = sys.argv[1]
    usuario = sys.argv[2]
else:
    nome_completo = "Usuário"
    usuario = ""

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1600x800")
app.title("Asteroides – Criar")

# =========================
# BACKGROUND
# =========================
bg_image = Image.open(img_path("fundologs.jpg")).resize((2000, 1000))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = ctk.CTkCanvas(app, width=2000, height=1000, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# =========================
# TOP BAR
# =========================
top_bar = ctk.CTkFrame(app, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0, relwidth=1)

logo = ImageTk.PhotoImage(Image.open(img_path("logo.png")).resize((100, 100)))
ctk.CTkLabel(top_bar, image=logo, text="").place(x=30, y=8)

ctk.CTkLabel(
    top_bar,
    text="Criar",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF"
).place(x=125, y=15)

# =========================
# FUNÇÃO DE CRIAÇÃO (ALINHADA)
# =========================
# =========================
# FUNÇÃO DE CRIAÇÃO (ALINHAMENTO GARANTIDO)
# =========================
fields = {}

def criar_label_entry(texto, x_pos, y_pos, width_entry=180):
    # Criamos um frame invisível para agrupar label e entry
    container = ctk.CTkFrame(app, fg_color="transparent")
    container.place(x=x_pos, y=y_pos)

    # A Label agora é um widget normal, mas com fg_color="transparent"
    # O CustomTkinter lida melhor com a transparência dentro de frames
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
        width=width_entry, 
        height=28, 
        fg_color="#1E1E1E", 
        text_color="white", 
        border_color="#444444"
    )
    entry.pack(side="left")
    
    return entry

# =========================
# POSICIONAMENTO DOS CAMPOS
# =========================
spacing_y = 40  
y_inicial = 120 
col1_x = 150  # Posição X da primeira coluna (Label + Entry)
col2_x = 650  # Posição X da segunda coluna (Label + Entry)

y = y_inicial

# Coluna 1 e Coluna 2 alinhadas lado a lado
fields['Nome'] = criar_label_entry("Nome", col1_x, y)
fields['Diametro_Inc'] = criar_label_entry("Diâmetro Inc. (km)", col2_x, y)

y += spacing_y
fields['Diametro'] = criar_label_entry("Diâmetro (km)", col1_x, y)
fields['Magnitude'] = criar_label_entry("Magnitude (H)", col2_x, y)

y += spacing_y
fields['Albedo'] = criar_label_entry("Albedo", col1_x, y)
fields['PHA'] = criar_label_entry("PHA (Y/N)", col2_x, y)

y += spacing_y
fields['NEO'] = criar_label_entry("NEO (Y/N)", col1_x, y)
fields['Epoch'] = criar_label_entry("Epoch", col2_x, y)

y += spacing_y
fields['e'] = criar_label_entry("e", col1_x, y)
fields['a'] = criar_label_entry("a (AU)", col2_x, y)

y += spacing_y
fields['q'] = criar_label_entry("q (AU)", col1_x, y)
fields['i'] = criar_label_entry("i (°)", col2_x, y)

y += spacing_y
fields['M'] = criar_label_entry("M (°)", col1_x, y)
fields['tp'] = criar_label_entry("tp", col2_x, y)

y += spacing_y
fields['MOID'] = criar_label_entry("MOID (LD)", col1_x, y)
fields['RMS'] = criar_label_entry("RMS", col2_x, y)

y += spacing_y
fields['Descricao'] = criar_label_entry("Descrição", col1_x, y)
fields['Sessoes'] = criar_label_entry("Sessões", col2_x, y)

y += spacing_y
fields['Imagens'] = criar_label_entry("Imagens", col1_x, y)
fields['Arco_Max'] = criar_label_entry("Arco Máx.", col2_x, y)

y += spacing_y
fields['Equipamentos'] = criar_label_entry("Equipamentos", col1_x, y)
fields['Softwares'] = criar_label_entry("Softwares", col2_x, y)

y += spacing_y
fields['Astronomos'] = criar_label_entry("Astrónomos", col1_x, y)
fields['Centros'] = criar_label_entry("Centros", col2_x, y)

# =========================
# BOTÃO GUARDAR
# =========================
def criar_asteroide():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Asteroid (full_name, diameter, diameter_sigma, H, albedo, pha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            fields['Nome'].get(),
            fields['Diametro'].get() or None,
            fields['Diametro_Inc'].get() or None,
            fields['Magnitude'].get() or None,
            fields['Albedo'].get() or None,
            fields['PHA'].get() or None
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Asteroide criado com sucesso!")
        app.destroy()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

guardar_btn = ctk.CTkButton(app, text="Guardar Asteroide", command=criar_asteroide, 
                             fg_color="#27AE60", hover_color="#1E8449", width=250, height=45, font=("Arial", 16, "bold"))
guardar_btn.place(x=600, y=y + 60)

# =========================
# DOWN BAR
# =========================
down_bar = ctk.CTkFrame(app, width=2000, height=60, fg_color="#B4AEAE", corner_radius=0)
down_bar.place(x=0, y=740)

ctk.CTkLabel(down_bar, text="@Adriana Abreu & Leonor Rebola", text_color="black", 
              font=("Aharoni", 14, "bold"), fg_color="transparent").place(x=20, y=15)

def add_social_icon(img_name, x, cmd):
    img = Image.open(img_path(img_name)).resize((35, 35))
    ph = ImageTk.PhotoImage(img)
    lbl = ctk.CTkLabel(down_bar, image=ph, text="", fg_color="transparent")
    lbl.image = ph
    lbl.place(x=x, y=12)
    lbl.bind("<Button-1>", lambda e: cmd())
    lbl.configure(cursor="hand2")

add_social_icon("nasa.png", 1350, open_nasa)
add_social_icon("insta.png", 1400, open_insta)
add_social_icon("twitter.png", 1450, open_twitter)
add_social_icon("facebook.png", 1500, open_facebook)
add_social_icon("linkedin.png", 1550, open_linkedin)

app.mainloop()