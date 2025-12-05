import pandas as pd
import pyodbc
import os
import sys
import time

# --- 1. CONFIGURAÇÃO DA CONEXÃO E CAMINHOS ---

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=172.20.10.12\SQLEXPRESS,1433;'
    r'DATABASE=projeto;'
    r'UID=adriana;'
    r'PWD=12345;'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEO_CSV_PATH = os.path.join(BASE_DIR, 'neo.csv')
MPCORB_DAT_PATH = os.path.join(BASE_DIR, 'MPCORB.DAT.txt')


# 2. FUNÇÃO AUXILIAR PARA INSERIR LISTAS NA STAGING
def insert_staging(cursor, query, data_list, batch_size=50000):
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i+batch_size]
        cursor.executemany(query, batch)

# 3. ETL PRINCIPAL
def run_etl():
    start_total = time.time()

    # Conexão ao SQL Server
    try:
        cnxn = pyodbc.connect(conn_str, autocommit=False)
        cursor = cnxn.cursor()
        cursor.fast_executemany = True
        print("\n>>> Conectado ao SQL Server!")
    except Exception as e:
        print("Erro ao conectar:", e)
        sys.exit(1)

    # 3.1 PROCESSAR neo.csv  → staging
    if os.path.exists(NEO_CSV_PATH):
        print("\n--- A processar neo.csv ---")

        df = pd.read_csv(NEO_CSV_PATH, delimiter=';', encoding='utf-8', low_memory=False)
        df = df.dropna(subset=['full_name'])

        numeric_cols = ['diameter', 'h', 'albedo', 'e', 'a', 'q', 'i',
                        'ma', 'moid_ld', 'rms', 'epoch_mjd']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

        # INSERIR ASTEROIDES
        staging_asteroids = []
        for _, row in df.iterrows():
            staging_asteroids.append((
                row['full_name'],
                1 if row['neo'] == 'Y' else 0,
                1 if row['pha'] == 'Y' else 0,
                row['diameter'],
                row['h'],
                row['albedo']
            ))

        print(f"Inserindo {len(staging_asteroids)} asteroides na staging...")
        insert_staging(cursor,
            "INSERT INTO Staging_Asteroid VALUES (?, ?, ?, ?, ?, ?)",
            staging_asteroids
        )

        # INSERIR ÓRBITAS
        staging_orbits = []
        for _, row in df.iterrows():
            q = row['q'] if row['q'] != 0 else row['a'] * (1 - row['e'])
            staging_orbits.append((
                row['full_name'],
                row['epoch_mjd'],
                row['e'],
                row['a'],
                q,
                row['i'],
                row['ma'],
                row['moid_ld'],
                row['rms']
            ))

        print(f"Inserindo {len(staging_orbits)} órbitas na staging...")
        insert_staging(cursor,
            "INSERT INTO Staging_Orbit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            staging_orbits
        )

        cnxn.commit()
        print("neo.csv → staging concluído!")

    else:
        print("Ficheiro neo.csv não encontrado!")

    # 3.2 PROCESSAR MPCORB.DAT  → staging
    if os.path.exists(MPCORB_DAT_PATH):
        print("\n--- A processar MPCORB.DAT ---")

        lines = open(MPCORB_DAT_PATH, "r", encoding="latin1").read().splitlines()

        staging_software = []
        staging_obs = []

        print("A extrair linhas...")

        for line in lines:
            # Nome correto do asteroide (colunas 166–194)
            full_name = line[166:194].strip()
            # Observações
            arc = line[32:37].strip()    # arc length
            num_obs = line[13:17].strip()
            # Software (colunas 38–41 no MPCORB)
            computer = line[38:41].strip()

            # Converter e tratar
            arc = float(arc) if arc else 0.0
            num_obs = int(num_obs) if num_obs else 0
            full_name = full_name if full_name else None
            computer = computer if computer else "Unknown"

            staging_obs.append((
                full_name,
                arc,
                num_obs,
                computer
            ))

            staging_software.append((computer,))

        print(f"Inserindo {len(staging_software)} softwares na staging...")
        insert_staging(cursor,
            "INSERT INTO Staging_Software VALUES (?)",
            staging_software
        )

        print(f"Inserindo {len(staging_obs)} observações na staging...")
        insert_staging(cursor,
            "INSERT INTO Staging_Observation VALUES (?, ?, ?, ?)",
            staging_obs
        )

        cnxn.commit()
        print("MPCORB.DAT → staging concluído!")

    else:
        print("Ficheiro MPCORB.DAT não encontrado!")

    # ---------------------------------------------------------
    cursor.close()
    cnxn.close()

if __name__ == "__main__":
    run_etl()