import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent / ".env")
print(f"USER: {os.getenv('GMAIL_USER')}")
print(f"PASS: {os.getenv('GMAIL_PASSWORD')}")

def enviar_reporte():
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    recipient = os.getenv("RECIPIENT")

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = "Retail Weekly Report — Semana 03-09 Sep 2017"

    body = """
    Hola,

    Adjunto encontrarás el reporte semanal de ventas retail.
    Pronto tendremos highlights semanales para incrementar el impacto de este reporte automatizado!

    Saludos,
    Ricardo Vargas.
    """
    msg.attach(MIMEText(body, 'plain'))

    with open("outputs/report.html", "rb") as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename='retail_report.html')
        msg.attach(attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print("Reporte enviado exitosamente")