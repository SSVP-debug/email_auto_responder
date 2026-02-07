from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('overview/<str:run_id>/', views.overview, name='overview'),
    path('stop/<str:run_id>/', views.stop_run, name='stop_run'),
    
]
