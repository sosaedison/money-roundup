import smtplib
from email.message import EmailMessage
from typing import Protocol

import boto3

from moneyroundup.dependencies import _get_secret_value
from moneyroundup.settings import settings


class EmailService(Protocol):
    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Send an email to the given email address with the given subject and body.
        """
        ...


def EmailFactory(env: str) -> EmailService:
    """
    Return an email service based on the given service type.
    """
    email_service_by_env = {
        "DEV": LocalEmailService,
        "PRODUCTION": ProductionEmailService,
    }

    if env not in email_service_by_env:
        raise KeyError(f"Invalid email service type: {env}")
    return email_service_by_env.get(env, LocalEmailService)


class ProductionEmailService:

    """
        response = client.send_email(
        Source='string',
        Destination={
            'ToAddresses': [
                'string',
            ],
            'CcAddresses': [
                'string',
            ],
            'BccAddresses': [
                'string',
            ]
        },
        Message={
            'Subject': {
                'Data': 'string',
                'Charset': 'string'
            },
            'Body': {
                'Text': {
                    'Data': 'string',
                    'Charset': 'string'
                },
                'Html': {
                    'Data': 'string',
                    'Charset': 'string'
                }
            }
        },
        ReturnPath='string',
        SourceArn='string',
        ReturnPathArn='string',
        Tags=[
            {
                'Name': 'string',
                'Value': 'string'
            },
        ],
        ConfigurationSetName='string'
    )
    """

    @staticmethod
    def send_email(
        to: str,
        subject: str = "This is an email subject",
        body: str = "This is an email body",
        source: str = "no-reply@moneyroundup.com",
    ) -> None:
        ses_client = boto3.client("ses")
        ses_client.send_email(
            Source=source,
            Destination={"ToAddresses": [to]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )


class LocalEmailService:
    @staticmethod
    def send_email(
        to: str,
        subject: str = "This is an email subject",
        body: str = "This is an email body",
    ) -> None:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = "MoneyRoundup"
        msg["To"] = to

        with smtplib.SMTP(
            settings.EMAIL_SERVICE_HOST, settings.EMAIL_SERVICE_PORT
        ) as smtp:
            smtp.starttls()
            smtp.login(
                settings.EMAIL_SERVICE_USERNAME,
                _get_secret_value(settings.EMAIL_SERVICE_PASSWORD),
            )
            smtp.send_message(msg)
