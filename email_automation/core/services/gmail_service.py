import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


class GmailService:
    def __init__(self, token_data):
        if not token_data or "token" not in token_data:
            raise ValueError("Missing or invalid Gmail OAuth token data")

        self.creds = Credentials(
            token=token_data["token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri=token_data["token_uri"],
            client_id=token_data["client_id"],
            client_secret=token_data["client_secret"],
            scopes=token_data["scopes"],
        )

        #  Refresh token if expired
        if self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())

        self.service = build("gmail", "v1", credentials=self.creds)

    def fetch_unseen_emails(self):
        """
        Fetch unread emails from Inbox reliably.
        We do NOT rely on `is:unread` query due to Gmail API quirks.
        """
        results = self.service.users().messages().list(
            userId="me",
            q="in:inbox",
            maxResults=50
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            data = self.service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Message-ID"]
            ).execute()

            label_ids = data.get("labelIds", [])
            if "UNREAD" not in label_ids:
                continue

            headers = data.get("payload", {}).get("headers", [])

            email_data = {
                "id": msg["id"],
                "thread_id": data.get("threadId"),
                "from": "",
                "subject": "",
                "message_id": "",
            }

            for h in headers:
                if h["name"] == "From":
                    email_data["from"] = h["value"]
                elif h["name"] == "Subject":
                    email_data["subject"] = h["value"]
                elif h["name"] == "Message-ID":
                    email_data["message_id"] = h["value"]

            emails.append(email_data)

        return emails

    def send_reply(self, to_email, subject, body, thread_id=None, message_id=None):
        """
        Send a reply using Gmail API.
        Keeps the reply in the same conversation.
        """
        message = EmailMessage()
        message.set_content(body)
        message["To"] = to_email
        message["Subject"] = f"Re: {subject}"

        # 🧵 Threading headers
        if message_id:
            message["In-Reply-To"] = message_id
            message["References"] = message_id

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        request_body = {"raw": raw}
        if thread_id:
            request_body["threadId"] = thread_id

        self.service.users().messages().send(
            userId="me",
            body=request_body
        ).execute()

    def mark_as_read(self, message_id):
        """
        Mark an email as read to avoid duplicate processing.
        """
        self.service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()
