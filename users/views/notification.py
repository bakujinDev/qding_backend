from django.conf import settings
from django.db import transaction, connection
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from users.models import Notification
from users import serializers
from users import function
from qnas import models as qnasModels


class Notifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = serializers.UserNotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        model_type = request.data.get("type")
        model_pk = request.data.get("id")

        if model_type == "answer":
            model = qnasModels.Answer.objects.prefetch_related("notification_user").get(
                pk=model_pk
            )

        if not model:
            return Response(status.HTTP_400_BAD_REQUEST)

        res = function.subscribe_notification(
            model=model,
            request_user=request.user,
            create_or_delete=True,
        )

        return Response({"message": res})


class NotificationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
