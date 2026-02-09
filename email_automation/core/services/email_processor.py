import time
from .gmail_service import GmailService
from ..models import EmailLog, RunControl
from .ai_reply import generate_acknowledgement


def process_emails_logic(run_id, token_data, use_stop=False):
    service = GmailService(token_data)
    emails = service.fetch_unseen_emails()

    control = None
    if use_stop:
        control = RunControl.objects.get(run_id=run_id)

    processed = []

    for e in emails:
        if use_stop:
            control.refresh_from_db()
            if control.stop_requested:
                break

        sender = (e.get("from") or "").lower()
        subject = e.get("subject") or ""
        subject_lower = subject.lower()

        is_system_email = any(x in sender for x in ["noreply", "no-reply", "newsletter"])

        if any(w in subject_lower for w in ["internship", "interview", "offer"]):
            body = "Thank you for reaching out regarding the opportunity."
            status = "REPLIED"
        elif not is_system_email:
            body = generate_acknowledgement(subject)
            status = "ACKNOWLEDGED"
        else:
            body = None
            status = "NEEDS_REVIEW"

        if body:
            service.send_reply(
                e["from"],
                subject,
                body,
                thread_id=e["thread_id"],
                message_id=e["message_id"]
            )

        service.mark_as_read(e["id"])

        EmailLog.objects.create(
            run_id=run_id,
            sender_email=e["from"],
            subject=subject,
            status=status
        )

        processed.append({
            "from": e["from"],
            "subject": subject,
            "status": status
        })

        time.sleep(1)

    return processed
