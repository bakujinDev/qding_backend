from django.urls import path
from . import views

urlpatterns = [
    path("questions", views.Questions.as_view()),
]
