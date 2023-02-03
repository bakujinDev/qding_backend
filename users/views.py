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


def getRandomUserNickname():
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

    return f"{header} {footer} {InitUserName.objects.count()}"


class Users(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(
            username=username,
            email=username,
            name=getRandomUserNickname(),
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


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id={settings.GITHUB_ID}&client_secret={settings.GITHUB_SECRET}",
                headers={
                    "Accept": "application/json",
                },
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()

            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()

            try:

                user = User.objects.get(email=user_emails[0]["email"])
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

            except User.DoesNotExist:

                user = User.objects.create(
                    username=user_emails[0]["email"],
                    email=user_emails[0]["email"],
                    name=user_data.get("name") or getRandomUserNickname(),
                    avatar=user_data.get("avatar_url"),
                )

                user.set_unusable_password()
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
            "email_address": user.email,
        }
        site_address = "http://localhost:3000/"
        token = jwt.encode(payload, settings.SECRET_KEY)

        print(f"{site_address}{token}")

        emailContent = render_to_string(
            "email.html",
            {
                "email": user.email,
                "url": os.path.join(
                    site_address, "auth", "email_authentication", token
                ),
            },
        )

        email = EmailMessage(
            "[Qding] 회원 인증 메일입니다.",
            emailContent,
            to=[user.email],
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

        try:
            user = User.objects.get(username=email_address)
            user.email_authentication = True
            user.save()

        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
