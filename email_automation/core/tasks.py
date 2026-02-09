import time

from .models import EmailLog, RunControl
from .services.gmail_service import GmailService
from .services.ai_reply import generate_acknowledgement


def process_emails(run_id, token_data):
    """
    Background task:
    - Fetch unread emails
    - Decide reply type
    - Send replies
    - Save logs
    """

    service = GmailService(token_data)

    emails = service.fetch_unseen_emails()
    control = RunControl.objects.get(run_id=run_id)

    for e in emails:
        control.refresh_from_db()
        if control.stop_requested:
            break

        sender = (e.get("from") or "").lower()
        subject = e.get("subject") or ""
        subject_lower = subject.lower()

        is_system_email = (
            "noreply" in sender or
            "no-reply" in sender or
            "newsletter" in sender
        )

        if any(
            word in subject_lower
            for word in ["internship", "interview", "offer", "application"]
        ):
            service.send_reply(e["from"], subject)
            status = "REPLIED"
            needs_manual = True

        elif not is_system_email:
            ai_msg = generate_acknowledgement(subject)
            service.send_reply(e["from"], subject, ai_msg)
            status = "ACKNOWLEDGED"
            needs_manual = True

        else:
            status = "NEEDS_REVIEW"
            needs_manual = False

        EmailLog.objects.create(
            run_id=run_id,
            sender_email=e["from"],
            subject=subject,
            status=status,
            needs_manual_reply=needs_manual
        )

        # MARK EMAIL AS READ (CRITICAL)
        service.mark_as_read(e["id"])

        time.sleep(1)  # simulate processing
