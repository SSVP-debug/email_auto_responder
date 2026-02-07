from time import sleep

from django.shortcuts import render, redirect

from .forms import EmailRunForm
from .models import EmailLog, RunControl
from .services.email_service import EmailService


import uuid
import django_rq

from django.shortcuts import render

from .forms import EmailRunForm
from .models import RunControl
from .tasks import process_emails


def index(request):
    if request.method == "POST":
        form = EmailRunForm(request.POST)

        if form.is_valid():
            run_id = str(uuid.uuid4())

            RunControl.objects.create(run_id=run_id)

            email_addr = form.cleaned_data["email"]
            app_password = form.cleaned_data["app_password"]

            queue = django_rq.get_queue("default")

            queue.enqueue(
                process_emails,
                run_id,
                email_addr,
                app_password,
                job_timeout=360,
                description="Email automation job"
            )


            return render(request, "core/processing.html", {
                "emails": [],
                "run_id": run_id
            })

    else:
        form = EmailRunForm()

    return render(request, "core/index.html", {"form": form})



def stop_run(request, run_id):
    RunControl.objects.filter(run_id=run_id).update(stop_requested=True)
    return redirect('overview', run_id=run_id)


def overview(request, run_id):
    emails = EmailLog.objects.filter(run_id=run_id).order_by('created_at')

    return render(request, 'core/overview.html', {
        'emails': emails
    })
