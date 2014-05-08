# -*- coding: utf-8 -*-
"""
    pipic.IMAPGmail
    ~~~~~~~~~~~~~~

    Retrive emails from Gmail using imaplib

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
import imaplib
import email
import smtplib

class IMAPGmail:
    def __init__(self, login, password):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
        self.mail.login(login, password)
        self.mail.select('INBOX')
        self.unseen_mail_count = 0

    def unseenMailsCount(self):
        return  self.unseen_mail_count

    def unseenMails(self):
        # Search for all new mail
        status, response = self.mail.search(None, '(UNSEEN)')
        email_ids = [e_id for e_id in response[0].split()]
        self.unseen_mail_count = len(email_ids)
        return email_ids

    def fetchMail(self, email_id):
        status, response = self.mail.fetch(email_id, '(RFC822)')
        raw_email = response[0][1]
        email_message = email.message_from_string(raw_email)
        return email_message

    def fetchAllUnseenMails(self):
        email_messages = []
        email_ids = self.unseenMails()
        if email_ids:
            for email_id in email_ids:
                email_messages.append(self.fetchMail(email_id))
        return email_messages

    def logout(self):
        self.mail.close()
        self.mail.logout()
