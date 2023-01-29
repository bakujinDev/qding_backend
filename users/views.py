import requests
from django.conf import settings

# from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import PrivateUserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    # def put(self, request):
    #     user = request.user
    #     serializer = PrivateUserSerializer(
    #         user,
    #         data=request.data,
    #         partial=True,
    #     )

    #     if serializer.is_valid():
    #         user = serializer.save()
    #         serializer = PrivateUserSerializer(user)
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
