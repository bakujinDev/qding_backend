import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import PrivateUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage


class User(APIView):
    def post(self, request):
        password = request.data.get("password")

        if not password:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PrivateUserSerializer(data=request.data)

        if serializer.is_valid():
            print("able")
            # user = serializer.save()
            # user.set_password(password)
            # user.save()
            # serializer = PrivateUserSerializer(user)
            # return Response(serializer.data)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


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


class Logout(APIView):
    def post(self, request):
        refresh = request.data.get("refresh")
        token = RefreshToken(refresh)
        token.blacklist()
        return Response(status=status.HTTP_200_OK)


class Email_Auth(APIView):
    def post(self, request):
        email_address = request.data.get("email_address")

        email = EmailMessage(
            "Title",  # 이메일 제목
            "Content",  # 내용
            to=[email_address],  # 받는 이메일
        )
        email.send()
        return Response(status=status.HTTP_200_OK)
