from rest_framework import serializers
from .models import Photo
from common import serializers as commonSerializers


class PhotoSerializer(serializers.ModelSerializer):
    creator = commonSerializers.MinimumUserSerializer()

    class Meta:
        model = Photo
        fields = (
            "creator",
            "category",
            "file",
        )
