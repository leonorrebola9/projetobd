import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import sys
import webbrowser
import hashlib # Necessário para hashing de senha
from main import conectar_sql # Assume-se que esta função retorna (conn, cursor)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- CAMINHO BASE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- JANELA PRINCIPAL ---
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Somos bue fixes")

## 🎨 Top Bar e UI Setup


# --- TOP BAR ---
top_bar = ctk.CTkFrame(app, width=1920, height=80, fg_color="#0C1B33")
top_bar.place(x=0, y=0)

# --- LOGO ---
img_path = os.path.join(BASE_DIR, r"Imagens_app\logo.png")
try:
    image = Image.open(img_path).resize((100, 100))
    photo = ImageTk.PhotoImage(image)
    logo_label = ctk.CTkLabel(top_bar, image=photo, text="")
    logo_label.place(x=30, y=8)
    logo_label.image = photo 
except FileNotFoundError:
    print(f"Aviso: Imagem de logo não encontrada em {img_path}")
    logo_label = ctk.CTkLabel(top_bar, text="LOGO", text_color="#E2DFDF")
    logo_label.place(x=30, y=15)


# --- TÍTULO ---
login_title = ctk.CTkLabel(
    top_bar,
    text="Sign In",
    font=("Aharoni", 50, "bold"),
    text_color="#E2DFDF"
)
login_title.place(x=150, y=15)

# --- CAMPOS DE ENTRADA ---
name = ctk.CTkEntry(app, placeholder_text="Nome", width=400, height=35)
name.place(x=400, y=120)

surname = ctk.CTkEntry(app, placeholder_text="Sobrenome", width=250, height=35)
surname.place(x=800, y=120)

usuario_entry = ctk.CTkEntry(app, placeholder_text="Usuário", width=400, height=35)
usuario_entry.place(x=400, y=200)

passw_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=250, height=35)
passw_entry.place(x=800, y=200)

# --- OUTPUT LABEL ---
output_label = ctk.CTkLabel(app, text="", text_color="Red")
output_label.place(x=650, y=235)

## 💾 Funções de Conexão e Registo (SQL)


# --- FUNÇÃO BOTÃO “ENTRAR” (REGISTO SQL) ---
def greet():
    nome = name.get()      # Corresponde à coluna 'name'
    sobrenome = surname.get() # Corresponde à coluna 'surname'
    usuario = usuario_entry.get() # Corresponde à coluna 'user'
    senha = passw_entry.get()    # Corresponde à coluna 'passw' (hash)

    if not nome or not sobrenome or not usuario or not senha:
        output_label.configure(text="Preencha todos os campos!", text_color="red")
        return

    try:
        # 1. Aplicar Hashing SHA-256 à senha para segurança
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

        # 2. Obter a conexão e o cursor
        conn, cursor = conectar_sql()

        # 3. Preparar a query SQL
        # Inserir na tabela 'users' com as colunas corretas
        sql_insert = """
            INSERT INTO users (name, surname, user, passw)
            VALUES (?, ?, ?, ?)
        """

        # 4. Executar a query (usando o hash da senha)
        cursor.execute(sql_insert, (nome, sobrenome, usuario, senha_hash))

        # 5. Confirmar a transação
        conn.commit()

        # Mostrar sucesso e limpar os campos
        output_label.configure(text="Conta criada com sucesso! Redirecionando...", text_color="green")
        name.delete(0, 'end')
        surname.delete(0, 'end')
        usuario_entry.delete(0, 'end')
        passw_entry.delete(0, 'end')

        # Abrir a tela de Login após 1.5 segundos
        app.after(1500, open_signin)


    except Exception as e:
        # Erro de base de dados (ex: usuário já existe, falha de conexão)
        print(f"Erro ao inserir dados no SQL: {e}")
        # Mensagens mais amigáveis para erros comuns:
        if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e).lower():
             output_label.configure(text="Erro: O usuário escolhido já existe.", text_color="red")
        else:
            output_label.configure(text=f"Erro ao criar conta: {e}", text_color="red")
        
    finally:
        # Garantir que a conexão é fechada
        if 'conn' in locals() and conn:
            conn.close()

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

## 🔁 Navegação e Redes Sociais


# --- FUNÇÃO PARA ABRIR login.py ---
def open_signin():
    login_path = os.path.join(BASE_DIR, "login.py")
    if not os.path.isfile(login_path):
        output_label.configure(text="Erro: login.py não encontrado.", text_color="red")
        return
    try:
        app.destroy()
        # Abre o login.py num novo processo Python
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


## ⬇️ Down Bar e Rodapé


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
# Funções auxiliares para carregar imagens e ligar eventos
def setup_social_icon(parent, x, y, image_name, command_func, size):
    path = os.path.join(BASE_DIR, "Imagens_app", image_name)
    try:
        img = Image.open(path).resize(size)
        photo_img = ImageTk.PhotoImage(img)
        label = ctk.CTkLabel(parent, image=photo_img, text="")
        label.place(x=x, y=y)
        label.image = photo_img # Manter a referência
        label.bind("<Button-1>", lambda e: command_func())
        label.configure(cursor="hand2")
        return label
    except FileNotFoundError:
        # Coloca um texto simples se a imagem falhar
        label = ctk.CTkLabel(parent, text=image_name.split('.')[0], text_color="black")
        label.place(x=x, y=y)
        print(f"Aviso: Imagem {image_name} não encontrada.")
        return label


# Nasa
nasa_label = setup_social_icon(down_bar, 1390, 15, "nasa.png", open_nasa, (30, 30))

# Instagram
insta_label = setup_social_icon(down_bar, 1425, 15, "insta.png", open_insta, (35, 35))

# Twitter
twitter_label = setup_social_icon(down_bar, 1460, 15, "twitter.png", open_twitter, (35, 30))

# Facebook
facebook_label = setup_social_icon(down_bar, 1495, 15, "facebook.png", open_facebook, (35, 35))

# LinkedIn
linkedin_label = setup_social_icon(down_bar, 1530, 14, "linkedin.png", open_linkedin, (38, 38))


app.mainloop()



