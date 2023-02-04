from rest_framework import serializers
from .models import Question
from common import serializers as commonSerializers


class QuestionListSerializer(serializers.ModelSerializer):
    creator = commonSerializers.MinimumUserSerializer()
    editor = commonSerializers.MinimumUserSerializer()

    class Meta:
        model = Question
        fields = (
            "creator",
            "editor",
            "title",
            "content",
            "select_answer",
            "view_count",
            "updated_at",
            "answers_count",
        )

    def get_answers_count(self, question):
        self.answers_count()


# class RoomListSerializer(serializers.ModelSerializer):
#     rating = serializers.SerializerMethodField()
#     is_owner = serializers.SerializerMethodField()
#     photos = PhotoSerializer(
#         many=True,
#         read_only=True,
#     )

#     class Meta:
#         model = Room
#         fields = (
#             "pk",
#             "name",
#             "country",
#             "city",
#             "price",
#             "rating",
#             "is_owner",
#             "photos",
#         )
#         depth = 1

#     def get_rating(self, room):
#         return room.rating()

#     def get_is_owner(self, room):
#         request = self.context.get("request")
#         if request:
#             return room.owner == request.user
#         return False
