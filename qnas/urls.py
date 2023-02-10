from django.urls import path
from . import views

urlpatterns = [
    path("questions", views.Questions.as_view()),
    path("questions/<int:id>", views.QuestionPost.as_view()),
    path("tags", views.Tags.as_view()),
]
