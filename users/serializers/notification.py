from rest_framework import serializers
from users import models
from common import serializers as commonSerializers


class NotificationSerializer(serializers.ModelSerializer):
    user = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.Notification
        fields = (
            "pk",
            "user",
            "content",
            "push_url",
            "updated_at",
        )


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = (
            "pk",
            "content",
            "push_url",
            "updated_at",
        )
