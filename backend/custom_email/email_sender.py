import smtplib
import ssl
from typing import List

from settings import EMAIL_PASSWORD, EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, EMAIL_USER

context = ssl.create_default_context()


def send_email(to: str, message: str):
    with smtplib.SMTP_SSL(
        EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, context=context
    ) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_USER,
            to,
            message,
        )


def send_many_emails(to: List[str], message: str):
    with smtplib.SMTP_SSL(
        EMAIL_SERVER_HOST, EMAIL_SERVER_PORT, context=context
    ) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        for receiver in to:
            server.sendmail(
                EMAIL_USER,
                receiver,
                message,
            )
