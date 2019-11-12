from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from aggiehub import views

urlpatterns = [
    path("", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    # path("ajax/validate_username/", views.validate_username, name='validate_username'),
]

urlpatterns += staticfiles_urlpatterns()
