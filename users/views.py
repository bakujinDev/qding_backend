import os
import jwt
import requests
import random
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from .models import User, InitUserName
from .serializers import PrivateUserSerializer, JoinUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


class Users(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        header = (
            InitUserName.objects.filter(
                kind=InitUserName.NameKindChoices.HEADER,
            )
            .order_by(("?"))[0]
            .value
        )

        footer = (
            InitUserName.objects.filter(
                kind=InitUserName.NameKindChoices.FOOTER,
            )
            .order_by(("?"))[0]
            .value
        )

        name = f"{header} {footer} {InitUserName.objects.count()}"

        user = User.objects.create(
            username=username,
            email=username,
            name=name,
        )

        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
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
    def get(self, request):
        user = request.user

        if user.email_authentication:
            return Response(status=200)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user

        payload = {
            "email_address": user.username,
        }
        site_address = "http://localhost:3000/"
        token = jwt.encode(payload, settings.SECRET_KEY)

        print(f"{site_address}{token}")

        emailContent = render_to_string(
            "email.html",
            {
                "email": user.username,
                "url": os.path.join(site_address, "email_auth", token),
            },
        )

        email = EmailMessage(
            "[Qding] 회원 인증 메일입니다.",
            emailContent,
            to=[user.username],
        )
        email.content_subtype = "html"
        email.send()

        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        token = request.data.get("token")

        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256",
        )
        email_address = decoded.get(("email_address"))

        user = User.objects.get(username="dddd")
        user.email_authentication = True
        user.save()

        return Response(status=status.HTTP_200_OK)
