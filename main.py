# ==== importações ====
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

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

#iniciando o navegador

driver = webdriver.Chrome()
driver.maximize_window()

# Acessando o site 

driver.get("https://www.mercadolivre.com.br")

#Buscando Notebooks

barra_busca = driver.find_element('id', 'cb1-edit')
barra_busca.send_keys('Notebook')
barra_busca.send_keys(Keys.ENTER)

#Scrollando até os 3 primeros resultados  

rolar_400px(driver)

#Coletando informações dos 3 primeiros 3/6

produtos = extrair_dados(driver)
print(produtos)


time.sleep(3)

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