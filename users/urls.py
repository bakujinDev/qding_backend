from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("email-login", views.EmailLogin.as_view()),
    path("github-login", views.GithubLogIn.as_view()),
    path("kakao-login", views.KakaoLogIn.as_view()),
    path("me", views.Me.as_view()),
    path("log-out", views.Logout.as_view()),
    path("email-auth", views.Email_Auth.as_view()),
    path("notification", views.Notifications.as_view()),
    path("notification/<int:pk>", views.NotificationDetail.as_view()),
    path("careers/@<int:user_pk>", views.UserCareer.as_view()),
    path("profile/@<int:pk>", views.UserProfile.as_view()),
]
