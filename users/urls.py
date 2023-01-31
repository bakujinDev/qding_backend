from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("log-out", views.Logout.as_view()),
    path("email-auth", views.Email_Auth.as_view()),
]
