from rest_framework import serializers
from .models import Question, Answer, Tag
from common import serializers as commonSerializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
            "description",
        )


class QuestionListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = (
            "pk",
            "title",
            "content",
            "select_answer",
            "views",
            "updated_at",
            "answers_count",
            "tag",
            "votes",
        )

    def get_answers_count(self, question):
        self.answers_count()


class QuestionPostSerializer(serializers.ModelSerializer):
    creator = commonSerializers.MinimumUserSerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = (
            "creator",
            "title",
            "content",
            "tag",
        )
