# -*- coding: utf-8 -*-
"""
    mailwebcan.IMAPGmail
    ~~~~~~~~~~~~~~

    Retrive emails from Gmail using imaplib

    :copyright: (c) 2013 by Andersen Pecorone.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
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
