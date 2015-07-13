#!/usr/bin/python
import smtplib
import time
from email.mime.text import MIMEText

def alertMe(subject, body):
    myAddress = "lidreamer@163.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = myAddress
    msg['Reply-to'] = myAddress
    msg['To'] = myAddress
#smtp.163.com
#    server = smtplib.SMTP('smtp.qq.com',587)
    server = smtplib.SMTP('smtp.163.com',25)
    server.starttls()
    server.login(myAddress,'password')
    server.sendmail(myAddress,myAddress,msg.as_string())
    server.quit()
    
if __name__=="__main__":
    alertMe("Alert!!!","Door is open!!!")
    print 'Hello'
