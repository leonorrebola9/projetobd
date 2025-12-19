import sys
import tkinter as tk
from tkinter import messagebox
from main import get_connection

# ===========================
# INICIALIZAR TKINTER
# ===========================
root = tk.Tk()
root.withdraw()

# ===========================
# CHECAGEM DE ARGUMENTO
# ===========================
if len(sys.argv) < 2:
    messagebox.showerror("Erro", "ID do asteroide não fornecido.")
    sys.exit()

asteroid_id = sys.argv[1]

# ===========================
# BUSCAR DADOS DO ASTEROIDE VIA VIEW
# ===========================
conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dbo.vw_App_Completa WHERE Asteroid_ID = ?",
        (asteroid_id,)
    )
    row = cursor.fetchone()

    if not row:
        messagebox.showerror("Erro", "Asteroide não encontrado.")
        sys.exit()

    column_names = [col[0] for col in cursor.description]

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# ===========================
# NORMALIZAR COLUNAS DA VIEW
# ===========================
dados_asteroide = dict(zip(column_names, row))
dados_asteroide_norm = {k.lower(): v for k, v in dados_asteroide.items()}

# ===========================
# CRIAR JANELA
# ===========================
root.deiconify()
root.title(f"Alterar Asteroide - ID {asteroid_id}")

entries = {}
row_index = 0

# ===========================
# CAMPOS DINÂMICOS
# ===========================
for col_name in column_names:
    col_key = col_name.lower()
    tk.Label(root, text=f"{col_name}:").grid(row=row_index, column=0, sticky="e", padx=5, pady=2)
    entry = tk.Entry(root, width=40)
    entry.grid(row=row_index, column=1, padx=5, pady=2)
    valor = dados_asteroide_norm.get(col_key, "")
    entry.insert(0, "" if valor is None else str(valor))
    entries[col_key] = entry
    row_index += 1

# ===========================
# FUNÇÃO SALVAR ALTERAÇÕES
# ===========================
def salvar_alteracoes():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # -------------------------
        # Função de conversão segura
        # -------------------------
        def conv_num(val):
            if val is None or val.strip() == "":
                return None
            try:
                return float(val) if "." in val else int(val)
            except:
                return val

        # =========================
        # TABELA ASTEROID
        # =========================
        asteroid_fields = {
            "full_name": "nome",
            "diameter": "diametro",
            "diameter_sigma": "incerteza",
            "H": "h",
            "albedo": "albedo",
            "pha": "pha",
            "neo": "neo"
        }

        fields_sql = []
        values = []
        for sql_field, form_key in asteroid_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                val = entries[form_key].get()
                if sql_field in ["diameter","diameter_sigma","H","albedo"]:
                    val = conv_num(val)
                values.append(val)
        values.append(asteroid_id)
        if fields_sql:
            cursor.execute(f"UPDATE dbo.Asteroid SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA ORBITAL_PARAMETER
        # =========================
        orbital_fields = {
            "moid_ld": "distancia_minima_terra",
            "rms": "rms",
            "e": "excentricidade",
            "a": "eixo_semimaior",
            "q": "perielio",
            "i": "inclinacao",
            "M": "anomalia_media",
            "tp_cal": "tp_cal",
            "epoch": "epoch"
        }

        fields_sql = []
        values = []
        for sql_field, form_key in orbital_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                val = entries[form_key].get()
                if sql_field in ["moid_ld","rms","e","a","q","i","M"]:
                    val = conv_num(val)
                values.append(val)
        values.append(asteroid_id)
        if fields_sql:
            cursor.execute(f"UPDATE dbo.Orbital_Parameter SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA ALERT
        # =========================
        alert_fields = {
            "status": "status",
            "Priority": "prioridade",
            "torino": "torino",
            "dap": "data_aproximacao",
            "Description": "descricao_risco"
        }

        if all(f in entries for f in alert_fields.values()):
            fields_sql = []
            values = []
            for sql_field, form_key in alert_fields.items():
                fields_sql.append(f"{sql_field} = ?")
                values.append(entries[form_key].get())
            values.append(asteroid_id)
            cursor.execute(f"UPDATE dbo.Alert SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA OBSERVATION
        # =========================
        observation_fields = {
            "total_sessoes": "total_sessoes",
            "total_imagens": "total_imagens",
            "maior_arco_dias": "maior_arco_dias"
        }
        fields_sql = []
        values = []
        for sql_field, form_key in observation_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                values.append(conv_num(entries[form_key].get()))
        if fields_sql:
            values.append(asteroid_id)
            cursor.execute(f"UPDATE dbo.Observation SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA EQUIPMENT
        # =========================
        equipment_fields = {"lista_equipamentos": "lista_equipamentos"}
        fields_sql = []
        values = []
        for sql_field, form_key in equipment_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                values.append(entries[form_key].get())
        if fields_sql:
            values.append(asteroid_id)
            cursor.execute(f"UPDATE dbo.Equipment SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA SOFTWARE
        # =========================
        software_fields = {"lista_softwares": "lista_softwares"}
        fields_sql = []
        values = []
        for sql_field, form_key in software_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                values.append(entries[form_key].get())
        if fields_sql:
            values.append(asteroid_id)
            cursor.execute(f"UPDATE dbo.Software SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA ASTRONOMER
        # =========================
        astronomer_fields = {"equipa_astronomos": "equipa_astronomos"}
        fields_sql = []
        values = []
        for sql_field, form_key in astronomer_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                values.append(entries[form_key].get())
        if fields_sql:
            values.append(asteroid_id)
            cursor.execute(f"UPDATE dbo.Astronomer SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # TABELA OBSERVATION_CENTER
        # =========================
        center_fields = {"centros": "centros_observacao"}
        fields_sql = []
        values = []
        for sql_field, form_key in center_fields.items():
            if form_key in entries:
                fields_sql.append(f"{sql_field} = ?")
                values.append(entries[form_key].get())
        if fields_sql:
            values.append(asteroid_id)
            cursor.execute(f"UPDATE dbo.Observation_Center SET {', '.join(fields_sql)} WHERE Asteroid_ID = ?", values)

        # =========================
        # COMMIT FINAL
        # =========================
        conn.commit()
        messagebox.showinfo("Sucesso", "Asteroide alterado com sucesso.")
        root.destroy()

    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao alterar asteroide: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ===========================
# BOTÃO SALVAR
# ===========================
btn_salvar = tk.Button(
    root,
    text="Salvar Alterações",
    command=salvar_alteracoes,
    bg="#27AE60",
    fg="white"
)
btn_salvar.grid(row=row_index + 1, column=0, columnspan=2, pady=10)

root.mainloop()
