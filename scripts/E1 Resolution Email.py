import csv
import smtplib
from email.message import EmailMessage

#points to mailhog
SMTP_SERVER = "smtp.d522.wgu.internal"
SMTP_PORT = 1025
FROM_EMAIL = "monitor@d522.wgu.internal"
TO_EMAIL = "stakeholders@d522.wgu.internal"

#lists devices that were fixed
remediated_names = ["PC2", "PC3", "SVR1", "SVR2"]

body = "Dear Stakeholders,\n"
body += "This is an automated notification to inform you that the DNS service issue and all related device compromises have been successfully resolved.\n"
body += "The following devices were affected and have now been remediated:\n"

csv_file = open("network_devices.csv", newline="")
reader = csv.DictReader(csv_file)
for device in reader:
    name = device["Device Name"]
    if name in remediated_names:
        body += "\n"
        body += "Hostname: " + name + "\n"
        body += "IP Address: " + device["Device Address"] + "\n"
csv_file.close()

body += "\n"
body += "No further action is required at this time. If you have any questions or concerns, please contact the IT support team.\n"
body += "Thank you for your attention.\n"
body += "Best regards,\n"
body += "Network Monitoring System\n"

msg = EmailMessage()
msg["Subject"] = "RESOLVED: DNS Service Issue and Device Compromise—All Issues Remediated"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL
msg.set_content(body)

smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp.send_message(msg)
smtp.quit()

print("Resolution email sent successfully.")