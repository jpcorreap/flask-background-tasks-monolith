import smtplib
import ssl
from typing import List
from settings import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


context = ssl.create_default_context()


def send_email(to: str, message: str):
      with smtplib.SMTP(
        config.EMAIL_SERVER_HOST, config.EMAIL_SERVER_PORT
    ) as server:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Status Submission Update SuperVoices'
        msg['From'] = formataddr(('Super Voices', 'juanpa1202@gmail.com'))
        msg['To'] = to
        msg.attach(MIMEText(message, 'plain'))
        server.ehlo()
        server.starttls(context=context)
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        server.sendmail(
            config.EMAIL_USER,
            to,
            msg.as_string(),
        )


def send_many_emails(to: List[str], message: str):
    print(f"\n-> Enviando Emails a {len(to)} users")
    with smtplib.SMTP(
        config.EMAIL_SERVER_HOST, config.EMAIL_SERVER_PORT
    ) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        for receiver in to:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Status Submission Update SuperVoices'
            msg['From'] = formataddr(('Super Voices', 'juanpa1202@gmail.com'))
            msg['To'] = receiver
            msg.attach(MIMEText(message, 'plain'))
            server.sendmail(
                config.EMAIL_USER,
                receiver,
                msg.as_string(),
            )
