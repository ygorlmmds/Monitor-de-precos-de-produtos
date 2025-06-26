# ==== EXTRA ====

import smtplib
from email.message import EmailMessage
import os

def enviar_email (produtos):
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
