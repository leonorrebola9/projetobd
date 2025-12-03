import pandas as pd
import pyodbc
import os
import sys

# --- 1. CONFIGURAÇÃO DA CONEXÃO E CAMINHOS ---

# Seu caminho de conexão
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-VG0H1U7H\SQLEXPRESS;'
    r'DATABASE=projeto;'
    r'Trusted_Connection=yes;'
)

# Define o diretório base onde o script está a correr (para robustez)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEO_CSV_PATH = os.path.join(BASE_DIR, 'neo.csv')
MPCORB_DAT_PATH = os.path.join(BASE_DIR, 'MPCORB.DAT')

# --- 2. FUNÇÕES DE INSERÇÃO (CHAMADA AOS STORED PROCEDURES) ---

def inserir_asteroide_sp(cursor, data):
    """
    Chama o SP SP_InserirAsteroide no SQL Server.
    Asteroide_ID (spkid) é a chave primária.
    
    NOTA: O SP deve estar criado no SQL Server.
    Parâmetros: @Asteroide_ID, @full_name, @neo, @pha, @diameter, @H, @Albedo
    """
    sp_call = "{CALL SP_InserirAsteroide (?, ?, ?, ?, ?, ?, ?)}"
    
    try:
        # Aceder aos dados do Pandas. Note que a coluna 'h' no Pandas é 'H' no SP
        cursor.execute(sp_call, 
                       data['spkid'], data['full_name'], data['neo'], data['pha'], 
                       data['diameter'], data['h'], data['albedo'])
        # Puxa o resultado do SP (Status e Mensagem)
        result = cursor.fetchone() 
        return result and result[0] == 1 # Retorna True se o status for 1 (sucesso)
    except pyodbc.IntegrityError:
        # Erro comum se Asteroide_ID já existir (o SP deve tratar, mas esta é a salvaguarda)
        return False
    except Exception as e:
        # print(f"Erro ao chamar SP_InserirAsteroide para {data['spkid']}: {e}")
        return False

def inserir_parametro_orbital_sp(cursor, data):
    """
    Chama o SP SP_InserirOrbitalParameter no SQL Server.
    Asteroide_ID (spkid) é a chave estrangeira.
    
    Parâmetros: @Asteroide_ID, @orbit_id, @epoch, @e, @a, @i, @M, @moid_ld, @rms
    """
    sp_call = "{CALL SP_InserirOrbitalParameter (?, ?, ?, ?, ?, ?, ?, ?, ?)}"
    
    try:
        # Assumimos que 'ma' no CSV é 'M' na BD.
        # Os campos moid_ld e rms são cruciais para o TRIGGER de alerta.
        cursor.execute(sp_call, 
                       data['spkid'], data['orbit_id'], data['epoch_mjd'], 
                       data['e'], data['a'], data['i'], data['ma'], data['moid_ld'], data['rms'])
        return True
    except pyodbc.IntegrityError:
        # Erro comum: Chave Estrangeira (spkid) não existe na tabela Asteroide
        return False
    except Exception as e:
        # print(f"Erro ao chamar SP_InserirOrbitalParameter para {data['spkid']}: {e}")
        return False


