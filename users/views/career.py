from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from users import models
from users import serializers


class UserCareer(APIView):
    def get(self, request, user_pk):
        user = models.User.objects.get(pk=user_pk)
        career = models.Career.objects.filter(user=user)
        serializer = serializers.CareerSerializer(
            career,
            many=True,
        )

        return Response(serializer.data)
