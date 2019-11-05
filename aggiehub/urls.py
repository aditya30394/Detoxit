from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from aggiehub import views

urlpatterns = [
    path("", views.login, name="login"),
    path("home/", views.home, name="home"),
]

urlpatterns += staticfiles_urlpatterns()
