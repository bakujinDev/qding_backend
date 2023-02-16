from rest_framework import serializers
from qnas import models
from common import serializers as commonSerializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = (
            "pk",
            "name",
            "description",
        )
