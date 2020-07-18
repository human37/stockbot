from stocks import Stock
from smtplib import SMTP_SSL
from ssl import create_default_context

def sendEmail(message):
    
    with open('/Users/ammontaylor/logins/passwords.txt', 'r') as f:
        for line in f:
            password = line.strip()
    context = create_default_context()
    with SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login('dev.acc3025934@gmail.com', password)
        server.sendmail('dev.acc3025934@gmail.com', 'ammonx9@gmail.com', message)

