import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")

def sendMail(to, subject, body):
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_email_pass')
    
    body = body

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to

    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return f"Mail sent to {to}.", True
    except Exception as e:
        return f"Failed to send email. Try again after some time.", False
