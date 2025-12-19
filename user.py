import customtkinter as ctk
from main import get_connection
import sys
import pyodbc
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# =========================
# Receber nome de usuário do login
# =========================
if len(sys.argv) > 1:
    nome_usuario = sys.argv[1]  # Ex: "usuario1"
else:
    messagebox.showerror("Erro", "Usuário não informado")
    sys.exit()

# =========================
# Janela
# =========================
app = ctk.CTk()
app.geometry("600x400")
app.title("Editar Usuário")

# =========================
# Função para carregar dados do usuário
# =========================
def carregar_dados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, surname, [user], passw FROM users WHERE [user]=?",
            (nome_usuario,)
        )
        dados = cursor.fetchone()
        cursor.close()
        conn.close()

        if dados:
            entry_name.delete(0, ctk.END)
            entry_name.insert(0, dados[0])

            entry_surname.delete(0, ctk.END)
            entry_surname.insert(0, dados[1])

            entry_user.delete(0, ctk.END)
            entry_user.insert(0, dados[2])

            entry_pass.delete(0, ctk.END)
            entry_pass.insert(0, dados[3])
        else:
            messagebox.showerror("Erro", "Usuário não encontrado")
            app.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar dados: {e}")
        app.destroy()

# =========================
# Função para verificar duplicidade de usuário
# =========================
def usuario_existe(usuario_novo):
    """
    Retorna True se já existir outro usuário com o mesmo nome.
    """
    if usuario_novo == nome_usuario:
        return False  # O usuário não mudou, então não há duplicidade

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE [user] = ?",
        (usuario_novo,)
    )
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


# =========================
# Função atualizar dados
# =========================
def atualizar_dados():
    novo_name = entry_name.get()
    novo_surname = entry_surname.get()
    novo_user = entry_user.get()
    nova_senha = entry_pass.get()

    if not novo_name or not novo_surname or not novo_user or not nova_senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    if usuario_existe(novo_user):
        messagebox.showerror("Erro", "Já existe outro usuário com esse nome!")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET name=?, surname=?, [user]=?, passw=?
            WHERE [user]=?
            """,
            (novo_name, novo_surname, novo_user, nova_senha, nome_usuario)
        )
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        app.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao atualizar dados: {e}")

# =========================
# Campos de entrada
# =========================
ctk.CTkLabel(app, text="Nome:").place(x=50, y=50)
entry_name = ctk.CTkEntry(app, width=300)
entry_name.place(x=150, y=50)

ctk.CTkLabel(app, text="Sobrenome:").place(x=50, y=100)
entry_surname = ctk.CTkEntry(app, width=300)
entry_surname.place(x=150, y=100)

ctk.CTkLabel(app, text="Usuário:").place(x=50, y=150)
entry_user = ctk.CTkEntry(app, width=300)
entry_user.place(x=150, y=150)

ctk.CTkLabel(app, text="Senha:").place(x=50, y=200)
entry_pass = ctk.CTkEntry(app, width=300, show="*")
entry_pass.place(x=150, y=200)

# =========================
# Botão atualizar
# =========================
btn_atualizar = ctk.CTkButton(app, text="Salvar Alterações", command=atualizar_dados)
btn_atualizar.place(x=200, y=300)

# Carregar dados ao iniciar
carregar_dados()

app.mainloop()
