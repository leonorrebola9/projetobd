import pandas as pd
import pyodbc
import os
import sys

# --- 1. CONFIGURAÇÃO DA CONEXÃO E CAMINHOS ---

# 🔧 Connection string correta para aceder ao SQL Server noutro PC
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=172.20.10.12\SQLEXPRESS,1433;'   # <-- IP + Instância + Porta
    r'DATABASE=projeto;'                      # <-- nome da tua BD
    r'UID=adriana;'                        # <-- user SQL
    r'PWD=12345;'                    # <-- password
)

# Diretório base do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEO_CSV_PATH = os.path.join(BASE_DIR, 'neo.csv')
MPCORB_DAT_PATH = os.path.join(BASE_DIR, 'MPCORB.DAT.txt')


# --- 2. FUNÇÕES DE INSERÇÃO (CHAMADA AOS STORED PROCEDURES) ---

def inserir_asteroide_sp(cursor, data):
    sp_call = "{CALL SP_InserirAsteroide (?, ?, ?, ?, ?, ?, ?)}"
    try:
        cursor.execute(
            sp_call,
            data['spkid'], data['full_name'], data['neo'], data['pha'],
            data['diameter'], data['h'], data['albedo']
        )
        result = cursor.fetchone()
        return result and result[0] == 1
    except pyodbc.IntegrityError:
        return False
    except Exception:
        return False


def inserir_parametro_orbital_sp(cursor, data):
    sp_call = "{CALL SP_InserirOrbitalParameter (?, ?, ?, ?, ?, ?, ?, ?, ?)}"
    try:
        cursor.execute(
            sp_call,
            data['spkid'], data['orbit_id'], data['epoch_mjd'],
            data['e'], data['a'], data['i'],
            data['ma'], data['moid_ld'], data['rms']
        )
        return True
    except pyodbc.IntegrityError:
        return False
    except Exception:
        return False


