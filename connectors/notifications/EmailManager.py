__author__ = 'snouto'

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailManager(object):

    def __init__(self,From,To,username,password):
        self.From = From
        self.To = To
        self.username = username
        self.password = password


    def setEmail(self,subject,message):
        self.subject = subject
        #self.message = "\r\n".join(["From:%s" % self.From,"To:%s" % self.To,"Subject: %s" % self.subject,'',message])
        self.message = MIMEMultipart("alternative")
        html = MIMEText(message,"html","utf-8")
        self.message['From'] = self.From
        self.message["To"] = self.To
        self.message["Subject"] = self.subject
        self.message.attach(html)



    def sendNotification(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username,self.password)
        server.sendmail(self.From, self.To, self.message.as_string())
        server.quit()
