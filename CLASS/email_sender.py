import smtplib
from email.mime.text import MIMEText

class Email_sending(object):
    
    def sendEmail(self, status, address, body):
        print('EMAIL_SENDER: Logging in to gmail..')
        mail_from = 'miles.verify@gmail.com'
        mail_to = address

        message = MIMEText(body)
        
        if status == 0:
            message['subject'] = 'MILES: THE MAIL IS UNSAFE'
        elif status == 1:
            message['subject'] = 'MILES: THE MAIL IS SAFE'
        message['from'] = mail_from
        message['to'] = mail_to

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login('miles.verify@gmail.com', 'milesMILES123!@#')
        server.sendmail(mail_from, mail_to, message.as_string())
        server.quit
        print('EMAIL_SENDER: Successfully sent email to author.')
