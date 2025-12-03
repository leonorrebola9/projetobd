import pyodbc

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=172.20.10.12\SQLEXPRESS,1433;'
    r'DATABASE=projeto;'
    r'UID=adriana;'
    r'PWD=12345;'
)

try:
    conn = pyodbc.connect(conn_str, timeout=5)
    print("✅ Conectou com sucesso ao SQL Server!")
except Exception as e:
    print("❌ Erro:", e)

