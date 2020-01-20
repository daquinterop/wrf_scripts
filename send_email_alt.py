import pdb
import rlcompleter
from datetime import datetime
pdb.Pdb.complete=rlcompleter.Completer(locals()).complete 
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
date = datetime.today()
date_path = '{:04d}{:02d}{:02d}'.format(date.year, date.month, date.day)
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "daquinteropdev@gmail.com"  # Enter your address
list_receiver_email = ["daquinterop@gmail.com"]  # Enter receiver address
password ='5Y&&?hdx' 
subject = 'Subject: Weekly weather forecast {:04d}-{:02d}-{:02d}'.format(date.year, date.month, date.day)
body = "This is an email with attachment sent from Python"

for i in list_receiver_email:
    receiver_email = i  # Enter receiver address
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = '{:s}_Alt.zip'.format(date_path)  # In same directory as script

    # Open PDF file in binary mode
    with open('{:s}/{:s}'.format(filename.split('_')[0], filename), "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
