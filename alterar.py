import sys
import tkinter as tk
from tkinter import messagebox
from main import get_connection

# ===========================
# CHECAGEM DE ARGUMENTO
# ===========================
if len(sys.argv) < 2:
    messagebox.showerror("Erro", "ID do asteroide não fornecido.")
    sys.exit()

asteroid_id = sys.argv[1]

# ===========================
# BUSCAR DADOS DO ASTEROIDE
# ===========================
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM vw_App_Completa WHERE Asteroid_ID = ?", (asteroid_id,))
row = cursor.fetchone()
conn.close()

if not row:
    messagebox.showerror("Erro", "Asteroide não encontrado.")
    sys.exit()

# ===========================
# CRIAR JANELA
# ===========================
root = tk.Tk()
root.title(f"Alterar Asteroide - ID {asteroid_id}")

# ===========================
# DEFINIR CAMPOS PARA ALTERAÇÃO
# ===========================
# Mapear cada coluna do row para um Entry
campos = [
    ("Nome", row[1]),
    ("Diametro", row[2]),
    ("Incerteza_Diametro", row[3]),
    ("Magnitude", row[4]),
    ("Albedo", row[5]),
    ("PHA", row[6]),
    ("NEO", row[7]),
    ("epoch_cal", row[8]),
    ("Distancia_Minima_Terra", row[9]),
    ("RMS", row[10]),
    ("Excentricidade", row[11]),
    ("Eixo_Semimaior", row[12]),
    ("Perielio", row[13]),
    ("Inclinacao", row[14]),
    ("Anomalia_Media", row[15]),
    ("tp_cal", row[16]),
    ("Epoch", row[17]),
    ("Status_Alerta", row[18]),
    ("Prioridade_Alerta", row[19]),
    ("Escala_Torino", row[20]),
    ("Data_Aproximacao", row[21]),
    ("Descricao_Risco", row[22]),
    ("Total_Sessoes", row[23]),
    ("Total_Imagens", row[24]),
    ("Maior_Arco_Dias", row[25]),
    ("Lista_Equipamentos", row[26]),
    ("Lista_Softwares", row[27]),
    ("Equipa_Astronomos", row[28]),
    ("Centros_Observacao", row[29])
]

entries = {}

# Criar labels e entries
for i, (nome, valor) in enumerate(campos):
    tk.Label(root, text=nome+":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entry.insert(0, "" if valor is None else str(valor))
    entries[nome] = entry

# ===========================
# FUNÇÃO PARA SALVAR ALTERAÇÕES
# ===========================
def salvar_alteracoes():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Preparar SQL dinamicamente
        update_cols = ", ".join([f"{col} = ?" for col in entries.keys()])
        update_vals = [entries[col].get() for col in entries.keys()]
        update_vals.append(asteroid_id)

        sql = f"UPDATE Asteroides SET {update_cols} WHERE Asteroid_ID = ?"

        cursor.execute(sql, update_vals)
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Asteroide alterado com sucesso.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao alterar asteroide: {e}")

# ===========================
# BOTÃO SALVAR
# ===========================
tk.Button(root, text="Salvar Alterações", command=salvar_alteracoes, bg="#27AE60", fg="white").grid(row=len(campos)+1, column=0, columnspan=2, pady=10)

root.mainloop()
