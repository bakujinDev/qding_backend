from rest_framework.serializers import ModelSerializer
from .models import User


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            "date_joined",
            "last_login",
        )


class JoinUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
        )
