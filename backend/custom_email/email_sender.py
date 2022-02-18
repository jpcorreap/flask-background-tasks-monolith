import smtplib
import ssl
from typing import List
from settings import config


context = ssl.create_default_context()


def send_email(to: str, message: str):
      with smtplib.SMTP(
        config.EMAIL_SERVER_HOST, config.EMAIL_SERVER_PORT
    ) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        server.sendmail(
            config.EMAIL_USER,
            to,
            message,
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
            server.sendmail(
                config.EMAIL_USER,
                receiver,
                message,
            )