# --- 3. FUNÇÃO PRINCIPAL DE ETL ---
def run_etl():
    """Executa o processo de Extração, Transformação e Carga para os dois ficheiros."""
    
    # --- 3.1 CONEXÃO ---
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        print("✅ Conexão ao SQL Server estabelecida com sucesso.")
    except pyodbc.Error as ex:
        print(f"❌ Erro ao conectar ao SQL Server: {ex}")
        sys.exit(1)

    # Definir colunas numéricas para tratamento de tipos e nulos (usando a caixa de letras correta: 'h' minúsculo)
    numeric_cols = ['h', 'diameter', 'albedo', 'e', 'a', 'q', 'i', 'om', 'w', 'ma', 
                    'moid_ld', 'rms', 'diameter_sigma', 'sigma_e', 'sigma_a', 'sigma_i', 'sigma_w', 'sigma_ma']
    
    # --- 3.2 PROCESSAMENTO NEO.CSV ---
    if not os.path.exists(NEO_CSV_PATH):
        print(f"ERRO: Ficheiro neo.csv não encontrado em: {NEO_CSV_PATH}")
    else:
        print("\n--- Processamento de neo.csv ---")
        try:
            # LER COM PONTO E VÍRGULA, pois a maioria dos ficheiros deste trabalho usa ';'
            df_neo = pd.read_csv(NEO_CSV_PATH, delimiter=';', encoding='utf-8', low_memory=False)
            
            # Limpeza de spkid
            df_neo = df_neo.dropna(subset=['spkid'])
            df_neo['spkid'] = pd.to_numeric(df_neo['spkid'], errors='coerce').astype('Int64')
            
            # Pré-processamento e Limpeza de Flags/Numéricos
            df_neo['neo'] = df_neo['neo'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)
            df_neo['pha'] = df_neo['pha'].map({'Y': 1, 'N': 0}).fillna(0).astype(int)
            for col in numeric_cols:
                if col in df_neo.columns:
                     # Converte para numérico e preenche NaN com 0
                     df_neo[col] = pd.to_numeric(df_neo[col], errors='coerce').fillna(0)
            
            # --- Carga de Asteroides Únicos ---
            asteroide_cols = ['spkid', 'full_name', 'name', 'pha', 'neo', 'h', 'diameter', 'albedo']
            df_asteroides_unicos = df_neo[asteroide_cols].drop_duplicates(subset=['spkid'])
            
            print(f"Inserindo {len(df_asteroides_unicos)} asteroides únicos...")
            count_inserted = 0
            
            # Usa transação única para maior performance
            for index, row in df_asteroides_unicos.iterrows():
                if inserir_asteroide_sp(cursor, row):
                    count_inserted += 1
            
            cnxn.commit()
            print(f"Concluído: {count_inserted} novos asteroides inseridos/atualizados.")
            
            # --- Carga de Parâmetros Orbitais ---
            # orbital_cols deve incluir todos os campos necessários para o SP
            orbital_cols = ['spkid', 'orbit_id', 'epoch_mjd', 'e', 'a', 'i', 'ma', 'moid_ld', 'rms']
            df_orbitas = df_neo[orbital_cols].dropna(subset=['orbit_id'])

            print(f"Iniciando a inserção de {len(df_orbitas)} parâmetros orbitais (neo.csv)...")
            count_orbits_inserted = 0
            
            for index, row in df_orbitas.iterrows():
                if inserir_parametro_orbital_sp(cursor, row):
                    count_orbits_inserted += 1
            
            cnxn.commit()
            print(f"Concluído: {count_orbits_inserted} parâmetros orbitais inseridos.")

        except Exception as e:
            cnxn.rollback()
            print(f"ERRO FATAL no processamento neo.csv: {e}. Provavelmente tipo de dados incorreto no SQL.")
            
    # --- 3.3 PROCESSAMENTO MPCORB.DAT (Leitura de Largura Fixa) ---
    if not os.path.exists(MPCORB_DAT_PATH):
        print(f"\nERRO: Ficheiro MPCORB.DAT não encontrado em: {MPCORB_DAT_PATH}")
    else:
        print("\n--- Processamento de MPCORB.DAT (Largura Fixa - read_fwf) ---")
        try:
            # Larguras fixas (Colspecs) baseadas no formato padrão MPCORB:
            colspecs = [
                (0, 6),     # 0-5 Des'n
                (6, 12),    # 6-11 H
                (12, 13),   # 12 G
                (14, 25),   # 14-24 Epoch (JD)
                (26, 36),   # 26-35 M (Anomalia Média)
                (37, 47),   # 37-46 Peri. (w)
                (48, 58),   # 48-57 Node (om)
                (59, 69),   # 59-68 Incl. (i)
                (70, 80),   # 70-79 e (Excentricidade)
                (80, 92),   # 80-91 n (Movimento médio diário)
                (92, 105),  # 92-104 a (Semi-eixo maior)
                (105, 116), # 105-115 Reference
                (116, 121), # 116-120 #Obs
                (121, 124), # 121-123 #Opp
                (124, 133), # 124-132 Arc
                (133, 138), # 133-137 rms
                (138, 142), # 138-141 Perts
                (142, 150), # 142-149 Computer
                (150, 172), # 150-171 Nome (full_name)
            ]

            names = [
                'Desn', 'h', 'G', 'Epoch', 'M', 'w', 'om', 'i', 'e', 'n', 'a', 
                'Reference', 'ObsCount', 'OppCount', 'Arc', 'rms', 'Perts', 'Computer', 'full_name'
            ]

            df_mpcorb = pd.read_fwf(
                MPCORB_DAT_PATH,
                colspecs=colspecs,
                header=None,
                names=names,
                encoding='latin1'
            )
            
            # --- Lógica de Inserção MPCORB ---
            print(f"Ficheiro MPCORB.DAT lido com sucesso e {len(df_mpcorb)} linhas.")
            
            # Limpeza e Mapeamento para Numérico (Apenas para as colunas necessárias para Orbital_Parameter)
            mpcorb_numeric_cols = ['h', 'M', 'w', 'om', 'i', 'e', 'n', 'a', 'rms']
            for col in mpcorb_numeric_cols:
                df_mpcorb[col] = pd.to_numeric(df_mpcorb[col].str.strip(), errors='coerce').fillna(0)
            
            # Para ligar MPCORB ao Asteroide_ID (spkid):
            # 1. Tente usar 'Desn' como o spkid (para asteroides numerados).
            # 2. Requer uma busca no BD ou uma tabela de mapeamento para não numerados.
            
            # Assumimos que 'Desn' pode ser convertido para Asteroide_ID (spkid) se for um número:
            df_mpcorb['spkid'] = pd.to_numeric(df_mpcorb['Desn'], errors='coerce').astype('Int64')
            df_mpcorb = df_mpcorb.dropna(subset=['spkid'])

            # Prepara os dados de órbita do MPCORB
            df_mpcorb['orbit_id'] = df_mpcorb['Desn'] + '_' + df_mpcorb['Epoch'].astype(str)
            
            # Mapeia colunas para o SP_InserirOrbitalParameter (deve corresponder ao SP)
            mpcorb_orbit_cols = ['spkid', 'orbit_id', 'Epoch', 'e', 'a', 'i', 'M', 'rms']
            
            print(f"Iniciando a inserção de {len(df_mpcorb)} órbitas do MPCORB.DAT...")
            count_mpcorb_orbits_inserted = 0
            
            for index, row in df_mpcorb.iterrows():
                # NOTE: Para o MPCORB, precisamos de 'moid_ld'. Como não existe, vamos passar 0 ou NULL
                # O SP DEVE SER AJUSTADO PARA ACEITAR NULLS/0 PARA ESTE CAMPO AQUI.
                data_for_sp = {
                    'spkid': row['spkid'],
                    'orbit_id': row['orbit_id'],
                    'epoch_mjd': row['Epoch'],
                    'e': row['e'],
                    'a': row['a'],
                    'i': row['i'],
                    'ma': row['M'], # Mapeando M do MPCORB para ma do SP
                    'moid_ld': 0.0, # Valor fictício, pois não existe no MPCORB
                    'rms': row['rms']
                }
                
                # Para inserir a órbita, o Asteroide_ID (spkid) já tem de existir!
                # Podemos tentar inserir primeiro o asteroide (se ele não existir no neo.csv):
                temp_asteroide = {
                    'spkid': row['spkid'],
                    'full_name': row['full_name'],
                    'neo': 0, # Assumimos não-NEO, a menos que haja classificação
                    'pha': 0,
                    'diameter': 0.0, # Não existe no MPCORB
                    'h': row['h'],
                    'albedo': 0.0
                }
                inserir_asteroide_sp(cursor, temp_asteroide) # Tenta inserir o asteroide primeiro
                
                # Tenta inserir a órbita
                if inserir_parametro_orbital_sp(cursor, data_for_sp):
                     count_mpcorb_orbits_inserted += 1

            cnxn.commit()
            print(f"Concluído: {count_mpcorb_orbits_inserted} parâmetros orbitais do MPCORB.DAT inseridos.")


        except Exception as e:
            cnxn.rollback()
            print(f"ERRO FATAL no processamento MPCORB.DAT: {e}")


    # --- 3.4 FECHAR CONEXÃO ---
    cursor.close()
    cnxn.close()
    print("\nConexão e Carga de dados concluídas. Conexão fechada.")


if __name__ == "__main__":
    run_etl()