import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

# Dados de exemplo
usuarios = []

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Janela principal
app = ctk.CTk()
app.geometry("1200x700")
app.title("Sistema CRUD")

# --- Variáveis de paginação ---
pagina_atual = 0  # começa na primeira página
total_paginas = 0

# --- Título ---
title_label = ctk.CTkLabel(app, text="Sistema CRUD de Usuários", font=("Aharoni", 24, "bold"))
title_label.pack(pady=20)

# --- Formulário ---
frame_form = ctk.CTkFrame(app)
frame_form.pack(pady=10)

ctk.CTkLabel(frame_form, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = ctk.CTkEntry(frame_form)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(frame_form, text="Email:").grid(row=1, column=0, padx=10, pady=10)
entry_email = ctk.CTkEntry(frame_form)
entry_email.grid(row=1, column=1, padx=10, pady=10)

# --- Barra de pesquisa ---
frame_search = ctk.CTkFrame(app)
frame_search.pack(pady=10)

ctk.CTkLabel(frame_search, text="Pesquisar:").grid(row=0, column=0, padx=10)
entry_search = ctk.CTkEntry(frame_search)
entry_search.grid(row=0, column=1, padx=10)

# --- Dropdown para número de linhas ---
ctk.CTkLabel(frame_search, text="Mostrar:").grid(row=0, column=2, padx=10)
combo_limit = ttk.Combobox(frame_search, values=[10, 100, 1000, 10000], width=10)
combo_limit.current(0)  # padrão 10 linhas
combo_limit.grid(row=0, column=3, padx=10)

# --- Botões de paginação ---
frame_pag = ctk.CTkFrame(app)
frame_pag.pack(pady=5)

btn_prev = ctk.CTkButton(frame_pag, text="Anterior")
btn_prev.grid(row=0, column=0, padx=10)
btn_next = ctk.CTkButton(frame_pag, text="Próxima")
btn_next.grid(row=0, column=1, padx=10)

label_pagina = ctk.CTkLabel(frame_pag, text="Página 1/1")
label_pagina.grid(row=0, column=2, padx=10)

# --- Lista (Treeview) ---
columns = ("nome", "email")
tree = ttk.Treeview(app, columns=columns, show="headings", height=10)
tree.heading("nome", text="Nome")
tree.heading("email", text="Email")
tree.pack(pady=20)

# --- Função para resetar página ---
def reset_pagina():
    global pagina_atual
    pagina_atual = 0

# --- Função de atualização da lista com pesquisa e paginação ---
def atualizar_lista():
    global total_paginas, pagina_atual
    termo = entry_search.get().lower()
    limit = int(combo_limit.get())
    
    # Filtra usuários pelo termo
    filtrados = [u for u in usuarios if termo in u["nome"].lower() or termo in u["email"].lower()]
    
    # Calcula total de páginas
    total_paginas = max(1, (len(filtrados) + limit - 1) // limit)
    
    # Corrige a página atual se estiver fora do intervalo
    if pagina_atual >= total_paginas:
        pagina_atual = total_paginas - 1
    if pagina_atual < 0:
        pagina_atual = 0
    
    # Determina o intervalo de índices
    start = pagina_atual * limit
    end = start + limit
    
    # Atualiza Treeview
    for item in tree.get_children():
        tree.delete(item)
    for idx, user in enumerate(filtrados[start:end], start=start):
        tree.insert("", "end", iid=idx, values=(user["nome"], user["email"]))
    
    # Atualiza label de página
    label_pagina.configure(text=f"Página {pagina_atual + 1}/{total_paginas}")

# --- Funções de navegação ---
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

btn_next.configure(command=proxima_pagina)
btn_prev.configure(command=pagina_anterior)

# --- Eventos ---
entry_search.bind("<KeyRelease>", lambda e: [reset_pagina(), atualizar_lista()])
combo_limit.bind("<<ComboboxSelected>>", lambda e: [reset_pagina(), atualizar_lista()])

# --- Funções CRUD ---
def criar():
    nome = entry_nome.get()
    email = entry_email.get()
    if nome and email:
        usuarios.append({"nome": nome, "email": email})
        entry_nome.delete(0, "end")
        entry_email.delete(0, "end")
        reset_pagina()
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

def deletar():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        usuarios.pop(idx)
        reset_pagina()
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Selecione um usuário para deletar")

def atualizar():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        usuarios[idx]["nome"] = entry_nome.get()
        usuarios[idx]["email"] = entry_email.get()
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Selecione um usuário para atualizar")

# --- Botões CRUD ---
frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10)

ctk.CTkButton(frame_buttons, text="Criar", command=criar).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_buttons, text="Atualizar", command=atualizar).grid(row=0, column=1, padx=10)
ctk.CTkButton(frame_buttons, text="Deletar", command=deletar).grid(row=0, column=2, padx=10)

# Inicializa a lista
atualizar_lista()

app.mainloop()
