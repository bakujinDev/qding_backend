from rest_framework import serializers
from .models import Photo
from common import serializers as commonSerializers


class PhotoSerializer(serializers.ModelSerializer):
    creator = commonSerializers.ProfileUserSerializer()

    class Meta:
        model = Photo
        fields = (
            "creator",
            "category",
            "file",
        )