# --- 3. FUNÇÃO PRINCIPAL DE ETL ---
def run_etl():
    # --- 3.1 Conexão ---
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        print("✅ Conexão ao SQL Server estabelecida com sucesso.")
    except pyodbc.Error as ex:
        print(f"❌ Erro ao conectar ao SQL Server: {ex}")
        sys.exit(1)

    numeric_cols = [
        'h', 'diameter', 'albedo', 'e', 'a', 'q', 'i', 'om', 'w', 'ma',
        'moid_ld', 'rms', 'diameter_sigma', 'sigma_e', 'sigma_a',
        'sigma_i', 'sigma_w', 'sigma_ma'
    ]

    # --- 3.2 PROCESSAMENTO NEO.CSV ---
    if not os.path.exists(NEO_CSV_PATH):
        print(f"ERRO: Ficheiro neo.csv não encontrado em: {NEO_CSV_PATH}")
    else:
        print("\n--- Processamento de neo.csv ---")
        try:
            df_neo = pd.read_csv(NEO_CSV_PATH, delimiter=';', encoding='utf-8', low_memory=False)

            df_neo = df_neo.dropna(subset=['spkid'])
            df_neo['spkid'] = pd.to_numeric(df_neo['spkid'], errors='coerce').astype('Int64')

            df_neo['neo'] = df_neo['neo'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)
            df_neo['pha'] = df_neo['pha'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)

            for col in numeric_cols:
                if col in df_neo.columns:
                    df_neo[col] = pd.to_numeric(df_neo[col], errors='coerce').fillna(0)

            # ASTEROIDES ÚNICOS
            asteroide_cols = ['spkid', 'full_name', 'name', 'pha', 'neo', 'h', 'diameter', 'albedo']
            df_asteroides_unicos = df_neo[asteroide_cols].drop_duplicates(subset=['spkid'])

            print(f"Inserindo {len(df_asteroides_unicos)} asteroides únicos...")
            count_inserted = 0

            for _, row in df_asteroides_unicos.iterrows():
                if inserir_asteroide_sp(cursor, row):
                    count_inserted += 1

            cnxn.commit()
            print(f"Concluído: {count_inserted} novos asteroides inseridos/atualizados.")

            # PARÂMETROS ORBITAIS
            orbital_cols = ['spkid', 'orbit_id', 'epoch_mjd', 'e', 'a', 'i', 'ma', 'moid_ld', 'rms']
            df_orbitas = df_neo[orbital_cols].dropna(subset=['orbit_id'])

            print(f"Iniciando a inserção de {len(df_orbitas)} parâmetros orbitais (neo.csv)...")
            count_orbits_inserted = 0

            for _, row in df_orbitas.iterrows():
                if inserir_parametro_orbital_sp(cursor, row):
                    count_orbits_inserted += 1

            cnxn.commit()
            print(f"Concluído: {count_orbits_inserted} parâmetros orbitais inseridos.")

        except Exception as e:
            cnxn.rollback()
            print(f"ERRO FATAL no processamento neo.csv: {e}")

    # --- 3.3 PROCESSAMENTO MPCORB.DAT ---
    if not os.path.exists(MPCORB_DAT_PATH):
        print(f"\nERRO: Ficheiro MPCORB.DAT não encontrado em: {MPCORB_DAT_PATH}")
    else:
        print("\n--- Processamento de MPCORB.DAT ---")
        try:
            colspecs = [
                (0, 6), (6, 12), (12, 13), (14, 25), (26, 36),
                (37, 47), (48, 58), (59, 69), (70, 80), (80, 92),
                (92, 105), (105, 116), (116, 121), (121, 124),
                (124, 133), (133, 138), (138, 142), (142, 150),
                (150, 172)
            ]

            names = [
                'Desn', 'h', 'G', 'Epoch', 'M', 'w', 'om', 'i', 'e', 'n', 'a',
                'Reference', 'ObsCount', 'OppCount', 'Arc', 'rms', 'Perts',
                'Computer', 'full_name'
            ]

            df_mpcorb = pd.read_fwf(
                MPCORB_DAT_PATH,
                colspecs=colspecs,
                header=None,
                names=names,
                encoding='latin1'
            )

            print(f"Ficheiro MPCORB.DAT lido com sucesso: {len(df_mpcorb)} linhas.")

            mpcorb_numeric = ['h', 'M', 'w', 'om', 'i', 'e', 'n', 'a', 'rms']
            for col in mpcorb_numeric:
                df_mpcorb[col] = pd.to_numeric(df_mpcorb[col].astype(str).str.strip(), errors='coerce').fillna(0)

            df_mpcorb['spkid'] = pd.to_numeric(df_mpcorb['Desn'], errors='coerce').astype('Int64')
            df_mpcorb = df_mpcorb.dropna(subset=['spkid'])

            df_mpcorb['orbit_id'] = df_mpcorb['Desn'] + '_' + df_mpcorb['Epoch'].astype(str)

            print(f"Iniciando a inserção de {len(df_mpcorb)} órbitas do MPCORB...")
            count_mpcorb_orbits_inserted = 0

            for _, row in df_mpcorb.iterrows():
                temp_asteroide = {
                    'spkid': row['spkid'],
                    'full_name': row['full_name'],
                    'neo': 0,
                    'pha': 0,
                    'diameter': 0.0,
                    'h': row['h'],
                    'albedo': 0.0
                }
                inserir_asteroide_sp(cursor, temp_asteroide)

                data_for_sp = {
                    'spkid': row['spkid'],
                    'orbit_id': row['orbit_id'],
                    'epoch_mjd': row['Epoch'],
                    'e': row['e'],
                    'a': row['a'],
                    'i': row['i'],
                    'ma': row['M'],
                    'moid_ld': 0.0,
                    'rms': row['rms']
                }

                if inserir_parametro_orbital_sp(cursor, data_for_sp):
                    count_mpcorb_orbits_inserted += 1

            cnxn.commit()
            print(f"Concluído: {count_mpcorb_orbits_inserted} órbitas do MPCORB inseridas.")

        except Exception as e:
            cnxn.rollback()
            print(f"ERRO FATAL no processamento MPCORB.DAT: {e}")

    cursor.close()
    cnxn.close()
    print("\nConexão fechada. ETL concluído com sucesso.")


if __name__ == "__main__":
    run_etl()
