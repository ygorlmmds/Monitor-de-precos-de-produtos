# ==== importações ====
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

import pandas as pd
import re

import sqlite3

import smtplib
from email.message import EmailMessage
import os

# ==== funções auxiliares ====

#função srollar 400px

def rolar_400px(driver):
    driver.execute_script('window.scrollBy(0, 400);')

#função scrollar 600px
def rolar_800px(driver):
    driver.execute_script('window.scrollBy(0, 800);')

#função extrair dados 

def extrair_dados(driver, limite=6):
    produtos = []

    rolar_400px(driver)

    blocos_a =  driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__wrapper")[:3]

    for bloco in blocos_a:
        try:
            nome = bloco.find_element(By.CSS_SELECTOR, "a.poly-component__title").text
            preco = bloco.find_element(By.CSS_SELECTOR, ".andes-money-amount").text
            produtos.append({
                "nome": nome,
                "preco": f"{preco}"

            })
        except:
            continue
    time.sleep(5)

    rolar_800px(driver)

    time.sleep(5)

    blocos_b = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result__wrapper")[3:6]
    for bloco in blocos_b:
        try:
            nome = bloco.find_element(By.CSS_SELECTOR, "a.poly-component__title").text
            preco = bloco.find_element(By.CSS_SELECTOR, ".andes-money-amount").text
            produtos.append({
                "nome": nome,
                "preco": f"{preco}"

            })
        except:
            continue
    return produtos



# ==== CÓDIGO PRINCIPAL ====



# = PARTE SELENIUM =


#iniciando o navegador

driver = webdriver.Chrome()
driver.maximize_window()

# Acessando o site 

driver.get("https://www.mercadolivre.com.br")

#Buscando Notebooks

barra_busca = driver.find_element('id', 'cb1-edit')
barra_busca.send_keys('Notebook')
barra_busca.send_keys(Keys.ENTER)

#Coletando informações dos produtos

produtos = extrair_dados(driver)
print(produtos)


time.sleep(3)

# = PARTE PANDAS =


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

# = PARTE SQLite =


#Criando o banco de dados e o cursor SQLite

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




# ==== EXTRA ====


# construção das informações

email_remetente ='ygorlima00778@gmail.com'
email_destinatario = 'ygorlima00778@gmail.com'
email_senha = 'ywnl dfne nstx gyki'

caminho_anexo = 'produtos.csv'
corpo_email = """
Olá,

Segue em anexo os dados da busca feita pelo monitor.

Atenciosamente,
Dev.

"""

mensagem = EmailMessage()
mensagem['From'] = email_remetente
mensagem['To'] = email_destinatario
mensagem['Subject'] = 'Teste de anexo CSV'

mensagem.set_content(corpo_email)

with open ('produtos.csv', 'rb') as f:
    conteudo = f.read()
    mensagem.add_attachment(conteudo, maintype = 'application', subtype = 'octet-stream', filename = 'produtos.csv')
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_remetente, email_senha)
    smtp.send_message(mensagem)
