from django.urls import path
from . import views

urlpatterns = [
    path("questions", views.Questions.as_view()),
    path("questions/<int:question_id>", views.QuestionPost.as_view()),
    path("questions/<int:question_id>/comments", views.QuestionComment.as_view()),
    path("questions/<int:question_id>/answers", views.AnswerPost.as_view()),
    path("answers/<int:answer_id>/comments", views.AnswerComment.as_view()),
    path("tags", views.Tags.as_view()),
]
