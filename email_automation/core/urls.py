from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("oauth/login/", views.google_login, name="google_login"),
    path("oauth/callback/", views.google_callback, name="google_callback"),
    path("reset/", views.reset_session, name="reset_session"),
    path("overview/<str:run_id>/", views.overview, name="overview"),
    path("stop/<str:run_id>/", views.stop_run, name="stop_run"),
]
