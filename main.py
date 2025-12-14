import pandas as pd
import pyodbc
import os
import sys
import webbrowser

# --- 1. CONFIGURAÇÃO DA CONEXÃO E CAMINHOS ---

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=172.20.10.12\SQLEXPRESS,1433;'
        'DATABASE=projeto;'
        'UID=adriana;'
        'PWD=12345;'
    )


def img_path(nome):

    """ Retorna o caminho completo da imagem dado o nome do arquivo. """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, "Imagens_app", nome)


def open_nasa():
    webbrowser.open("https://www.nasa.gov/")

def open_insta():
    webbrowser.open("https://www.instagram.com/nasa/")

def open_twitter():
    webbrowser.open("https://x.com/NASA")

def open_facebook():
    webbrowser.open("https://www.facebook.com/NASA/")

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/company/nasa/?originalSubdomain=pt")





