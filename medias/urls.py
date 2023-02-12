from django.urls import path
from .views import GetUploadURL


urlpatterns = [
    path("photos/get-url", GetUploadURL.as_view()),
]
