from django.urls import path
from .views import GetUploadURL

# from .views import

urlpatterns = [
    path("photos/get-url", GetUploadURL.as_view()),
]
