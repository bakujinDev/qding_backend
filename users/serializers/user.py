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
    class Meta:
        model = models.User
        fields = (
            "pk",
            "name",
            "avatar",
        )
