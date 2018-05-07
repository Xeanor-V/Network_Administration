import smtplib

def send_email(address, text):
	username = 'errorcentervega@gmail.com'
	msg = "\r\n".join([
  	"From: " + username,
  	"To: "+address,
  	"Subject: Error in network",
  	"",
  	text
  	])
	password = 'escom2018'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(username, address, msg)
	server.quit()

##send_email('vg.ursa@gmail.com','Houston we have a problem')
