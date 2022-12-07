import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

from loguru import logger

from settings import MAIL_EMAIL, MAIL_PASS

from template import get_html_text


def send_fraud_report_on_mail(recipient_mail: str, report_url: str):

    server = smtplib.SMTP_SSL('smtp.yandex.ru')
    server.set_debuglevel(0)
    server.secure = True
    try:
        server.login(MAIL_EMAIL, MAIL_PASS)
        logger.success("logged in smtp server")
    
    except:
        logger.error("unable to login to smtp server")
        return False
    


    msg = MIMEMultipart('alternative')
    msg['Subject'] = "FRAUD REPORT"
    msg['From'] = MAIL_EMAIL
    msg['To'] = recipient_mail

    html_text = get_html_text(report_url)

    html_template = MIMEText(html_text, 'html')
    msg.attach(html_template)

    try:
        server.sendmail(MAIL_EMAIL, recipient_mail, msg.as_string())
        logger.success(f"report sent to {recipient_mail}")
    except:
        logger.error(f"unable to send message on email:{recipient_mail}")
        return False
    
    server.quit()
    return True


