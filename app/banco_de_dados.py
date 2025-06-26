# = PARTE SQLite =

import sqlite3
import pandas as pd

def criar_bd (produtos_ordenados):
    #Criando o banco de dados e o cursor SQLite
    df = pd.DataFrame(produtos_ordenados)

    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()

    #Criando a tabela 

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    nome UNIQUE,
                    preco,
                    preco_limpo
            )
    """)

    #Limpando a tabela (caso queira)

    # cursor.execute("DELETE FROM produtos")
    # conexao.commit()

    #Inserir dados na tabela

    for _, row in df.iterrows():
        cursor.execute("""
                    INSERT OR IGNORE INTO produtos (nome, preco, preco_limpo)
                    VALUES (?, ?, ?)               
        """, (row['nome'], row['preco'], row['preco_limpo']))
        conexao.commit()

    #Consultando o banco de dados

    cursor.execute("SELECT * FROM produtos")

    resultado = cursor.fetchall()

    for linha in resultado:
        print(linha)