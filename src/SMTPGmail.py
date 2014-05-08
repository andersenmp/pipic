# -*- coding: utf-8 -*-
"""
    pipic.SMTPGmail
    ~~~~~~~~~~~~~~

    Send email from Gmail using smptlib

    The MIT License (MIT)

    Copyright (c) 2013-2014 Andersen Pecorone
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
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
