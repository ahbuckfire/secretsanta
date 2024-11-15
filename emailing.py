import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

HOST = "smtp.gmail.com"
SUBJECT = "Secret Santa Assignment Enclosed!"

def build_body(giver_name, receiver_name):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5dc; padding: 20px; color: #333;">
        <h2 style="color: #b22222; text-align: center;">🎅🎅🎅 Secret Santa Assignment 🎅🎅🎅</h2>
        <p>Hey <strong>{giver_name.capitalize()}</strong>,</p>
        <p style="font-size: 1.2em;">
            Get excited for <strong>Secret Santa</strong> this year!
        </p>
        <p style="font-size: 1.3em; color: #b22222; text-align: center;">
            🎁 You are tasked with gifting something to: <strong><u>{receiver_name.capitalize()}</u></strong> 🎁
        </p>
        
        <div style="margin-top: 20px; padding: 15px; background-color: #fff8e1; border: 1px solid #b22222; border-radius: 5px;">
            <h3 style="color: #006400; font-size: 1.2em; text-align: center;">The Details:</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><strong>🎁 How much can I spend?</strong> <span style="font-style: italic">{config.max_spend}</span></li>
                <li><strong>📅 When are we doing this?</strong> <span style="font-style: italic">{config.date_time}</span></li>
                <li><strong>📍 Where are we doing this?</strong> <span style="font-style: italic">{config.location.capitalize()}</span></li>
                <li><strong>👀 Who knows what the pairings are?</strong> No one!</li>
            </ul>
        </div>

        <p style="text-align: center; margin-top: 20px;">
            Some wise words to get in the mood:<br>
            <img src="https://partner.studentbeans.com/wp-content/uploads/2023/11/image-1.jpg" alt="Festive Office Sparkle" width="300" style="border-radius: 10px;">
        </p>

        <p style="font-size: 1.1em; color: #333; text-align: center;">
            Get excited(!),
        </p>
        <p style="text-align: center; font-weight: bold; color: #b22222;">
            The elves
        </p>
    </body>
    </html>
    """

def get_email_for_name(name):
	email = config.email_list.get(name)
	if email is None:
		raise Exception("no email registered for name {}".format(name))
	return email

def send_assignments(assignments):
	mailserver = smtplib.SMTP()
	mailserver._host = HOST
	mailserver.connect(HOST, 587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login(config.from_email, config.email_passkey)

	for giver, receiver in assignments.items():
		giver_email = get_email_for_name(giver)
		
		msg = MIMEMultipart()
		msg['From'] = config.from_email
		msg['To'] = giver_email
		msg['Subject'] = SUBJECT
		msg.attach(MIMEText(build_body(giver, receiver), "html"))

		try:
			mailserver.sendmail(config.from_email, giver_email, msg.as_string())
			print("successfully sent assignment to {giver} ({giver_email}) ".format(giver=giver, giver_email=giver_email))
		except Exception as e:
			print("error sending assignment to ", giver)
			print(e)

	mailserver.quit()
