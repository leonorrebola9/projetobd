import pandas as pd
import pyodbc
import os
import sys

# --- 1. CONFIGURAÇÃO DA CONEXÃO E CAMINHOS ---

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=172.20.10.12\SQLEXPRESS,1433;'
        'DATABASE=projeto;'
        'UID=adriana;'
        'PWD=12345;'
    )





