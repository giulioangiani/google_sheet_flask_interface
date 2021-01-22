import smtplib
import sys
import os
import time
import base64
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from config import mail_config

### NOTA
### Per inviare mail da script devi abilitare le "app meno sicure" nel
### pannello di controllo di Gmail
### Ref: https://support.google.com/accounts/answer/6010255?hl=it



def inviaMail(subject, to_address, mail_text):
		
	mailServer = smtplib.SMTP('smtp.gmail.com', 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(mail_config["gmailUser"], mail_config["gmailPwd"])

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = from_address = mail_config["sendermail"]
	msg['To'] = to_address


	html = """<div style='padding:3px; border:1px solid brown; background-color:#eeeeee'>
						TESTO DELLA MAIL
			</div>
	"""

	try:
		r = mailServer.sendmail(from_address, to_address, msg.as_string())
		if r == {}:
			esito = True
		else:
			esito = False
		txt = "Sent mail for <b>%(to_address)s</b> - result = <b>%(esito)s<b><br>" % vars()
	except:
		esito = False
		txt = "Error in sending for <b>%(to_address)s</b> - result = <b>%(esito)s<b><br>" % vars()
		import traceback
		print (traceback.format_exc())

	mailServer.close()
	return esito
	
if __name__ == '__main__':
	inviaMail("Primo messaggio con python e Gmail", "giulio.angiani@iispascal.it", "Il testo della mia mail")
