# = PARTE PANDAS =

import pandas as pd
import re
from app.scraping import produtos

produtos = produtos

def criar_csv (produtos):

    #Criando um DataFrame com os dados coletados

    df = pd.DataFrame(produtos)

    #extraindo o valor, sem os sinais

    df['preco_limpo'] = df['preco'].str.replace(r'[R$\.\n\\]', '', regex=True)

    print(df)

    #ordenando do menor ao maior

    produtos_ordenados = df.sort_values('preco_limpo')
    print(produtos_ordenados)

    #Eportando o Dataframe com csv

    df = produtos_ordenados
    df.to_csv('produtos.csv', index=False)

    return produtos_ordenados