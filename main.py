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
MPCORB_DAT_PATH = os.path.join(BASE_DIR, 'MPCORB.DAT')

BATCH_SIZE = 10000 


# --- 2. FUNÇÃO DE INSERÇÃO EM MASSA (MANTIDA) ---

def bulk_insert_data(cursor, df, table_name, columns, commit_on_batch=True):
    """
    Executa a inserção em massa usando executemany do pyodbc em lotes.
    """
    
    quoted_columns = [f'[{col}]' for col in columns] 
    placeholders = ', '.join(['?'] * len(columns))
    sql_insert = f"INSERT INTO {table_name} ({', '.join(quoted_columns)}) VALUES ({placeholders})"
    
    total_rows = len(df)
    inserted_count = 0
    
    print(f"  > SQL Target: {table_name} | Colunas: {quoted_columns}")
    
    for i in range(0, total_rows, BATCH_SIZE):
        batch = df.iloc[i:i + BATCH_SIZE]
        data_to_insert = [tuple(x) for x in batch.values]
        
        try:
            cursor.executemany(sql_insert, data_to_insert)
        except pyodbc.Error as e:
            print(f"\n  ⚠️ ERRO FATAL no Lote {i // BATCH_SIZE}: {e}")
            cursor.connection.rollback()
            raise 
        
        if commit_on_batch:
            cursor.connection.commit()
        
        inserted_count += len(batch)
        print(f"  > Progresso: {inserted_count}/{total_rows} ({round(inserted_count/total_rows*100, 2)}%)")
    
    return inserted_count


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
            # 1. Leitura e Limpeza dos Dados
            df_neo = pd.read_csv(NEO_CSV_PATH, delimiter=';', encoding='utf-8', low_memory=False)
            
            # Limpeza das colunas 'neo', 'pha' e numéricas (mantendo 'spkid' no DF original)
            df_neo = df_neo.dropna(subset=['spkid']) # Mantemos a exclusão de linhas sem ID de asteroide
            
            # 🚨 MANTEMOS A LIMPEZA DE TIPO APENAS PARA O FK
            df_neo['spkid'] = pd.to_numeric(df_neo['spkid'], errors='coerce').astype('Int64')
            
            df_neo['neo'] = df_neo['neo'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)
            df_neo['pha'] = df_neo['pha'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)
            for col in numeric_cols:
                if col in df_neo.columns:
                    df_neo[col] = pd.to_numeric(df_neo[col], errors='coerce').fillna(0)


            # --- INSERÇÃO ASTEROIDES ÚNICOS ---
            
            # Colunas do DataFrame para a tabela Asteroid (EXCLUINDO spkid/Asteroid_id)
            asteroid_map_cols = ['full_name', 'neo', 'pha', 'diameter', 'h', 'albedo'] 
            
            # 🚨 Desduplicação AGORA baseada em 'full_name' (se 'spkid' fosse removido)
            # Como a FK em OrbitalParameter é crítica, vamos manter a desduplicação por spkid.
            df_asteroids_unicos = df_neo.drop_duplicates(subset=['spkid'])
            df_asteroids_unicos = df_asteroids_unicos[asteroid_map_cols] # Seleciona as colunas a inserir
            
            # Preparação Final
            df_asteroids_unicos['full_name'] = df_asteroids_unicos['full_name'].fillna('').astype(str)
            
            # 🚨 Usar o nome 'H' (maiúsculo) para corresponder ao esquema SQL
            df_asteroids_unicos = df_asteroids_unicos.rename(columns={'h': 'H'})
            asteroid_cols = ['full_name', 'neo', 'pha', 'diameter', 'H', 'albedo']
            
            df_asteroids_unicos = df_asteroids_unicos[asteroid_cols].astype(object) 

            print(f"Iniciando Inserção em Massa de {len(df_asteroids_unicos)} asteroides únicos...")
            
            # Inserção no Asteroid (Asteroid_ID é gerado automaticamente)
            count_inserted = bulk_insert_data(
                cursor, df_asteroids_unicos, 'Asteroid', asteroid_cols, commit_on_batch=True
            )
            print(f"Concluído: {count_inserted} novos asteroides inseridos/atualizados.")

            # --- INSERÇÃO PARÂMETROS ORBITAIS (FK para Asteroid_ID) ---
            # Aqui, ainda precisamos do spkid como chave temporária para FK
            
            orbital_map_cols = ['spkid', 'orbit_id', 'epoch_mjd', 'e', 'a', 'i', 'ma', 'moid_ld', 'rms']
            df_orbitas = df_neo[orbital_map_cols].dropna(subset=['orbit_id', 'spkid'])
            
            # Renomeia 'spkid' para 'Asteroid_id' no DF
            df_orbitas = df_orbitas.rename(columns={'spkid': 'Asteroid_id'})
            df_orbitas['orbit_id'] = df_orbitas['orbit_id'].astype(str).fillna('')
            
            orbital_cols = ['Asteroid_id', 'orbit_id', 'epoch_mjd', 'e', 'a', 'i', 'ma', 'moid_ld', 'rms']
            df_orbitas = df_orbitas[orbital_cols].astype(object)

            print(f"\nIniciando Inserção em Massa de {len(df_orbitas)} parâmetros orbitais (neo.csv)...")

            count_orbits_inserted = bulk_insert_data(
                cursor, df_orbitas, 'OrbitalParameter', orbital_cols, commit_on_batch=True
            )

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
            # 1. Leitura do Arquivo Fixo (FWF)
            colspecs = [
                (0, 6), (6, 12), (12, 13), (14, 25), (26, 36), (37, 47), (48, 58), 
                (59, 69), (70, 80), (80, 92), (92, 105), (105, 116), (116, 121), 
                (121, 124), (124, 133), (133, 138), (138, 142), (142, 150), (150, 172)
            ]
            names = [
                'Desn', 'h', 'G', 'Epoch', 'M', 'w', 'om', 'i', 'e', 'n', 'a',
                'Reference', 'ObsCount', 'OppCount', 'Arc', 'rms', 'Perts',
                'Computer', 'full_name'
            ]
            df_mpcorb = pd.read_fwf(
                MPCORB_DAT_PATH, colspecs=colspecs, header=None, names=names, encoding='latin1'
            )

            mpcorb_numeric = ['h', 'M', 'w', 'om', 'i', 'e', 'n', 'a', 'rms']
            for col in mpcorb_numeric:
                df_mpcorb[col] = pd.to_numeric(df_mpcorb[col].astype(str).str.strip(), errors='coerce').fillna(0)
            
            df_mpcorb = df_mpcorb.rename(columns={'Desn': 'spkid'})
            df_mpcorb['spkid'] = pd.to_numeric(df_mpcorb['spkid'], errors='coerce').astype('Int64')
            df_mpcorb = df_mpcorb.dropna(subset=['spkid'])
            df_mpcorb['orbit_id'] = df_mpcorb['spkid'].astype(str) + '_' + df_mpcorb['Epoch'].astype(str).str.strip()


            # --- INSERÇÃO ASTEROIDES ---
            asteroid_map_cols = ['full_name', 'h']
            df_mpcorb_asteroids = df_mpcorb.drop_duplicates(subset=['spkid'])
            df_mpcorb_asteroids = df_mpcorb_asteroids[asteroid_map_cols]
            
            # Adicionar colunas em falta
            df_mpcorb_asteroids['neo'] = 0
            df_mpcorb_asteroids['pha'] = 0
            df_mpcorb_asteroids['diameter'] = 0.0
            df_mpcorb_asteroids['albedo'] = 0.0
            df_mpcorb_asteroids['full_name'] = df_mpcorb_asteroids['full_name'].fillna('').astype(str)
            
            # Renomear h para H e definir ordem final para SQL Server
            df_mpcorb_asteroids = df_mpcorb_asteroids.rename(columns={'h': 'H'})
            asteroid_final_cols = ['full_name', 'neo', 'pha', 'diameter', 'H', 'albedo']
            df_mpcorb_asteroids = df_mpcorb_asteroids[asteroid_final_cols].astype(object)
            
            print(f"Iniciando Inserção em Massa de {len(df_mpcorb_asteroids)} asteroides do MPCORB...")
            bulk_insert_data(
                cursor, df_mpcorb_asteroids, 'Asteroid', asteroid_final_cols, commit_on_batch=True
            )
            
            
            # --- INSERÇÃO PARÂMETROS ORBITAIS MPCORB ---
            df_mpcorb_orbitas = df_mpcorb.rename(columns={'Epoch': 'epoch_mjd', 'M': 'ma', 'spkid': 'Asteroid_id'})
            
            # Adicionar campo em falta
            df_mpcorb_orbitas['moid_ld'] = 0.0
            
            # Ordem final das colunas (MANTÉM Asteroid_id)
            orbital_final_cols = ['Asteroid_id', 'orbit_id', 'epoch_mjd', 'e', 'a', 'i', 'ma', 'moid_ld', 'rms']
            df_mpcorb_orbitas = df_mpcorb_orbitas[orbital_final_cols].astype(object)
            
            print(f"\nIniciando Inserção em Massa de {len(df_mpcorb_orbitas)} órbitas do MPCORB...")
            count_mpcorb_orbits_inserted = bulk_insert_data(
                cursor, df_mpcorb_orbitas, 'OrbitalParameter', orbital_final_cols, commit_on_batch=True
            )
            
            print(f"Concluído: {count_mpcorb_orbits_inserted} órbitas do MPCORB inseridas.")

        except Exception as e:
            cnxn.rollback()
            print(f"ERRO FATAL no processamento MPCORB.DAT: {e}")

    # --- 3.4 FECHAR CONEXÃO ---
    cursor.close()
    cnxn.close()
    print("\nConexão fechada. ETL concluído com sucesso.")


if __name__ == "__main__":
    run_etl()