import uuid
from time import sleep

from django.shortcuts import render, redirect

from .forms import EmailRunForm
from .models import EmailLog, RunControl
from .services.email_service import EmailService


def index(request):
    if request.method == 'POST':
        form = EmailRunForm(request.POST)

        if form.is_valid():
            run_id = str(uuid.uuid4())

            # create run control
            control = RunControl.objects.create(run_id=run_id)

            email_addr = form.cleaned_data['email']
            app_password = form.cleaned_data['app_password']

            service = EmailService(email_addr, app_password)
            processed_emails = []

            try:
                service.connect()
                emails = service.fetch_unseen_emails()

                for e in emails:
                    # refresh STOP flag
                    control.refresh_from_db()
                    if control.stop_requested:
                        break

                    sender = (e.get('from') or "").lower()
                    subject = e.get('subject') or ""
                    subject_lower = subject.lower()

                    is_system_email = (
                        "noreply" in sender or
                        "no-reply" in sender or
                        "newsletter" in sender
                    )

                    # ---- Decision Logic ----
                    if any(
                        word in subject_lower
                        for word in ["internship", "interview", "offer", "application"]
                    ):
                        service.send_reply(e['from'], subject)
                        status = "REPLIED"
                        needs_manual = True

                    elif not is_system_email:
                        # safe acknowledgment
                        service.send_reply(e['from'], subject)
                        status = "ACKNOWLEDGED"
                        needs_manual = True

                    else:
                        status = "NEEDS_REVIEW"
                        needs_manual = False

                    # ---- Save to DB ----
                    EmailLog.objects.create(
                        run_id=run_id,
                        sender_email=e['from'],
                        subject=subject,
                        status=status,
                        needs_manual_reply=needs_manual
                    )

                    processed_emails.append({
                        'from': e['from'],
                        'subject': subject,
                        'status': status
                    })

                    sleep(1)  # visual / demo realism

            except Exception as ex:
                return render(request, 'core/processing.html', {
                    'emails': [],
                    'error': str(ex),
                    'run_id': run_id
                })

            finally:
                service.close()

            return render(request, 'core/processing.html', {
                'emails': processed_emails,
                'run_id': run_id
            })

    else:
        form = EmailRunForm()

    return render(request, 'core/index.html', {'form': form})


def stop_run(request, run_id):
    RunControl.objects.filter(run_id=run_id).update(stop_requested=True)
    return redirect('overview', run_id=run_id)


def overview(request, run_id):
    emails = EmailLog.objects.filter(run_id=run_id).order_by('created_at')

    return render(request, 'core/overview.html', {
        'emails': emails
    })
