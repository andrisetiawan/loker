#!/usr/bin/python
import smtplib
 
def send_email(key, command, previous_ip_list, previous_check_time, current_ip_list, current_check_time):

	# Email configuration.
	# Todo: Change it with actual configuration.
	SMTP_SERVER = 'smtp.gmail.com'
	SMTP_PORT = 587
	SENDER = 'ahnshev@gmail.com'
	PASSWORD = "this_is_email_password"

	recipient = 'andri.setiawan@veritrans.co.id'
	subject = '[nslookup report] %s - "%s" found some different result.' % (key, command)

	body = build_mail_body(key, command, previous_ip_list, previous_check_time, current_ip_list, current_check_time)
	headers = ["From: " + SENDER,
	           "Subject: " + subject,
	           "To: " + recipient,
	           "MIME-Version: 1.0",
	           "Content-Type: text/html"]
	headers = "\r\n".join(headers)
	 
	session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	session.ehlo()
	session.starttls()
	session.ehlo
	session.login(SENDER, PASSWORD)
	 
	session.sendmail(SENDER, recipient, headers + "\r\n\r\n" + body)
	session.quit()

def build_mail_body(key, command, previous_ip_list, previous_check_time, current_ip_list, current_check_time):
	message = '<style type="text/css">table{border-width: 0 0 1px 1px;border-spacing: 0;border-collapse: collapse;border-style: solid;} td, th {margin: 0;padding: 4px;border-width: 1px 1px 0 0;border-style: solid;}</style>'

	message += '"%s" found some different result. <br /><br />' % command

	message += "<table border=1>"
	message += "<tr>"
	message += "<td><strong>PREVIOUS</strong> <br /> (%s)</td>" % previous_check_time
	message += "<td><strong>CURRENT</strong> <br /> (%s)</td>" % current_check_time
	message += "<td><strong>STATUS</strong></td>"
	message += "</tr>"

	for i in xrange(0,(len(previous_ip_list))):
		if previous_ip_list[i] in current_ip_list:
			message += "<tr><td>%s</td><td>%s</td><td>-</td></tr>" % (previous_ip_list[i], previous_ip_list[i])
		else:
			message += '<tr><td style="color:#dd1111;">%s</td><td> - </td><td>missing</td></tr>' % previous_ip_list[i]

	for i in xrange(0,(len(current_ip_list))):
		if current_ip_list[i] in previous_ip_list:
			pass
		else:
			message += '<tr><td></td><td style="color:#dd1111;">%s</td><td>new</td></tr>' % current_ip_list[i]

	message += "</table>"

	return message