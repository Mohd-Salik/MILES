from os import link, stat
import sys, imaplib, email, re
from url_processing import Url_processing
from email.header import decode_header
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import smtplib
from email.mime.text import MIMEText

class Email_Receiving(object):
    def __init__(self):
        super().__init__()
        self.regression = Url_processing()
        self.init()

    def init(self):
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")

    def login(self, user, password):
        self.imap.login(user, password)

    def logout(self):
        self.imap.close()
        self.imap.logout()
        
    def extractUrl(self, string):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)      
        return [x[0] for x in url]

    def getNumberMails(self):
        status, messages = self.imap.select("INBOX")
        counter = 0
        for i in range(1, 10):
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            if msg[0] is None:
                break
            else:
                counter +=1
        return counter

    def deleteMail(self):
        status, messages = self.imap.select("INBOX")
        status, messages = self.imap.search(None, "ALL")
        messages = messages[0].split(b' ')
        for mail in messages:
            res, msg = self.imap.fetch(mail, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                self.imap.store(mail, "+FLAGS", "\\Deleted")

    def processMail(self, textbox, progressbar, header):
        header.hide()
        progressbar.show()
        safe = True

        for x in range(0, 40):
                progressbar.setProperty("value", x)

        status, messages = self.imap.select("INBOX")
        print("STATUS:", status, "\nMESSAGES: ", messages)
        res, msg = self.imap.fetch(str(1), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
               
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                textbox.addItem("="*100)
                textbox.addItem("PROCESSING:    {}".format(subject))
                textbox.addItem("SENT BY:   {}".format(From))
                for x in range(41, 60):
                    progressbar.setProperty("value", x)

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            print(body)
                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        print(body)
                print("="*100)

                for x in range(61, 90):
                    progressbar.setProperty("value", x)

                textbox.addItem("\nEXTRACTED LINKS")
                email_urls = self.extractUrl(body)

                safe_url = []
                phishing_url = []
                print("SAFE:" , safe_url)
                print("PHISHING:", phishing_url)

                for links in email_urls:
                    textbox.addItem("   " + str(links))
                    value = self.regression.prediction(str(links))
                    if value != 0:
                        textbox.addItem("       -THIS URL LOOKS SAFE")
                        safe_url.append(links)
                    else:
                        textbox.addItem("       -WARNING: SUSPICIOUS URL")
                        phishing_url.append(links)
                        safe = False
                
                if safe is True:
                    message = """
                    Thank you for using Machine Integrated Learning for Email Safety (MILES).

                    The email you have sent is safe."
                    """
                    if len(safe_url) > 0:
                        message = message + """
                        ----------EXTRACTED SAFE LINKS----------
                        """

                        for links in safe_url:
                            message = message + """
                            {}
                            """.format(str(links))
                elif safe is False:
                    message = """
                    Thank you for using Machine Integrated Learning for Email Safety (MILES).

                    The email you have sent contains suspicious url links.



                    
                    """
                    if len(safe_url) > 0:
                        message = message + """
                        ----------EXTRACTED SAFE LINKS----------
                        """

                        for links in safe_url:
                            message = message + """
                            {}
                            """.format(str(links))
                    if len(phishing_url) > 0:
                        message = message + """
                        ----------EXTRACTED SUSPICIOUS LINKS----------
                        """

                        for links in phishing_url:
                            message = message + """
                            {}
                            """.format(str(links))
                    print("SAFE URL ",safe_url)
                    print("PHISHING ", phishing_url)

                self.sendEmail(From, message)
                status, messages = self.imap.select("INBOX")
                status, messages = self.imap.search(None, 'SUBJECT "{}"'.format(subject))
                messages = messages[0].split(b' ')
                self.imap.store(messages[0], "+FLAGS", "\\Deleted")
                print("Deleted Mail from MILES")

        
        for x in range(91, 100):
            progressbar.setProperty("value", x)
        progressbar.hide()
        header.show()
        textbox.addItem("\nFEEDBACK SENT TO :   {}".format(From))
        textbox.addItem("="*100)

        #########self.deleteMail(subject)####### 

    def extractInbox(self, total_mail):
        status, messages = self.imap.select("INBOX")
        print("STATUS:", status, "\nMESSAGES: ", messages)
        inbox = []
        for curmail in range(1, total_mail+1):
            res, msg = self.imap.fetch(str(curmail), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("\n\nSUBJECT:", subject)
                    print("FROM::", From, ":")
                    inbox.append(From)
                    inbox.append("  " + subject)
        return inbox

    def sendEmail(self, address, body):
        print('EMAIL_SENDER: Logging in to gmail..')
        mail_from = 'miles.verify@gmail.com'
        mail_to = address
        message = MIMEText(body)
        message['subject'] = 'MILES: YOUR EMAIL HAS BEEN PROCESSED'
        message['from'] = mail_from
        message['to'] = mail_to
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login('miles.verify@gmail.com', 'milesMILES123!@#')
        server.sendmail(mail_from, mail_to, message.as_string())
        server.quit
        print('Successfully sent email to author.')