import os, smtplib
from email.mime.text import MIMEText

import settings

emailLogin = os.getenv('SENDER_EMAIL')
emailPass = os.getenv('SENDER_EMAIL_PASS')

class Email:
    def _createMsg(self, recipient, subject, message):
        msg = MIMEText(message)

        msg['From'] = emailLogin
        msg['To'] = recipient

        msg['Subject'] = subject

        return msg

    def send(self, recipient, subject, message):
        try:
            server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
            msg = self._createMsg(recipient, subject, message)
            server.login(emailLogin, emailPass)
            server.sendmail(emailLogin, [recipient], msg.as_string())

        except Exception as e:
            print('ERROR:', e)

        finally:
            server.quit()
