from rest_framework.serializers import ModelSerializer
from users.models import User


class MinimumUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "avatar",
        )
