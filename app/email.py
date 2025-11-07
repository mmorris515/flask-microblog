from threading import Thread
import os
import traceback
from flask import current_app
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_async_email(app, subject, sender, recipients, html_body):
    with app.app_context():
        try:
            app.logger.info(f"send_async_email started for {recipients}")

            # Configure Brevo API client
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = app.config['BREVO_API_KEY']
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": email} for email in recipients],
                sender={"email": sender},
                subject=subject,
                html_content=html_body
            )
            api_instance.send_transac_email(send_smtp_email)
            app.logger.info(f"Email sent successfully to {recipients}")
        except Exception as e:
            app.logger.error(f"Email send failed: {e}")
            app.logger.error(traceback.format_exc())


def send_email(subject, sender, recipients, text_body, html_body):
    from flask import current_app
    app = current_app._get_current_object()  # get the actual app instance
    app.logger.info(f"send_email called for {recipients}")
    Thread(target=send_async_email,
           args=(app, subject, sender, recipients, html_body)).start()