import pandas as pd
import pyodbc
import os
import sys

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


# --- 2. FUNÇÕES DE INSERÇÃO (CHAMADA AOS STORED PROCEDURES) ---

def inserir_asteroide_sp(cursor, data):
    """
    Chama o SP para inserir o asteroide e retorna o Asteroid_ID (novo ou existente).
    """
    # 6 Parâmetros
    sp_call = "{CALL SP_InserirAsteroide (?, ?, ?, ?, ?, ?)}"
    try:
        cursor.execute(
            sp_call,
            data['full_name'], data['neo'], data['pha'],
            data['diameter'], data['h'], data['albedo']
        )
        # O SP retorna o Asteroid_ID (novo ou existente)
        result = cursor.fetchone() 
        
        if result:
            return result[0] # Retorna o valor numérico (Asteroid_ID)
        else:
            return None
            
    except Exception:
        return None


def inserir_parametro_orbital_sp(cursor, asteroid_id, data):
    """
    Chama o SP para inserir os parâmetros orbitais.
    Captura pyodbc.IntegrityError (duplicação de órbita) e ignora.
    """
    # 9 Parâmetros (Asteroid_ID + orbit_id + 7 campos de órbita)
    sp_call = "{CALL SP_InserirOrbitalParameter (?, ?, ?, ?, ?, ?, ?, ?, ?)}" 
    try:
        cursor.execute(
            sp_call,
            asteroid_id,            # 1. @Asteroid_ID (FK)
            data['orbit_id'],       # 2. @orbital_id (Não é inserido no SQL)
            data['epoch'],          # 3. @epoch
            data['e'],              # 4. @e
            data['a'],              # 5. @a
            data['i'],              # 6. @i
            data['M'],              # 7. @M
            data['moid_ld'],        # 8. @moid_ld
            data['rms']             # 9. @rms
        )
        return True
    except pyodbc.IntegrityError:
        # Duplicação de órbita (Asteroid_ID + epoch já existem).
        return False 
    except Exception as e:
        # Erros de conversão de dados, etc.
        print(f"ERRO DE INSERÇÃO ORBITAL (MPCORB): ID {asteroid_id} | Erro: {e}") 
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

    # --- 3.2 PROCESSAMENTO NEO.CSV (Funcionamento comprovado) ---
    if not os.path.exists(NEO_CSV_PATH):
        print(f"ERRO: Ficheiro neo.csv não encontrado em: {NEO_CSV_PATH}")
    else:
        print("\n--- Processamento de neo.csv ---")
        try:
            df_neo = pd.read_csv(NEO_CSV_PATH, delimiter=';', encoding='utf-8', low_memory=False)

            df_neo = df_neo.dropna(subset=['spkid']) 

            df_neo['neo'] = df_neo['neo'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)
            df_neo['pha'] = df_neo['pha'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)

            for col in numeric_cols:
                if col in df_neo.columns:
                    df_neo[col] = pd.to_numeric(df_neo[col], errors='coerce').fillna(0)

            # --- ASTEROIDES ÚNICOS ---
            asteroide_cols_map = ['full_name', 'neo', 'pha', 'diameter', 'h', 'albedo']
            df_asteroides_unicos = df_neo[asteroide_cols_map].drop_duplicates(subset=['full_name'])

            print(f"Inserindo {len(df_asteroides_unicos)} asteroides únicos...")
            
            asteroid_id_map = {} 
            count_inserted = 0

            for _, row in df_asteroides_unicos.iterrows():
                asteroid_id = inserir_asteroide_sp(cursor, row)
                
                if asteroid_id:
                    count_inserted += 1
                    asteroid_id_map[row['full_name']] = asteroid_id

            cnxn.commit()
            print(f"Concluído: {count_inserted} novos asteroides inseridos/atualizados.")
            
            # --- PARÂMETROS ORBITAIS NEO.CSV ---
            orbital_cols_neo = ['full_name', 'orbit_id', 'epoch_mjd', 'e', 'a', 'i', 'ma', 'moid_ld', 'rms']
            df_orbitas = df_neo[orbital_cols_neo].dropna(subset=['orbit_id', 'full_name'])

            df_orbitas = df_orbitas.rename(columns={'ma': 'M', 'epoch_mjd': 'epoch'}) 
            
            print(f"Iniciando a inserção de {len(df_orbitas)} parâmetros orbitais (neo.csv)...")
            count_orbits_inserted = 0

            for _, row in df_orbitas.iterrows():
                asteroid_id = asteroid_id_map.get(row['full_name'])
                
                if asteroid_id:
                    data_for_sp = {
                        'orbit_id': row['orbit_id'],
                        'epoch': row['epoch'],
                        'e': row['e'], 'a': row['a'], 'i': row['i'],
                        'M': row['M'], 'moid_ld': row['moid_ld'], 'rms': row['rms']
                    }
                    if inserir_parametro_orbital_sp(cursor, asteroid_id, data_for_sp):
                        count_orbits_inserted += 1

            cnxn.commit()
            print(f"Concluído: {count_orbits_inserted} parâmetros orbitais inseridos.")

        except Exception as e:
            cnxn.rollback()
            print(f"ERRO FATAL no processamento neo.csv: {e}")

    # --- 3.3 PROCESSAMENTO MPCORB.DAT (CORRIGIDO) ---
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

            # LISTA CORRIGIDA: Inclui todas as colunas que são FLOAT no SP/Tabela
            mpcorb_numeric_to_float = ['h', 'M', 'w', 'om', 'i', 'e', 'n', 'a', 'rms', 'Epoch', 'G']
            
            for col in mpcorb_numeric_to_float:
                if col in df_mpcorb.columns:
                    # CORREÇÃO: Força a conversão para float e substitui lixo por 0.0
                    df_mpcorb[col] = pd.to_numeric(df_mpcorb[col].astype(str).str.strip(), errors='coerce').fillna(0).astype(float)
            
            # Renomear para corresponder aos SPs
            df_mpcorb = df_mpcorb.rename(columns={'Desn': 'orbit_id', 'Epoch': 'epoch', 'M': 'M'})
            
            print(f"Iniciando a inserção de {len(df_mpcorb)} órbitas do MPCORB...")
            count_mpcorb_orbits_inserted = 0

            for _, row in df_mpcorb.iterrows():
                # 1. Insere/Atualiza o Asteroide (para garantir que existe na tabela e obter o ID)
                temp_asteroide = {
                    'full_name': row['full_name'],
                    'neo': 0, 'pha': 0, 'diameter': 0.0,
                    'h': row['h'], 'albedo': 0.0
                }
                asteroid_id = inserir_asteroide_sp(cursor, temp_asteroide)
                
                # 2. Insere o Parâmetro Orbital se tiver o ID
                if asteroid_id:
                    data_for_sp = {
                        'orbit_id': row['orbit_id'],
                        'epoch': row['epoch'],
                        'e': row['e'], 'a': row['a'], 'i': row['i'],
                        'M': row['M'], 
                        'moid_ld': float(0.0), # Moid_ld fixo como FLOAT
                        'rms': row['rms']
                    }

                    if inserir_parametro_orbital_sp(cursor, asteroid_id, data_for_sp):
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