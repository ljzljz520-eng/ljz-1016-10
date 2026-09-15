from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("overview/", views.overview, name="overview"),
]
