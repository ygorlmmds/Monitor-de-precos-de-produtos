
from app.scraping import extracao
from app.csv_exporter import criar_csv
from app.banco_de_dados import criar_bd
from app.email_sender import enviar_email

produtos = extracao()
produtos_ordenados = criar_csv(produtos)

criar_csv(produtos)
criar_bd(produtos_ordenados)
enviar_email(produtos)







