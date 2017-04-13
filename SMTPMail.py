import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE
from email import Encoders
import BotCredentials

def prepare_attachment(attachment):
    """Prepares the attachment and sets necessary fields for sending"""
    attachment_component = MIMEBase('application', "octet-stream")
    attachment_component.set_payload(open(attachment,"rb").read())
    Encoders.encode_base64(attachment_component)
    attachment_component.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
    return attachment_component

def send_mail(bot_address, bot_password, send_to, subject, body, files):
    """Sends an email from and to the specified addresses with the given attachment files"""

    # create the email
    msg = MIMEMultipart()
    msg["From"] = bot_address
    msg["To"] = COMMASPACE.join(send_to)
    msg["Subject"] = subject
    msg.attach(MIMEText(body))

    # add the attachments
    for attachment in files:
        msg.attach(prepare_attachment(attachment))

    # send the email
    SERVER = "mail.privateemail.com"
    SERVER_EXTENSION = "587"
    smtp = smtplib.SMTP(SERVER, SERVER_EXTENSION)
    smtp.starttls()
    smtp.login(bot_address, bot_password)
    smtp.sendmail(bot_address, send_to, msg.as_string())
    smtp.close()

if __name__=="__main__":
    bot_address = BotCredentials.bot_username
    bot_password = BotCredentials.bot_password
    send_to = ["redacted"]
    subject = "Hello, this is the subject"
    text = "This is the body."
    files = []

    send_mail(bot_address, bot_password, send_to, subject, text, files)
