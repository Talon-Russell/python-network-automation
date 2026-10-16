import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
#specifys where to send email
SMTP_SERVER = "smtp.d522.wgu.internal"
SMTP_PORT = 1025
FROM_EMAIL = "monitor@d522.wgu.internal"
TO_EMAIL = "stakeholders@d522.wgu.internal"
#lists devices with bad dns
compromised_names = ["PC2", "PC3", "SVR1", "SVR2"]

body = "Dear Stakeholders,\n"
body += "This is an automated alert to inform you that the following device(s) have been identified as compromised during the recent network scan:\n"
#opens csv file
csv_file = open("network_devices.csv", newline="")
reader = csv.DictReader(csv_file)

for device in reader:
    name = device["Device Name"]
    if name in compromised_names:
        body += "\n"
        body += "Device Name: " + name + "\n"
        body += "IP Address: " + device["Device Address"] + "\n"
        body += "Service: DNS\n"

csv_file.close()
#pulls current date and time
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
body += "\n"
body += "Last Checked: " + now + "\n"
body += "Immediate investigation and remediation are recommended to prevent further impact.\n"
body += "If you have any questions, please contact the IT support team.\n"
body += "Best regards,\n"
body += "Network Monitoring System\n"

msg = EmailMessage()
msg["Subject"] = "URGENT: Device Compromise Detected—Immediate Attention Required"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL
msg.set_content(body)

smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp.send_message(msg)
smtp.quit()

print("Email sent.")