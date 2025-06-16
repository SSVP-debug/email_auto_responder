import imaplib
import email
from email.header import decode_header
import smtplib
from email.message import EmailMessage
import schedule
import time

# ----------- Configuration -------------
EMAIL = "your_email@gmail.com"         # Your email
APP_PASSWORD = "your_app_password"     # App-specific password from Gmail
SMTP_SERVER = "smtp.gmail.com"
IMAP_SERVER = "imap.gmail.com"
RESPONDED_LOG = set()  # To avoid replying twice
# ---------------------------------------

# ----------- Function to check new emails ----------
def check_emails():
    print("Checking for new emails...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        # Search for unseen messages
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        for num in email_ids:
            _, msg_data = mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_subject = decode_header(msg["Subject"])[0][0]
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
    except Exception as e:
        print("Error checking emails:", e)

# ---------- Function to Send Auto-Reply -----------
def send_auto_reply(to_email, subject):
    try:
        reply = EmailMessage()
        reply["Subject"] = f"Re: {subject}"
        reply["From"] = EMAIL
        reply["To"] = to_email
        reply.set_content(
            "Dear HR/Faculty,\n\nThank you for reaching out. I have received your email and will get back to you shortly.\n\nBest regards,\n[Your Name]"
        )

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL, APP_PASSWORD)
            server.send_message(reply)
            print(f"Auto-reply sent to {to_email}")
    except Exception as e:
        print("Error sending reply:", e)

# ------------- Scheduling the Checker -------------
schedule.every(1).minutes.do(check_emails)

print("📬 Auto Email Responder is now running...\n(Press Ctrl+C to stop)\n")

while True:
    schedule.run_pending()
    time.sleep(5)
