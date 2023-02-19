from rest_framework.serializers import ModelSerializer
from users import models


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "pk",
            "username",
            "name",
            "avatar",
        )


class JoinUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "username",
            "name",
        )
