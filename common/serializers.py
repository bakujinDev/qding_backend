from rest_framework.serializers import ModelSerializer
from users.models.user import User


class NameUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
        )


class ProfileUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "avatar",
        )
