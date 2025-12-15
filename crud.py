import customtkinter as ctk
from tkinter import ttk, messagebox
import pyodbc
from main import get_connection



# =========================
# CONFIGURAÇÕES DA JANELA
# =========================
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1400x750")
app.title("CRUD - dbo.dados")

pagina_atual = 0
total_paginas = 1

# =========================
# TÍTULO
# =========================
ctk.CTkLabel(
    app,
    text="Sistema CRUD - Asteroides (dbo.dados)",
    font=("Aharoni", 24, "bold")
).pack(pady=20)

# =========================
# FORMULÁRIO
# =========================
frame_form = ctk.CTkFrame(app)
frame_form.pack(pady=10)

labels = ["Name_Neo", "Name_MPCORB", "Diameter", "Albedo", "PHA", "NEO"]
entries = {}

for i, label in enumerate(labels):
    ctk.CTkLabel(frame_form, text=label + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = ctk.CTkEntry(frame_form, width=300)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[label.lower()] = entry

# =========================
# PESQUISA E PAGINAÇÃO
# =========================
frame_search = ctk.CTkFrame(app)
frame_search.pack(pady=10)

ctk.CTkLabel(frame_search, text="Pesquisar:").grid(row=0, column=0, padx=10)
entry_search = ctk.CTkEntry(frame_search, width=300)
entry_search.grid(row=0, column=1, padx=10)

ctk.CTkLabel(frame_search, text="Mostrar:").grid(row=0, column=2, padx=10)
combo_limit = ttk.Combobox(frame_search, values=[10, 50, 100, 500], width=10)
combo_limit.current(0)
combo_limit.grid(row=0, column=3, padx=10)

# =========================
# TREEVIEW
# =========================
columns = ("id", "name_neo", "name_mpcorb", "diameter", "albedo", "pha", "neo")
tree = ttk.Treeview(app, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col.upper())
    tree.column(col, width=150)

tree.pack(pady=20, fill="x")

# =========================
# PAGINAÇÃO
# =========================
frame_pag = ctk.CTkFrame(app)
frame_pag.pack(pady=5)

label_pagina = ctk.CTkLabel(frame_pag, text="Página 1/1")
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
# ATUALIZAR LISTA (SQL)
# =========================
def atualizar_lista():
    global total_paginas, pagina_atual

    termo = entry_search.get()
    limit = int(combo_limit.get())
    offset = pagina_atual * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM dbo.dados
        WHERE Name_Neo LIKE ? OR Name_MPCORB LIKE ?
    """, (f"%{termo}%", f"%{termo}%"))

    total_registros = cursor.fetchone()[0]
    total_paginas = max(1, (total_registros + limit - 1) // limit)

    cursor.execute("""
        SELECT id, Name_Neo, Name_MPCORB, diameter, albedo, pha, neo
        FROM dbo.dados
        WHERE Name_Neo LIKE ? OR Name_MPCORB LIKE ?
        ORDER BY id
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """, (f"%{termo}%", f"%{termo}%", offset, limit))

    rows = cursor.fetchall()
    conn.close()

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert("", "end", iid=row.id, values=row)

    label_pagina.configure(text=f"Página {pagina_atual + 1}/{total_paginas}")

# =========================
# CRUD
# =========================
def criar():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO dbo.dados (Name_Neo, Name_MPCORB, diameter, albedo, pha, neo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        entries["name_neo"].get(),
        entries["name_mpcorb"].get(),
        entries["diameter"].get(),
        entries["albedo"].get(),
        entries["pha"].get(),
        entries["neo"].get()
    ))

    conn.commit()
    conn.close()
    atualizar_lista()

def atualizar():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um registro")
        return

    record_id = selected[0]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE dbo.dados
        SET Name_Neo=?, Name_MPCORB=?, diameter=?, albedo=?, pha=?, neo=?
        WHERE id=?
    """, (
        entries["name_neo"].get(),
        entries["name_mpcorb"].get(),
        entries["diameter"].get(),
        entries["albedo"].get(),
        entries["pha"].get(),
        entries["neo"].get(),
        record_id
    ))

    conn.commit()
    conn.close()
    atualizar_lista()

def deletar():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um registro")
        return

    record_id = selected[0]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.dados WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    atualizar_lista()

# =========================
# BOTÕES CRUD
# =========================
frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10)

ctk.CTkButton(frame_buttons, text="Criar", command=criar).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_buttons, text="Atualizar", command=atualizar).grid(row=0, column=1, padx=10)
ctk.CTkButton(frame_buttons, text="Deletar", command=deletar).grid(row=0, column=2, padx=10)

# =========================
# EVENTOS
# =========================
entry_search.bind("<KeyRelease>", lambda e: atualizar_lista())
combo_limit.bind("<<ComboboxSelected>>", lambda e: atualizar_lista())

# =========================
# START
# =========================
atualizar_lista()
app.mainloop()

