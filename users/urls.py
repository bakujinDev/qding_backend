from django.urls import path
from . import views

urlpatterns = [
    path("me", views.Me.as_view()),
    path("log-out", views.Logout.as_view()),
]
