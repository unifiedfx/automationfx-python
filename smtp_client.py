import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pystache
from datetime import datetime
import os
import json
from colorama import init
init(True)

class SmtpClient:
    sender_email = "my@gmail.com"
    password = "mypassword"
    smtp_server = "smtp.gmail.com"
    port = 465
    text_template = "template.txt"
    html_template = "template.html"
    filename = os.path.join(os.getcwd(), 'smtp_settings.json')
    def __init__(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as outfile:
                json.dump({
                    'sender_email': self.sender_email,
                    'password': self.password,
                    'smtp_server': self.smtp_server,
                    'port': self.port,
                    'text_template' : self.text_template,
                    'html_template' : self.html_template,
                    }, outfile, indent=4, sort_keys=True)
        else:
            json_data = open(self.filename).read()
            data = json.loads(json_data)
            self.__dict__.update(data)
    def save(self):
        with open(self.filename, 'w') as outfile:
            json.dump({
                'sender_email': self.sender_email,
                'password': self.password,
                'smtp_server': self.smtp_server,
                'port': self.port,
                'text_template' : self.text_template,
                'html_template' : self.html_template,
                }, outfile, indent=4, sort_keys=True)

    def send_email(self, email, renderdata, subject = None , copy = None, ):
      texttemplate = open(self.text_template, "r")
      text = texttemplate.read()
      htmltemplate = open(self.html_template, "r")
      html = htmltemplate.read()
      text = pystache.render(text,renderdata)
      html = pystache.render(html,renderdata)
      part1 = MIMEText(text, "plain")
      part2 = MIMEText(html, "html")
      # Add HTML/plain-text parts to MIMEMultipart message and the email client will try to render the last part first
      message = MIMEMultipart("alternative")
      message["Subject"] = "MigrationFX Activation"
      message["Subject"] = subject if subject is not None else "MigrationFX Activation" 
      message["From"] = self.sender_email
      message["To"] = email
      message["Cc"] = copy
      message.attach(part1)
      message.attach(part2)
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
        server.login(self.sender_email, self.password)
        if self.sender_email and email:
            server.sendmail(self.sender_email, email, message.as_string())
        else:
            print("\033[1;31;40m Unbale to send mail, Invalid email ({0}) or Incorrect SMTP Setting.".format(email))

