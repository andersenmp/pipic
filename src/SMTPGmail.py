# -*- coding: utf-8 -*-
"""
    mailwebcan.SMTPGmail
    ~~~~~~~~~~~~~~

    Send email from Gmail using smptlib

    :copyright: (c) 2013 by Andersen Pecorone.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SMTPGmail:

    def __init__(self, login, password):
        self.mail = smtplib.SMTP('smtp.gmail.com',587)
        self.mail.starttls()
        self.mail.login(login, password)

    def sendMail(self, from_addr, to_addr, subject, body, file_att):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.preamble = body
        if file_att:
            fp = open(file_att,'rb')
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename=file_att.rsplit('/')[1])
            fp.close()
            msg.attach(img)
            part = MIMEText('text', "plain")
            part.set_payload(body)
            msg.attach(part)
        self.mail.sendmail(from_addr, to_addr, msg.as_string())

    def logout(self):
        self.mail.quit()
