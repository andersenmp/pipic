#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    mailwebcan.main
    ~~~~~~~~~~~~~~

    Retrieve emails and send webcan  pics from Gmail using imapliband smtp

    :copyright: (c) 2013 by Andersen Pecorone.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

# import modules used here
import sys, os, subprocess
import ConfigParser
import datetime, time
from time import sleep
from IMAPGmail import IMAPGmail
from SMTPGmail import SMTPGmail

# Gather our code in a main() function
def main():
    allowed_emails = []
    config = ConfigParser.ConfigParser()
    config.readfp(open('parameters.ini'))
    print 'Service version %s started' %  config.get('app','version',0)
    print 'Running on %s' % sys.platform
    allowed_emails =  [ email for email in config.get('app','allowed_emails',0).split(',') ]

    while True:
        try:
            print 'Connecting IMAP server'
            mail_server = IMAPGmail(config.get('gmail','user', 0), config.get('gmail','password',0))
            print 'Fetching mails'
            mails = mail_server.fetchAllUnseenMails()
            print 'New mails -> ', len(mails)
            if mails:
                mail_smtp = SMTPGmail(config.get('gmail','user',0), config.get('gmail','password',0))
                for mail in mails:
                    if isEmailAllowed(mail['From'], allowed_emails):
                        print 'Email %s allowed!' % mail['From']
                        pic_name = 'pics/pic_'+str(time.time())+'.jpg'
                        print 'Taking picture'
                        takePic(pic_name,config.getboolean('motion','present'))
                        print 'Sending mail to ' + mail['From']  + ' with pic ' +  pic_name
                        mail_smtp.sendMail(mail['To'], mail['From'],'Hello from PiPic','There you go!',pic_name)
                    else:
                        print 'Email %s NOT allowed!' % mail['From']
                        pic_name = 'pics/not_allowed.jpg'
                        print 'Sending mail to ' + mail['From'] + ' with pic ' + pic_name
                        mail_smtp.sendMail(mail['To'], mail['From'],'Hello from PiPic','No pics for you!',pic_name)

                mail_smtp.logout()
            print 'Logout IMAP'
            mail_server.logout();
            print 'Going to sleep for %d secs' % config.getint('app','standby_time')
            sleep(config.getint('app','standby_time'))

        except KeyboardInterrupt:
            break
        except:
            print 'Exception:', sys.exc_info()
            sleep(10)
            continue

    print 'Logout service'

def isEmailAllowed(email, allowed_emails):
    for email_addr in allowed_emails:
        if email.strip().find(email_addr.strip()) > -1:
            return True
    return False

def startStopMotion():
    cmd = 'ps -ef | pgrep motion'
    ps = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
    process_num = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    print 'PID: ', process_num
    if process_num:
        cmd = 'stop'
    else:
        cmd = 'start'

    print cmd, ' motion'
    cmd = 'sudo /etc/init.d/motion ' + cmd
    os.system(cmd)


def takePic(pic_name,motion):
    if sys.platform = 'darwin':
        cmd = './imagesnap -q -w 1 ' + pic_name
    else:
        cmd = 'fswebcam -r 640x480 -S 15 --jpeg 95 --title "PiPic" --subtitle "Framboesa Pi" --info "WebCam 1" --input 0 --set brightness=50% --set framerate=15 -d /dev/video0 --save ' + pic_name

    if motion:
        startStopMotion()
    os.system(cmd)
    if motion :
        startStopMotion()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()

