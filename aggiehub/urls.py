from django.urls import path
from aggiehub import views

urlpatterns = [
    path("", views.home, name="home"),
]
