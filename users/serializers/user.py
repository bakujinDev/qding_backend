from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users import models
from qnas import serializers as qnasSerializers


class AuthSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username",)


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "pk",
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
            "introduce",
            "is_owner",
            "blog",
            "github",
        )

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if request:
            return obj == request.user
        return False
