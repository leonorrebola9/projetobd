import pandas as pd
import pyodbc
import os

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=PC0ADRIANA\SQLEXPRESS;'
    r'DATABASE=projeto;'
    r'Trusted_Connection=yes;'
)

try:
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    print("Conexao ao SQL Server estabelecida com sucesso.")
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Erro ao conectar ao SQL Server: {sqlstate}")
    exit()



def inserir_asteroide(cursor, data):
    """
    Insere um asteroide unico na tabela dbo.Asteroide.
    Recomendacao: Usar um Stored Procedure aqui e mais seguro e eficiente.
    """
    # A query T-SQL abaixo e um exemplo de INSERT simples.
    # No SQL Server, voce deve criar um Stored Procedure que faca o INSERT
    # e chama-lo aqui (e.g., cursor.execute("{CALL SP_InserirAsteroide (?, ?, ...)}", ...))
    
    # Exemplo de INSERT simples em T-SQL:
    query = """
    INSERT INTO dbo.Asteroide (spkid, full_name, name, pha, neo, H, diameter, albedo)
    SELECT ?, ?, ?, ?, ?, ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM dbo.Asteroide WHERE spkid = ?);
    """
    
    try:
        cursor.execute(query, 
                       data['spkid'], data['full_name'], data['name'], 
                       data['pha'], data['neo'], data['H'], data['diameter'], 
                       data['albedo'], data['spkid']) # O ultimo spkid e para a clausula WHERE NOT EXISTS
        return True
    except pyodbc.IntegrityError as e:
        # Se for um erro de integridade (e.g., PK duplicada), ignora ou loga
        cnxn.rollback()
        # print(f"Erro de Integridade ao inserir Asteroide {data['spkid']}: {e}")
        return False
    except Exception as e:
        cnxn.rollback()
        print(f"Erro geral: {e}")
        return False

def inserir_parametro_orbital(cursor, data):
    """
    Insere um conjunto de parâmetros orbitais na tabela dbo.Orbital_Parameter.
    """
    # Certifique-se de que os nomes das colunas e a ordem estao corretos
    query = """
    INSERT INTO dbo.Orbital_Parameter (
        spkid, orbit_id, epoch, e, a, i, rms, moid_ld, class, sigma_i, sigma_e
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    try:
        cursor.execute(query, 
                       data['spkid'], data['orbit_id'], data['epoch_mjd'], 
                       data['e'], data['a'], data['i'], data['rms'], 
                       data['moid_ld'], data['class'], data['sigma_i'], data['sigma_e'])
        return True
    except Exception as e:
        cnxn.rollback()

        return False


csv_path = 'neo.csv' 

if not os.path.exists(csv_path):
    print(f"ERRO: Ficheiro nao encontrado em: {csv_path}")
    exit()

# Leitura eficiente com Pandas
try:
    # low_memory=False a crucial para CSVs grandes para inferir tipos corretamente
    df_neo = pd.read_csv(csv_path, delimiter=',', encoding='utf-8', low_memory=False)
    
    # Filtro essencial para garantir que o spkid (PK/FK) nao e nulo e um numero inteiro
    df_neo = df_neo.dropna(subset=['spkid'])
    df_neo['spkid'] = df_neo['spkid'].astype(pd.Int64Dtype) # Para garantir tipo correto
    
    print(f"Ficheiro CSV lido com {len(df_neo)} linhas.")
except Exception as e:
    print(f"Erro ao ler o ficheiro CSV: {e}")
    exit()