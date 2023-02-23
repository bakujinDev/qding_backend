from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users import models
from qnas import serializers as qnasSerializers


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "pk",
            "username",
            "name",
            "avatar",
        )


class ProfileUserSerializer(ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            "pk",
            "name",
            "avatar",
            "message",
            "is_owner",
        )

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if request:
            return obj == request.user
        return False
