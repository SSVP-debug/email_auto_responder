import imaplib
import email
from email.utils import parseaddr
from email.header import decode_header
import smtplib
from email.message import EmailMessage

class EmailService:
    def __init__(self, email_address, app_password):
        self.email_address = email_address
        self.app_password = app_password
        self.mail = None

    def connect(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.email_address, self.app_password)

    def fetch_unseen_emails(self):
        self.mail.select("inbox")

        status, messages = self.mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        results = []

        for eid in email_ids:
            _, msg_data = self.mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]

            msg = email.message_from_bytes(raw_email)

            sender = parseaddr(msg.get("From"))[1]
            subject, encoding = decode_header(msg.get("Subject"))[0]

            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            results.append({
                "from": sender,
                "subject": subject
            })

        return results

    def close(self):
        if self.mail:
            self.mail.logout()

    def send_reply(self, to_email, subject):
        msg = EmailMessage()
        msg["From"] = self.email_address
        msg["To"] = to_email
        msg["Subject"] = f"Re: {subject}"

        msg.set_content(
            "Thank you for your email.\n\n"
            "This is an automated acknowledgment to let you know I’ve received your message. "
            "I’ll review it and get back to you with a detailed response soon.\n\n"
            "Best regards"
)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.email_address, self.app_password)
            server.send_message(msg)
