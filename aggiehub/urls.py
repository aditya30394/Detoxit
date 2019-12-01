from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from aggiehub import views

urlpatterns = [
    path("", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("ajax/delete/", views.delete_post, name='delete_post'),
    path("ajax/claim/", views.claim_post, name='claim_post'),
    path("survey/<int:sid>/", views.survey, name="survey"),
]

urlpatterns += staticfiles_urlpatterns()
