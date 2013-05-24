import mc
from getpass import getpass
import urllib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import string
import random
import os
import filecmp
import multiprocessing
from KeyLimeDefs import *
username = raw_input('Email username? ')
password = getpass('Email password? (hidden) ')
servername = raw_input('Server\'s name? ')
ipaddress = raw_input('Your external IP address? ')
ospath = os.path.expanduser('~')
code = generate_id()
usedCode = None
print 'Authentication code is ' + code
mcserver = mc.Server()
mcserver.start()
"""if open('status.txt', 'r+').read() == 'offline':
	emailserver = smtplib.SMTP('smtp.gmail.com:587')
	emailserver.starttls()
	emailserver.login(username,password)
	online(emailserver)
	open('status.txt', 'w+').write('online')"""
def main():
	global code
	global ipaddress
	global mcserver
	global emailList
	while True: #main loop
		urllib.urlretrieve("http://dl.bukkit.org/latest-beta/craftbukkit.jar", ospath + '/craftbukkit/compare.jar')
		if not filecmp.cmp(ospath + '/craftbukkit/compare.jar', ospath + '/craftbukkit/craftbukkit.jar'):
			mcserver.command('stop Updating server')
			os.remove(ospath + '/craftbukkit/compare.jar')
			urllib.urlretrieve("http://dl.bukkit.org/latest-beta/craftbukkit.jar", ospath + '/craftbukkit/craftbukkit.jar')
			mcserver.start()
		if not mcserver.status():
			emailserver = smtplib.SMTP('smtp.gmail.com:587')
			emailserver.starttls()
			emailserver.login(username,password)
			open('status.txt', 'w+').write('offline')
			downtime('unknown reason', emailserver)
			while not mcserver.status():
				pass #wait until server is back up to continue
			online(emailserver)
		testip = urllib.urlopen("http://bot.whatismyipaddress.com").read()
		if not testip == ipaddress:
			ipaddress = testip
			emailserver = smtplib.SMTP('smtp.gmail.com:587')
			emailserver.starttls()
			emailserver.login(username,password)
			downtime('IP adress change', emailserver)
		time.sleep(300)
def codegen():
	global code
	code = generate_id()
	print code
	time.sleep(120)
def commandcheck():
	global code
	global usedCode
	global mcserver
	usedCode = None
	while True:
		latest_email = imap_get_latest(username, password, 'imap.gmail.com')
		if latest_email['Subject'] == code and not latest_email['Subject'] == usedCode:
			body = latest_email.get_payload()[0].get_payload()
			mcserver.command(body)
			usedCode = code
			code = generate_id()
			sendemail(username, password, 'smtp.gmail.com:587', 'Thanks. Command was ' + body + '. The new code is ' + code, "Command ran successfully", latest_email['From'])
			print code
		time.sleep(60)
def cellcheck():
	global code
	global mcserver
	global usedCode
	while True:
		latest_email = imap_get_latest(username, password, 'imap.gmail.com')
		#print latest_email['From'].split('@')[1].split('>')[0] == 'txt.voice.google.com'
		#print latest_email.get_payload()[:7] == code + ' '
		if latest_email['From'].split('@')[1].split('>')[0] == 'txt.voice.google.com':
			cellmsg = latest_email.get_payload()
			if cellmsg[:7] == code + ' ' and not cellmsg[:7] == usedCode:
				mcserver.command(cellmsg[7:])
				usedCode = code
				code = generate_id()
				sendemail(username, password, 'smtp.gmail.com:587', servername + ' ran command ' + cellmsg[7:], 'RE: ' + latest_email['Subject'], latest_email['From'])
				sendemail(username, password, 'smtp.gmail.com:587', 'The new code is ' + code + '.', 'RE: ' + latest_email['Subject'], latest_email['From'])
mainloop = multiprocessing.Process(target=main, args=())
emailcheck = multiprocessing.Process(target=cellcheck, args=())
#codegen = multiprocessing.Process(target=codegen, args=())
mainloop.start()
#codegen.start()
emailcheck.start()


		
		
		
		
