from threading import Thread
import os
from flask import current_app
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Configure Brevo API client
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_async_email(subject, sender, recipients, html_body):
    with current_app.app_context():
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email} for email in recipients],
            sender={"email": sender},
            subject=subject,
            html_content=html_body
        )
        try:
            api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            current_app.logger.error(f"Brevo API error: {e}")

def send_email(subject, sender, recipients, text_body, html_body):
    current_app.logger.info(f"Starting email thread for {recipients}")
    Thread(target=send_async_email,
           args=(subject, sender, recipients, html_body)).start()
