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


class Notifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = serializers.UserNotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)


class NotificationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
