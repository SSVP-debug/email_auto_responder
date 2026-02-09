import uuid
import django_rq
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from .models import EmailLog, RunControl
from .services.google_oauth import get_oauth_flow
from .services.email_processor import process_emails_logic


def index(request):
    """
    GET  -> show Login or Run button
    POST -> run email automation
    """

    token_data = request.session.get("gmail_token")
    oauth_ready = isinstance(token_data, dict) and "token" in token_data

    # --------------------
    # POST: user clicked Run
    # --------------------
    if request.method == "POST":
        if not oauth_ready:
            return HttpResponse(
                "Google account not connected. Please login first.",
                status=403
            )

        run_id = str(uuid.uuid4())
        RunControl.objects.create(run_id=run_id)

        # ---- ASYNC MODE ----
        if settings.EMAIL_PROCESSING_MODE == "async":
            queue = django_rq.get_queue("default")
            queue.enqueue(
                process_emails_logic,
                run_id,
                token_data,
                use_stop=True
            )

            return render(request, "core/processing.html", {
                "emails": [],
                "run_id": run_id
            })

        # ---- SYNC MODE ----
        processed = process_emails_logic(
            run_id,
            token_data,
            use_stop=False
        )

        return render(request, "core/processing.html", {
            "emails": processed,
            "run_id": run_id
        })

    # --------------------
    # GET: just show page
    # --------------------
    return render(request, "core/index.html", {
        "oauth_ready": oauth_ready
    })


def google_login(request):
    flow = get_oauth_flow()
    flow.redirect_uri = "http://127.0.0.1:8000/oauth/callback/"

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session["oauth_state"] = state
    return redirect(authorization_url)


def google_callback(request):
    flow = get_oauth_flow()
    flow.redirect_uri = "http://127.0.0.1:8000/oauth/callback/"
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    request.session["gmail_token"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
        
    }

    return redirect("index")


def overview(request, run_id):
    emails = EmailLog.objects.filter(run_id=run_id).order_by("created_at")
    return render(request, "core/overview.html", {"emails": emails})


def stop_run(request, run_id):
    RunControl.objects.filter(run_id=run_id).update(stop_requested=True)
    return redirect("overview", run_id=run_id)
# Debug utility – used during OAuth testing
def reset_session(request):
    request.session.flush()
    return HttpResponse("Session reset successfully. Go back to home page.")
