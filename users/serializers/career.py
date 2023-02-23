from rest_framework import serializers
from users import models
from common import serializers as commonSerializers


class CareerSerializer(serializers.ModelSerializer):
    user = commonSerializers.NameUserSerializer(read_only=True)

    class Meta:
        model = models.Career
        fields = (
            "user",
            "company",
            "position",
            "first_day",
            "last_day",
        )
