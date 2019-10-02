# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

def SendResEmail(receiver_addr, score, test_name):
	# create message object instance
	msg = MIMEMultipart()
	 
	message = u"Вы набрали " + str(score) + u" баллов из 20 за тест по теме " + test_name

	# setup the parameters of the message
	msg['From'] = "chemist1567@gmail.com"
	msg['To'] = receiver_addr
	msg['Subject'] = "Chemistry_test"
	 
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))

	#create server
	#Login Credentials for sending the mail

	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	pwd = "Beredes2Q"
	smtpserver.login('chemist1567@gmail.com', pwd)

	 
	# send the message via the server.
	smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())
	smtpserver.quit()

def CreateAccessCode(receiver_addr, send):
	acs = os.urandom(64).hex()
	if send == True:
		msg = MIMEMultipart()
		
		message = u"Access code is: " + acs

		# setup the parameters of the message
		msg['From'] = "chemist1567@gmail.com"
		msg['To'] = receiver_addr
		msg['Subject'] = "Code for access"
		 
		# add in the message body
		msg.attach(MIMEText(message, 'plain'))

		#create server
		#Login Credentials for sending the mail

		smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		pwd = "Beredes2Q"
		smtpserver.login('chemist1567@gmail.com', pwd)

		 
		# send the message via the server.
		smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())
		smtpserver.quit()
		
	else:
		print(acs)
	return(acs)