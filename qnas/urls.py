from django.urls import path
from . import views

urlpatterns = [
    path("questions", views.Questions.as_view()),
    path("questions/@<int:user_pk>", views.QuestionByCreator.as_view()),
    path("questions/<int:question_id>", views.QuestionDetail.as_view()),
    path("questions/<int:question_id>/choice_answer", views.ChoiceAnswer.as_view()),
    path("questions/<int:question_id>/vote", views.QuestionVotes.as_view()),
    path("questions/<int:question_id>/comments", views.QuestionComments.as_view()),
    path("questions/<int:question_id>/answers", views.AnswerPost.as_view()),
    path("questions/comments/<int:comment_id>", views.QuestionCommentDetail.as_view()),
    path("answers/@<int:user_pk>", views.AnswerByCreator.as_view()),
    path("answers/<int:answer_id>/vote", views.AnswerVotes.as_view()),
    path("answers/<int:answer_id>/comments", views.AnswerComments.as_view()),
    path("answers/comments/<int:comment_id>", views.AnswerCommentDetail.as_view()),
    path("tags", views.Tags.as_view()),
    path("tags/@<int:user_pk>", views.TagHistory.as_view()),
]
