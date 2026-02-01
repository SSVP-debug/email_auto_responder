from django.db import models


class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('REPLIED', 'Replied (Auto)'),
        ('ACKNOWLEDGED', 'Acknowledged (Auto)'),
        ('NEEDS_REVIEW', 'Needs Manual Review'),
        ('FAILED', 'Failed'),
    ]

    run_id = models.CharField(max_length=100)

    sender_email = models.EmailField()
    subject = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    #  This answers your question: "Do I need to reply later?"
    needs_manual_reply = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_email} | {self.subject} | {self.status}"


class RunControl(models.Model):
    run_id = models.CharField(max_length=100, unique=True)
    stop_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"Run {self.run_id} | Stop: {self.stop_requested}"
