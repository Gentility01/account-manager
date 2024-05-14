from django.urls import path

from core.applications.home import views

app_name = "homeapp"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
