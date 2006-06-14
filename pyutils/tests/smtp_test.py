#!/usr/bin/env python

import smtplib

def send_mail(fr, to, subject, body):
	header = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (fr, to, subject)

	msg = header + body
	server = smtplib.SMTP('mail.novell.com')
	server.sendmail(fr, to, msg)
	server.quit()


fr = 'wberrier@novell.com'
#to = 'wberrier@novell.com'
to = 'wberrier@berrier.org'


message = "Hey, what's up?"

send_mail(fr, to, 'testing', message)

