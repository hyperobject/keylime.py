import smtplib
import imaplib
import email
import time
import string
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
servername = None
username = None
carrier= None
cellnumber = None
emailList = [i.strip() for i in open("emails.txt", "r+").readlines()]
def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
def downtime(reason, server):
	global emailList
	global servername
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Server downtime"
	msg['From'] = servername
	msg['To'] = ', '.join(emailList)
	text = "Hi all!\nThe server is currently experiencing some downtime. Server admins have been notified, and you will recieve another message when the server is back up.\nHappy Crafting!"
	html = """\
	<html>
		<head></head>
		<body style="font-family: Trebuchet MS;">
		<p>Hi all!<br> the server is currently </p><p style="color:red;display:inline;">OFFLINE</p><p> because %s . Server admins have been notified, and you will recieve another email when the server is back up.<br>Happy Crafting!</p>
		</body>
	</html>
"""
	html = html % (reason)
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	msg.attach(part1)
	msg.attach(part2)
	server.sendmail(username, emailList, msg.as_string())
	server.quit()
def online(server):
	global servername
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Server is back up!"
	msg['From'] = servername
	msg['To'] = ', '.join(emailList)
	text = "Hi all!\nThe server is now back online.\nHappy Crafting!"
	html = """\
	<html>
		<head></head>
		<body style="font-family: Trebuchet MS;">
		<p>Hi all!<br> The server is now back online.<br>Happy Crafting!</p>
		</body>
	</html>
"""
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	msg.attach(part1)
	msg.attach(part2)
	server.sendmail(username, emailList, msg.as_string())
	server.quit()
def imap_get_latest(username, password, imap):
	imap_server = imaplib.IMAP4_SSL(imap)
	imap_server.login(username, password)
	imap_server.select('inbox')
	result, data = imap_server.uid('search', None, "ALL")
	latest_email_uid = data[0].split()[-1]
	result, data = imap_server.uid('fetch', latest_email_uid, '(RFC822)')
	raw_email = data[0][1]
	imap_server.logout()
	return email.message_from_string(raw_email)
def sendemail(username, password, server, body, subject, toaddr):
	global servername
	msg = MIMEMultipart()
	msg['From'] = servername
	msg['To'] = toaddr
	msg['Subject'] = subject
	part = MIMEText(body, 'plain')
	msg.attach(part)
	emailserver = smtplib.SMTP(server)
	emailserver.starttls()
	emailserver.login(username,password)
	emailserver.sendmail(username, toaddr, msg.as_string())
	emailserver.quit()
