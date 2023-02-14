from rest_framework.serializers import ModelSerializer
from .models import User


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "name",
            "avatar",
        )


class JoinUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
        )
