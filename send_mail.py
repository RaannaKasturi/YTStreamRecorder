import os
import brevo_python
from brevo_python.rest import ApiException
from dotenv import load_dotenv

load_dotenv()
mail_api = os.getenv("MAIL_API")

def mail_body(title, url, yt_url):
    body = f"""
    Hello,
    Nyberman had a new stream titled "{title}" from "{yt_url}".
    You can watch it at {url}.

    Regards,
    Nayan Kasturi (Raanna),
    https://nayankasturi.eu.org
    """
    return body

def email_ids(email_ids):
    emails = []
    for email in email_ids:
        emails.append({"email": email})
    return emails

def send_email(emails, title, url, yt_url):
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = mail_api
    api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
    data = mail_body(title=title, url=url, yt_url=yt_url)
    subject = f"'{title}' has been streamed by Nyberman Scientifically!"
    sender = {"name": "Nayan Kasturi", "email": "raanna@silerudaagartha.eu.org"}
    reply_to = {"name": "Nayan Kasturi", "email": "raanna@silerudaagartha.eu.org"}
    text_content = data
    emails = email_ids(emails)
    to = [{"email": 'raannakasturi@gmail.com'}]
    send_smtp_email = brevo_python.SendSmtpEmail(to=to, reply_to=reply_to, text_content=text_content, sender=sender, subject=subject)
    try:
        api_instance.send_transac_email(send_smtp_email)
        print("Email Sent")
        return True
    except ApiException as e:
        print("Can't send email")
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return False
