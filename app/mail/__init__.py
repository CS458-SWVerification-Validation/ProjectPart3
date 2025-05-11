import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

SENDER = os.environ.get('SENDER')
PASSWORD = os.environ.get('PASSWORD')
SMPT_SERVER = "smtp.gmail.com"
SMPT_PORT = 465

def send_email(subject, body, receiver):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER
        msg['To'] = receiver
        with smtplib.SMTP_SSL(SMPT_SERVER, SMPT_PORT) as smtp_server:
            smtp_server.login(SENDER, PASSWORD)
            smtp_server.sendmail(SENDER, receiver, msg.as_string())
        print("Message sent!")
    except Exception as e:
        print(e)