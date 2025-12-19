# app_graficos_alertas.py

import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from main import get_connection
import pandas as pd

# =========================
def carregar_dados():
    """Carrega dados da view do SQL Server"""
    try:
        conn = get_connection()
        query = "SELECT full_name, Priority, Torino FROM vw_App_Completa"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar dados:\n{e}")
        return pd.DataFrame()

def gerar_grafico_prioridade():
    df = carregar_dados()
    if df.empty:
        return
    prioridade_counts = df['Priority'].value_counts()
    plt.figure(figsize=(8,5))
    prioridade_counts.plot(kind='bar', color='skyblue')
    plt.title('Número de Alertas por Prioridade')
    plt.xlabel('Prioridade')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def gerar_grafico_neo_pha():
    """Gera gráfico comparando NEO, PHA e NEO+PHA"""
    try:
        conn = get_connection()
        query = """
            SELECT
                SUM(CASE WHEN NEO = 'Y' THEN 1 ELSE 0 END) as total_neo,
                SUM(CASE WHEN PHA = 'Y' THEN 1 ELSE 0 END) as total_pha,
                SUM(CASE WHEN NEO = 'Y' AND PHA = 'Y' THEN 1 ELSE 0 END) as total_neo_pha
            FROM vw_App_Completa
        """
        counts = pd.read_sql(query, conn).iloc[0]
        conn.close()

        categorias = ['NEO', 'PHA']
        valores = [counts['total_neo'], counts['total_pha']]

        plt.figure(figsize=(8,5))
        plt.bar(categorias, valores, color=['pink', 'purple'])
        plt.title('Asteroides NEO, PHA')
        plt.ylabel('Quantidade')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao gerar gráfico NEO/PHA:\n{e}")

def gerar_grafico_risco_colisao(top_n=10):
    """Gera gráfico dos asteroides com maior probabilidade de colisão (maior Torino)"""
    try:
        conn = get_connection()
        query = """
            SELECT full_name, Torino
            FROM vw_App_Completa
            WHERE Torino IS NOT NULL
            ORDER BY Torino DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("Informação", "Não há asteroides com Torino registrado.")
            return

        # Seleciona os top N asteroides mais perigosos
        df_top = df.head(top_n)

        plt.figure(figsize=(10,6))
        plt.barh(df_top['full_name'], df_top['Torino'], color='red')
        plt.xlabel('Torino (Probabilidade/Risco)')
        plt.ylabel('Asteroide')
        plt.title(f'Top {top_n} Asteroides com Maior Probabilidade de Colisão')
        plt.gca().invert_yaxis()  # inverte eixo para maior risco no topo
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao gerar gráfico de risco:\n{e}")



