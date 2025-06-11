Esse projeto faz a automação da coleta de dados de notebooks no Mercado Livre, ordena os dados por preço, salva em um CSV, armazena no SQLite e envia por e-mail.


# ==== FUNCIONALIDADES ====

-Coleta os dados dos produtos pelo site 
-Ordena os produtos do menor para o maior
-Salva em um arquivo .CSV
-Armazena os dados em um banco de dados SQLite
-Envia o arquivo por email

# === FERRAMENTAS ===

-Linguagem Python

-Selenium

-Pandas

-SQLite3 

# ==== AMBIENTE VIRTUAL ====

-Criar o ambiente

python -m venv venv

-Ativar o ambiente:

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

-Instalar o requirements(depedencias)

pip install -r requirements.txt

-Ao terminar, desative o ambiente:

deactivate