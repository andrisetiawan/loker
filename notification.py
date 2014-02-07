#!/usr/bin/python
import smtplib
 
def send_email(previous_ip_list, previous_check_time, current_ip_list, current_check_time):

	# Email configuration.
	# Todo: Change it with actual configuration.
	SMTP_SERVER = 'smtp.gmail.com'
	SMTP_PORT = 587
	SENDER = 'shevtiawan@gmail.com'
	PASSWORD = "this_is_my_password"

	recipient = 'andri.setiawan@veritrans.co.id'
	subject = 'NSLOOKUP DIFF'


	body = build_mail_body(previous_ip_list, previous_check_time, current_ip_list, current_check_time)
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

def build_mail_body(previous_ip_list, previous_check_time, current_ip_list, current_check_time):
	message = "NSLOOKUP on Google.com found some differences. <br /><br />"

	message += "<strong>Current IP list:</strong> "
	message += "(Checked at: %s)" % current_check_time
	message += "<br />"
	for ip in current_ip_list:
		message = message + ip + "<br />"

	message += "<br /><strong>Previous IP list:</strong> "
	message += "(Checked at: %s)" % previous_check_time
	message += "<br />"
	for ip in previous_ip_list:
		message = message + ip + "<br />"

	return message