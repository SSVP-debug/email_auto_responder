import imaplib                                # important libraries to connect to gmail server
import email
from email.header import decode_header
import smtplib
from email.message import EmailMessage
import socket
import schedule
import time
import re

# ----------- Configuration -------------
EMAIL = "nerellabunny5@gmail.com"         # Your email
APP_PASSWORD = "stxnyvbfntqsbksn"     # App-specific password from Gmail -note that it is not your gmail password
SMTP_SERVER = "smtp.gmail.com"
IMAP_SERVER = "imap.gmail.com"
NAME = EMAIL.split('@')[0]
paln_name = re.sub(r'\d+', '', NAME)
RESPONDED_LOG = set()                  # To avoid replying twice
# ---------------------------------------

# ----------- Function to check new emails ----------
def check_emails():
    print("Checking for new emails...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        inbox_mails = mail.select("inbox")

        if "no-reply" in inbox_mails:
            return None
        status, messages = mail.search(None, 'UNSEEN')            # Search for unseen messages
        email_ids = messages[0].split()

        for num in email_ids:
            _, msg_data = mail.fetch(num, '(RFC822)')              # specail code- raw data of inbox
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_subject = decode_header(msg["Subject"])[0][0]    # [0][0] indicates subject section
                    if isinstance(email_subject, bytes):
                        email_subject = email_subject.decode()
                    from_email = msg["From"]
                    
                    # Skip if already responded
                    if from_email in RESPONDED_LOG:
                        continue
                    
                    print(f"New email from {from_email} with subject: {email_subject}")
                    send_auto_reply(from_email, email_subject)
                    RESPONDED_LOG.add(from_email)

        mail.logout()
    except (imaplib.IMAP4.abort, socket.error, EOFError) as e:
        print("Error checking emails:", e)

# ---------- Function to Send Auto-Reply -----------
def send_auto_reply(to_email, subject):
    try:
        reply = EmailMessage()
        reply["Subject"] = f"Re: {subject}"
        reply["From"] = EMAIL
        reply["To"] = to_email
        reply.set_content(
            f"Dear HR/Faculty,\n\nThank you for reaching out. I have received your email and will get back to you shortly.\n\nBest regards,\n{paln_name.capitalize()}"
        )

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL, APP_PASSWORD)
            server.send_message(reply)
            print(f"Auto-reply sent to {to_email}")
    except Exception as e:
        print("Error sending reply:", e)

# ------------- Scheduling  the Checker -------------
schedule.every(1).minutes.do(check_emails)

print("📬 Auto Email Responder is now running...\n(Press Ctrl+C to stop)\n")

while True:
    schedule.run_pending()
    time.sleep(5)
